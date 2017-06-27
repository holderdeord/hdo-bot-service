class bot_service::packages {
  package { 'apt-transport-https':
    ensure => installed
  }

  include apt

  apt::source {'nodesource':
    location => 'https://deb.nodesource.com/node_6.x',
    release  => 'xenial',
    repos    => 'main',
    key      => {
      id     => '9FD3B784BC1C6FC31A8A0A1C1655A0AB68576280',
      source => 'https://deb.nodesource.com/gpgkey/nodesource.gpg.key'
    },
    require => Package['apt-transport-https']
  }

  apt::source {'yarn':
    location => 'https://dl.yarnpkg.com/debian/',
    release  => 'stable',
    repos    => 'main',
    key      => {
      id     => '72ECF46A56B4AD39C907BBB71646B01B86E50310',
      source => 'https://dl.yarnpkg.com/debian/pubkey.gpg'
    },
    require => Package['apt-transport-https']
  }

  $packages = [
    'python3', 'python3-dev', 'python3-venv', 'python3-pip', 'git-core', 'yarn'
  ]

  package { $packages:
    ensure  => installed,
    require => Apt::Source['yarn']
  }

  package { 'nodejs':
    ensure  => latest,
    require => Apt::Source['nodesource']
  }
}