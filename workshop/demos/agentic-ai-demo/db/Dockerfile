FROM postgres:17.6

# Switch to the 'postgres' user.
# The official postgres image already creates this user with appropriate permissions.
USER postgres

COPY ./db/init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE ${POSTGRES_PORT}
