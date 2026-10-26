# PHP 8.5.12 fixes CVE-2026-109618 and CVE-2026-109619. PHP 8.1 and older are EOL.
FROM php:8.5.12-apache@sha256:7cd25eb48f9763dfeabe8fda3939897aca2001802fadeafa1b602f26c735ef96
WORKDIR /var/www/html

COPY status.conf /etc/apache2/mods-available/status.conf
COPY index.php index.php
EXPOSE 80

LABEL org.opencontainers.image.source=https://github.com/splunk/observability-workshop
