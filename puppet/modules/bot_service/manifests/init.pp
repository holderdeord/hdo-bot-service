class bot_service(
  String $full_web_path = '/var/www'
) {
  # Packages
  include bot_service::packages

  # Lets Encrypt client
  class {'bot_service::letsencrypt':
    account => 'nikolaik@gmail.com'
  }

  include nginx

  file {'/etc/nginx/ssl/':
    ensure  => directory,
  }

  cron { 'run_puppet_apply':
    command => 'cd /home/nikolark/hdo-quiz-service/puppet && ./scripts/run_apply.sh',
    special => 'reboot'
  }

  file { $full_web_path:
    ensure => directory,
  }

  # default location
  nginx::resource::server { 'default':
    ensure         => present,
    server_name    => ['_'],
    listen_port    => 80,
    listen_options => 'default_server',
    www_root       => '/usr/share/nginx/html/'
  }

  nginx::resource::server { 'default_ssl':
    ensure         => present,
    server_name    => ['_'],
    listen_port    => 443,
    listen_options => 'default_server',
    www_root       => '/usr/share/nginx/html/',
    ssl            => true,
    ssl_port       => 443,
    ssl_cert       => '/etc/ssl/certs/ssl-cert-snakeoil.pem',
    ssl_key        => '/etc/ssl/private/ssl-cert-snakeoil.key',
  }

  class { 'supervisord':
    package_provider => 'apt',
    install_init     => false,
    service_name     => 'supervisor',
    executable       => '/usr/bin/supervisord',
    executable_ctl   => '/usr/bin/supervisorctl',
    config_include   => '/etc/supervisor/conf.d',
    config_file      => '/etc/supervisor/supervisord.conf'
  }

  class { 'postgresql::server':}

  include redis
}
