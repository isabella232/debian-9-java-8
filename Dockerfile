FROM maven:3.5.2-jdk-8-slim as defaultjavaapp
MAINTAINER brian.wilkinson@1and1.co.uk
COPY defaultapp /
RUN cd /defaultapp && mvn package

FROM golang as configurability_java8
MAINTAINER brian.wilkinson@1and1.co.uk
WORKDIR /go/src/github.com/1and1internet/configurability
RUN git clone https://github.com/1and1internet/configurability.git . \
       && make java8 \
       && echo "configurability java8 plugin successfully built"

FROM 1and1internet/debian-9
MAINTAINER brian.wilkinson@1and1.co.uk
COPY files/ /
COPY --from=defaultjavaapp /defaultapp/target/defaultapp-1.0-SNAPSHOT-jar-with-dependencies.jar /opt/jarfiles
COPY --from=configurability_java8 /go/src/github.com/1and1internet/configurability/bin/plugins/java8.so /opt/configurability/goplugins
RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
	&& apt-get update \
	&& apt-get install openjdk-8-jre-headless \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& mkdir -p /var/www/ /etc/configurability/custom \
	&& chmod 777 /var/www/ \
	&& chmod +x /usr/local/bin/* \
	&& chmod -R 777 /opt/jarfiles /etc/configurability/custom
WORKDIR /var/www
