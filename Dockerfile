FROM python:3.8 AS build

RUN python3 --version
RUN pip3 --version

WORKDIR /app
COPY . /app/
    
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:application"]

# Configuración de new relic
RUN pip3 install newrelic
ENV NEW_RELIC_APP_NAME="blacklist"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTE_TRACING_ENABLED=true
#INTEST_licence
ENV NEW_RELIC_LICENSE_KEY=2069cdfdf0ecd67a452bb3d486544f41c8a4NRAL
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT [ "newrelic-admin", "run-program" ]