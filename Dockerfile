FROM python:3.6-alpine

LABEL maintainer="Lyuben Bahtarliev <lyuben.bahtarliev@akat-t.com>"

WORKDIR /opt/malwarescan

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

COPY requirements.txt ./

RUN clear && echo -e "\n[$(date)] Starting... \n" && apk update \
	&& echo -e "\n[$(date)] Processing build dependencies... \n" \
	&& apk -q --no-progress --no-cache add \
	openssl \
        nano \
        sudo \
        git \
        unzip \
        postgresql-libs \
        libxslt \
        supervisor \
        libcap \
        shadow \
	&& addgroup -g 1000 -S malwarescan \
	&& adduser -u 1000 -s /bin/bash -h /opt/malwarescan -S malwarescan -G malwarescan \
	&& chown malwarescan:malwarescan -R /opt/malwarescan

RUN echo -e "\n[$(date)] Processing python dependencies from requirements.txt... \n" \
    && apk -q --no-progress --no-cache add --virtual .build-deps \
	gcc \
	musl-dev \
	libffi-dev \
	libxslt-dev \
	postgresql-dev \
	tzdata \
	zlib-dev \
	&& cp -pfrv /usr/share/zoneinfo/Europe/Sofia /etc/localtime \
	&& echo "Europe/Sofia" > /etc/timezone \
	&& pip -q --no-cache-dir install --no-use-pep517 -r requirements.txt \
	&& apk --purge del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . .

RUN echo -e "\n[$(date)] Installing MalwareScan package... \n" \
    && for i in `ls -1 *.zip`; do unzip -o $i; rm -rfv $i; done \
	&& chown malwarescan:malwarescan -R /opt/malwarescan \
	&& pip -q --no-cache-dir install --no-use-pep517 --editable .\
	&& touch /opt/malwarescan/.firstrun \
    && echo -e "\n[$(date)] Finished!\n"

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "./docker-entrypoint.sh"]
