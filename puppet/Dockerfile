FROM ubuntu:xenial
MAINTAINER Nikolai R Kristiansen <nikolaik@gmail.com>

# Install puppet, ruby, ssh ++
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install -yqq wget && \
    wget https://apt.puppetlabs.com/puppet5-release-xenial.deb && \
    dpkg -i puppet5-release-xenial.deb && \
    rm puppet5-release-xenial.deb && \
    apt-get update && \
    apt-get install -yqq puppet-agent openssh-server sudo ruby-bundler lsb-release && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
