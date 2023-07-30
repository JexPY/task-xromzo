FROM nginx:alpine

COPY nginx.conf /etc/nginx/

RUN apk update \
    && apk upgrade \
    && apk --update add logrotate \
    && apk add --no-cache openssl \
    && apk add --no-cache bash

RUN apk add --no-cache curl

# RUN delgroup www-data

# RUN set -x ; \
#     addgroup -g 82 -S www-data ; \
#     adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

RUN set -x ; \
    if ! getent group www-data ; then \
    addgroup -g 82 -S www-data ; \
    fi ; \
    if ! getent passwd www-data ; then \
    adduser -u 82 -D -S -G www-data www-data && exit 0 ; \
    exit 1 ; \
    fi

ARG PYTHON_UPSTREAM_CONTAINER=gapi
ARG PYTHON_UPSTREAM_PORT=3000

# Create 'messages' file used from 'logrotate'
RUN touch /var/log/messages

# Copy 'logrotate' config file
COPY logrotate/nginx /etc/logrotate.d/

# Set upstream conf and remove the default conf
RUN echo "upstream python-upstream { server ${PYTHON_UPSTREAM_CONTAINER}:${PYTHON_UPSTREAM_PORT}; }" > /etc/nginx/conf.d/upstream.conf 
# && rm /etc/nginx/conf.d/default.conf

ADD ./startup.sh /opt/startup.sh
RUN sed -i 's/\r//g' /opt/startup.sh
CMD ["/bin/bash", "/opt/startup.sh"]

EXPOSE 80 81 443
