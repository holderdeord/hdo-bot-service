from fabric.context_managers import cd
from fabric.operations import local as lrun, sudo
from fabric.state import env

env.hosts = ['hdo-bot-service.nkweb.no']
env.puppet_path = '/home/nikolark/hdo-quiz-service'


def deploy():
    lrun('git push heroku master')
    lrun('heroku run python manage.py migrate')


def puppet_apply():
    with cd(env.puppet_path):
        lrun('git pull --ff-only')
        sudo('./puppet/scripts/run-apply.sh')
