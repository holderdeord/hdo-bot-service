node default {
  notice("The host ${hostname} has no node entry")
}

node "hdo-bot-service" {
  class { 'timezone':
    timezone => 'Europe/Oslo',
  }
  include bot_service
}