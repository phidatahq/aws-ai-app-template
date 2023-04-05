from phidata.app.postgres import PostgresDb

from workspace.settings import ws_settings

# -*- Run a postgres database on docker

# Dev postgres: A postgres instance to use for dev data
dev_postgres_app = PostgresDb(
    name=f"postgres-{ws_settings.ws_name}",
    enabled=ws_settings.dev_postgres_enabled,
    db_user=ws_settings.ws_name,
    db_password=ws_settings.ws_name,
    db_schema=ws_settings.ws_name,
    # Connect to this db on port 8315
    container_host_port=8315,
)
