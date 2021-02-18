FROM debian:10-slim

# Update
RUN apt-get -y update

# Install build tools
RUN apt-get -y install git wget dpkg-dev apt-utils gpg

RUN useradd -ms /bin/bash publisher

COPY publish.sh /opt/publish.sh

WORKDIR /opt/publish

RUN chown -R publisher:publisher /opt/publish

USER publisher
ENTRYPOINT ["/opt/publish.sh"]