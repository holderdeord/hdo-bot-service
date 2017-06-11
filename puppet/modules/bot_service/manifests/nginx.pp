define bot_service::nginx (
  String $tls_letsencrypt_account,
  String $tls_letsencrypt_method = 'dns-01',
) {

  # From https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-16-04 :
  $ssl_ciphers = 'EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5'

  $full_web_path = '/var/www'
  $www_root = "${full_web_path}/${name}"

  $server_name = [$name]
  $domains = $server_name

  # Redirect port 80 to $name
  nginx::resource::server { "${name}_redir":
    ensure              => present,
    server_name         => $domains,
    www_root            => '/var/www/html/',
    location_cfg_append => { 'rewrite' => "^ https://${name}\$request_uri? permanent" },
  }
  nginx::resource::location { "${name}_redir_letsencrypt":
    server         => "${name}_redir",
    location       => '/.well-known/acme-challenge',
    location_alias => '/tmp/letsencrypt/.well-known/acme-challenge',
    index_files    => []
  }

  # FIXME: The following should run after Anchor[nginx::end] if possible
  # Lets Encrypt cert
  class {'bot_service::letsencrypt':
    account => $tls_letsencrypt_account
  }

  bot_service::letsencrypt::certificate { "${name}_certs":
    domains => $domains,
    method  => $tls_letsencrypt_method
  }

  # DH params
  file {'/etc/nginx/ssl/':
    ensure  => directory,
    recurse => true
  }

  $dhparam_path = "/etc/nginx/ssl/${name}-dhparam.pem"
  exec {"/usr/bin/openssl dhparam -out ${dhparam_path} 2048":
    creates => $dhparam_path
  }

  # server with location /
  nginx::resource::server { $name:
    ensure              => present,
    server_name         => $server_name,
    www_root            => $www_root,
    # location_cfg_append => '',  # FIXME: More
    index_files         => ['index.htm', 'index.html'],
    listen_port         => 443,
    ssl                 => true,
    ssl_cert            => "${::bot_service::letsencrypt::certificate_path}/${domains[0]}.crt",
    ssl_key             => "${::bot_service::letsencrypt::certificate_path}/${domains[0]}.key",
    ssl_ciphers         => $ssl_ciphers,
    ssl_dhparam         => $dhparam_path,
    ssl_port            => 443,
    http2               => 'on',
    server_cfg_append   => {
      client_max_body_size => '100M'
    },
  }

}
