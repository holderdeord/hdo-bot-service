node default {
  notice("The host ${hostname} has no node entry")
}

node "hdo-bot-service" {
  include timezone
  include bot_service
}