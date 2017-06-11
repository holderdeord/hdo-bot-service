from fabric.context_managers import cd
from fabric.operations import local as lrun, sudo, run
from fabric.state import env

env.use_ssh_config = True
env.forward_agent = True
env.hosts = ['hdo-bot-service.nkweb.no']
env.puppet_path = '/home/nikolark/hdo-quiz-service/puppet'
env.docker = False


def docker():
    env.docker = True
    env.hosts = ['localhost:2222']
    env.user = 'root'
    env.puppet_path = '/app/puppet'


def deploy():
    lrun('git push heroku master')
    lrun('heroku run python manage.py migrate')


def puppet_apply():
    with cd(env.puppet_path):
        if not env.docker:
            run('git pull --ff-only')
        sudo('./scripts/run-apply.sh')
