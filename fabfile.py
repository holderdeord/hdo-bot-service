from fabric.operations import local as lrun

def deploy():
    lrun('git push heroku master')
    lrun('heroku run python manage.py migrate')
