FROM unicon/grouper-demo:2.2.2

MAINTAINER jgasper@unicon.net

ADD /provisioningTargetAttributes.gsh /

RUN set -x \
    && service mysql start \
    && service slapd start \
    && cd /opt/grouper.apiBinary-2.2.2/ \
    && bin/gsh /provisioningTargetAttributes.gsh

EXPOSE 389 3306 8080

CMD ["run-grouper.sh"]
