define bot_service::app (
  String $domain,
  String $app_path = "/opt/${name}",
  String $app_user = 'botapp',
  String $app_environment = 'production',
  String $python_path = "${app_path}/venv/bin/python3",
  String $pip_path = "${app_path}/venv/bin/pip",
  String $gunicorn_path = "${app_path}/venv/bin/gunicorn",
  String $yarn_path = '/usr/bin/yarn',
  String $botadmin_path = "${app_path}/botadmin/static/botadmin",
  String $botadmin_build_cmd = "${yarn_path} run build",
  Integer $gunicorn_port = 8000,
  Integer $gunicorn_num_workers = 2,
  String $gunicorn_wsgi = 'bot_service.wsgi',
  String $db_name = $name,
  String $db_user = $name,
  String $db_password = lookup('bot_service_db_password'),
) {
  # App environment
  $db_env = {'DATABASE_URL' => "postgresql://${db_user}:${db_password}@localhost:5432/${db_name}"}
  $program_environment = merge(lookup("bot_service_environment_${app_environment}", {merge => 'hash'}), $db_env)

  bot_service::letsencrypt::certificate { "${name}_certs":
    domains => [$domain]
  }

  bot_service::nginx { $domain:
    ssl_cert      => "${::bot_service::letsencrypt::certificate_path}/${domain}.crt",
    ssl_key       => "${::bot_service::letsencrypt::certificate_path}/${domain}.key",
    app_user      => $app_user,
    gunicorn_port => $gunicorn_port,
  }

  user { $app_user:
    ensure     => present,
    home       => "/home/${app_user}",
    managehome => true
  }

  file { "/home/${app_user}":
    ensure => directory,
    owner  => $app_user
  }

  file { $app_path:
    ensure => directory,
    owner  => $app_user
  }

  # Clone app
  vcsrepo { $app_path:
    ensure   => latest,
    user     => $app_user,
    provider => git,
    source   => 'https://github.com/holderdeord/hdo-quiz-service.git',
    revision => 'master',
    require  => File[$app_path]
  }

  # Python virtualenv and requirements
  exec { "${name}_venv":
    command => '/usr/bin/env python3 -m venv venv',
    creates => "${app_path}/bin/activate",
    cwd     => $app_path,
    user    => $app_user,
    require => Package[$bot_service::packages::packages]
  }

  exec { "${name}_pip_upgrade":
    command => "${pip_path} install -U pip wheel",
    cwd     => $app_path,
    user    => $app_user,
    require => Exec["${name}_venv"]
  }

  exec { "${name}_pip_install":
    command => "${pip_path} install -r requirements.txt",
    cwd     => $app_path,
    user    => $app_user,
    require => Exec["${name}_venv"]
  }

  # Process managment
  supervisord::program { $name:
    command             => "${gunicorn_path} --bind 127.0.0.1:${gunicorn_port} --workers ${gunicorn_num_workers} ${gunicorn_wsgi}",
    directory           => $app_path,
    user                => $app_user,
    autostart           => true,
    autorestart         => true,
    program_environment => $program_environment
  }

  # Database
  postgresql::server::db { $db_name:
    user     => $db_user,
    password => postgresql_password($db_user, $db_password),
  }

  # Enviroment hash to array (ninja style)
  $_sep = ';;;;;;;;;;;' # FIXME: tried \n but could not escape the escaping
  $_env_var_template = "<% @program_environment.each do |key,value| -%><%= key %>=<%= value %>${_sep}<% end -%>"
  $program_environment_array = split(inline_template($_env_var_template), $_sep)

  # App: Django database migrations
  exec { "${python_path} manage.py migrate --noinput":
    cwd         => $app_path,
    user        => $app_user,
    environment => $program_environment_array,
    require     => [Exec["${name}_pip_install"], Postgresql::Server::Db[$db_name]]
  }

  # App: yarn install
  exec { "${name}_yarn":
    command => $yarn_path,
    cwd     => $botadmin_path,
    user    => $app_user,
    require => Package[$bot_service::packages::packages]
  }

  # App: Build botadmin
  # FIXME: Takes forever
  exec { "${name}_botadmin_build":
    command     => $botadmin_build_cmd,
    cwd         => $botadmin_path,
    user        => $app_user,
    environment => $program_environment_array,
    require     => Exec["${name}_yarn"]
  }

  # App: Django collectstatic
  exec { "${name}_django_collectstatic":
    command     => "${python_path} manage.py collectstatic --noinput -i node_modules -i bower_components",
    cwd         => $app_path,
    user        => $app_user,
    environment => $program_environment_array,
    require     => Exec["${name}_botadmin_build"]
  }

  # App: Restart app srv
  exec { "/usr/bin/supervisorctl restart ${name}":
    require     => Exec["${name}_botadmin_build"]
  }

}
