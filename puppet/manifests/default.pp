node default {
  notice("The host ${hostname} has no node entry")
}

node "hdo-bot-service" {
  include apt
  include timezone

  class { 'unattended_upgrades':
    origins => ['${distro_id}:${distro_codename}',
                '${distro_id}:${distro_codename}-security',
                '${distro_id}:${distro_codename}-updates',
                '${distro_id}:${distro_codename}-proposed']
  }

  class { 'bot_service':
    domain => 'snakk.holderdeord.no'
  }
}