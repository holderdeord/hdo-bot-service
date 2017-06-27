define bot_service::letsencrypt::certificate (
  String $method = 'http-01',
  Array $domains = [],
  Integer $renew_min_days = 30,
  Array $services = ['nginx'],
  Integer $http_port = 0  # Random by default
) {

  if( !$method in ['http-01']) {
    fail("method '${method}' not supported.")
  }

  if( empty($domains) ) {
    fail('Need at least domain in $domains')
  }
  $cert_name = $domains[0]

  $domain_params = join($domains, ' -d ')
  $_base_params = "--accept-tos --email ${bot_service::letsencrypt::account} --http :${http_port}"

  $base_params = "${_base_params} --path ${bot_service::letsencrypt::config_path} -d ${domain_params}"

  $renew_params = "--days ${renew_min_days} --reuse-key"
  $certificate_file = "${bot_service::letsencrypt::certificate_path}/${cert_name}.crt"

  $cmds = $services.map |$service| { "/usr/sbin/service ${service} reload" }
  $service_reload_cmds = join($cmds, ' && ')

  $le_certs = $facts['letsencrypt_certificates']
  # Initial run
  if( !has_key($le_certs, $cert_name) or (has_key($le_certs, $cert_name) and sort($le_certs[$cert_name]['domains']) != sort($domains)) ) {
    exec { "lego_run_${cert_name}":
      command => "${bot_service::letsencrypt::bin} ${base_params} run",
    }
  }

  # Renewal
  $certificate_exists_cmd = "/usr/bin/test -f ${certificate_file}"
  cron { "letsencrypt_${cert_name}":
    command => "${certificate_exists_cmd} && ${bot_service::letsencrypt::bin} ${base_params} renew ${renew_params} && ${service_reload_cmds}",
    special => 'weekly'
  }
}
