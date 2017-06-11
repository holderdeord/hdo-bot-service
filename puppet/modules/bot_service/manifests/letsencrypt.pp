class bot_service::letsencrypt (
  String $account,
  String $lego_binary_url = 'https://nikola.nkweb.no/pub/lego_linux_amd64'
) {

  # Lego
  $bin = '/usr/local/bin/lego'
  $config_path = '/var/lib/lego'
  $certificate_path = "${config_path}/certificates"
  $owner = 'root'
  $webroot_path = '/tmp/letsencrypt'

  file { $bin:
    source => $lego_binary_url,
    owner  => $owner,
    group  => $owner,
    mode   => '0755'
  }

  file { $config_path:
    ensure => directory,
    owner  => $owner,
    group  => $owner,
    mode   => '0755'
  }

  file { $webroot_path:
    ensure => directory,
    owner  => $owner,
    group  => $owner,
    mode   => '0755'
  }

}
