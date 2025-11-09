FROM postgres:17.6

COPY ./db/init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE ${POSTGRES_PORT}
