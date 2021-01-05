# helpers/lib/sql_queries.py


class SqlQueries:
    ports_table_insert = """INSERT INTO ports(
        countryName, portName, unlocode, coordinates, staging_id
    )
    VALUES (
        %(countryName)s,
        %(portName)s,
        %(unlocode)s,
        %(coordinates)s,
        %(staging_id)s
    )
    ON CONFLICT (countryName, portName, unlocode, coordinates)
    DO UPDATE SET
        (countryName, portName, unlocode, coordinates, updated_at)
        = (
            EXCLUDED.countryName,
            EXCLUDED.portName,
            EXCLUDED.unlocode,
            EXCLUDED.coordinates,
            '{updated_at}'
        );
    """
    table_row_count = "SELECT COUNT(*) FROM {table}"