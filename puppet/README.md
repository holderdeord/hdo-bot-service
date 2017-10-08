## Install
    sudo apt install ruby-bundler
    bundle install
    # Install puppet modules
    librarian-puppet install  # --verbose if problems

## Development with docker
    # Build development image
    docker build . -t puppet

    # Start container
    export PATH_TO_APP=/home/nikolark/dev/hdo-bot-service/
    docker run -d -v "$PATH_TO_APP:/app" -v "${PATH_TO_APP}puppet/keys/:/etc/puppetlabs/puppet/eyaml/" -p 2222:22 -h hdo-bot-service puppet

    # Install your public key
    ssh-copy-id root@localhost -p 2222  # password is root

    # Run puppet
    fab docker deploy

    # SSH into container
    ssh root@localhost -p 2222
