FROM docker.elastic.co/logstash/logstash:7.9.2

# copy installation script to disable SSL verify
COPY ./install.rb /usr/share/logstash/lib/pluginmanager

RUN bin/logstash-plugin install logstash-codec-protobuf

