class bot_service {
  $packages = [
    'python3', 'python3-dev', 'python3-venv', 'python3-pip', 'supervisor'
  ]

  package { $packages:
    ensure => 'installed'
  }

  $domain = 'hdo-bot-service.nkweb.no'
  bot_service::nginx { $domain:
    tls_letsencrypt_account => 'nikolaik@gmail.com'
  }

  include nginx

}