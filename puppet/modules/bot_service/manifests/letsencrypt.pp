class bot_service::letsencrypt (
  String $account,
  String $lego_binary_url = 'https://github.com/xenolf/lego/releases/download/v0.4.1/lego_linux_amd64.tar.xz'
) {
  # Lego
  $path = '/usr/local/lib/lego'
  $bin_path = '/usr/local/bin'
  $bin = "${bin_path}/lego"
  $config_path = '/var/lib/lego'
  $certificate_path = "${config_path}/certificates"
  $owner = 'root'
  $webroot_path = '/tmp/letsencrypt'

  include ::archive

  file { $path:
    ensure => directory,
    owner  => $owner,
    group  => $owner,
    mode   => '0755'
  }

  archive { '/tmp/lego.tar.xz':
    ensure       => present,
    extract      => true,
    extract_path => $path,
    source       => $lego_binary_url,
    group        => $owner,
    cleanup      => true,
    creates      => $bin,
    require      => Package[$bot_service::packages::packages]
  }

  file { $bin:
    ensure  => link,
    target  => "${path}/lego_linux_amd64",
    owner   => $owner,
    group   => $owner,
    mode    => '0777',
    require => Archive['/tmp/lego.tar.xz']
  }

  file { $config_path:
    ensure  => directory,
    owner   => $owner,
    group   => $owner,
    mode    => '0755',
    require => File[$bin]
  }

  file { $webroot_path:
    ensure => directory,
    owner  => $owner,
    group  => $owner,
    mode   => '0755'
  }

  cron { "recreate webroot_path_on_reboot":
    command => "mkdir -p ${webroot_path}",
    special => 'reboot'
  }
}