node default {
  notice("The host ${hostname} has no node entry")
}

node "hdo-bot-service" {
  include apt

  class { 'timezone':
    timezone => 'Europe/Oslo',
  }

  class { 'unattended_upgrades':
    origins => ['${distro_id}:${distro_codename}',
                '${distro_id}:${distro_codename}-security',
                '${distro_id}:${distro_codename}-updates',
                '${distro_id}:${distro_codename}-proposed']
  }

  include bot_service
}