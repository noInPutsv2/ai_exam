FROM mcr.microsoft.com/mssql/server:2022-CU12-ubuntu-22.04

USER root

# Create a config directory
RUN mkdir -p /usr/config

# Set mssql as owner of the app directory
RUN chown mssql /usr/config

WORKDIR /usr/config

# Bundle config source
COPY . /usr/config

# Grant permissions so our scripts can be executable
RUN chmod +x /usr/config/entrypoint.sh
RUN chmod +x /usr/config/configure-db.sh

ENTRYPOINT ["./entrypoint.sh"]