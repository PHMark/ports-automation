# data_pipeline/plugins/helpers/config/postgres/postgres_config.py


class PostgresConfig:
    """Class abstraction for setting up PostgreSQL configuration."""
    def __init__(self, conn_id: str, table: str = '', db: str = ''):
        self.conn_id = conn_id
        self.db = db
        self.table = table
