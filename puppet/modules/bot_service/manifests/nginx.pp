define bot_service::nginx (
  String $ssl_cert,
  String $ssl_key,
  # From https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-16-04 :
  String $ssl_ciphers = 'EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5',
  String $full_web_path = '/var/www',
  String $www_root = "${full_web_path}/${name}",
  String $static_path = '/static'
) {
  $server_name = [$name]

  # DH params
  file {'/etc/nginx/ssl/':
    ensure  => directory,
    recurse => true
  }

  file { $full_web_path:
    ensure => directory,
    owner => $::bot_service::app_user,
  }

  file { $www_root:
    ensure => directory,
    owner => $::bot_service::app_user,
  }

  $dhparam_path = "/etc/nginx/ssl/${name}-dhparam.pem"
  exec {"/usr/bin/openssl dhparam -out ${dhparam_path} 2048":
    creates => $dhparam_path
  }


  nginx::resource::upstream { 'upstream_app':
    members => ["localhost:${::bot_service::gunicorn_port}"]
  }

  # server with location /
  nginx::resource::server { $name:
    ensure              => present,
    server_name         => $server_name,
    listen_port         => 443,
    ssl                 => true,
    ssl_cert            => $ssl_cert,
    ssl_key             => $ssl_key,
    ssl_ciphers         => $ssl_ciphers,
    ssl_dhparam         => $dhparam_path,
    ssl_port            => 443,
    proxy               => "http://upstream_app",
    http2               => 'on',
    server_cfg_append   => {
      client_max_body_size => '100M'
    },
  }

  # static
  nginx::resource::location { "${name}_static":
    location       => $static_path,
    server         => $name,
    location_alias => $www_root,
    ssl            => true,
    ssl_only       => true
  }

  # Redirect port 80 to $name
  nginx::resource::server { "${name}_redir":
    ensure              => present,
    server_name         => $server_name,
    www_root            => '/var/www/html/',
    location_cfg_append => { 'rewrite' => "^ https://${name}\$request_uri? permanent" },
  }
}
