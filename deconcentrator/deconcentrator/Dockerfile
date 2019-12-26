FROM alpine:3

RUN adduser -h /mnt -G users -D -H -u 1000 default
RUN chown default:users /mnt

RUN apk add --no-cache \
        python3 \
        uwsgi \
        uwsgi-python \
        gettext \
        su-exec \
        postgresql-client \
        py3-psycopg2 \
        tini
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --compile -r /tmp/requirements.txt

RUN mkdir /mnt/deconcentrator
COPY --chown=default:users src /mnt/deconcentrator

USER default
WORKDIR /mnt/deconcentrator
ENV HOME=/mnt

ENTRYPOINT [ "/sbin/tini", "--" ]