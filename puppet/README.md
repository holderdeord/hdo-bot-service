## Install
    sudo apt install ruby-bundler
    bundle install
    # Install puppet modules
    librarian-puppet install  # --verbose if problems

## Development with docker
    # Build development image
    docker built . -t puppet

    # Start container
    PATH_TO_APP=/home/nikolark/dev/hdo-quiz-service/
    docker run -d -v "$PATH_TO_APP:/app" -p 2222:22 -h hdo-bot-service puppet

    # Install your public key
    ssh-copy-id root@localhost -p 2222  # password is root

    # Run puppet
    fab docker puppet_apply

    # SSH into container
    ssh root@localhost -p 2222
