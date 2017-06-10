class bot_service {
  $packages = [
    'python3', 'python3-dev', 'python3-venv', 'python3-pip', 'supervisor'
  ]

  package { $packages:
    ensure => 'installed'
  }

  class { 'bot_service::nginx':
    tls_letsencrypt_account => 'nikolaik@gmail.com'
  }

}