FROM mcr.microsoft.com/mssql/server:2022-CU12-ubuntu-22.04

USER root

# Create a config directory
RUN mkdir -p /usr/config
WORKDIR /usr/config

# Bundle config source
COPY . /usr/config

# Grant permissions so our scripts can be executable
RUN chmod +x /usr/config/entrypoint_v2.sh
RUN chmod +x /usr/config/configure-db_v2.sh

ENTRYPOINT ["./entrypoint_v2.sh"]