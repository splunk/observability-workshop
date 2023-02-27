FROM php:8.0-apache
WORKDIR /var/www/html

COPY status.conf /etc/apache2/mods-available/status.conf
COPY index.php index.php
EXPOSE 80

LABEL org.opencontainers.image.source=https://github.com/splunk/observability-workshop
