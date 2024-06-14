from app.db.migrations import engine, create_schema_if_not_exists, create_tables_if_not_exists
from app.db.feed import feed_ports, feed_ships, feed_route
from app.db.utils import drop_table


def main():
    table_names_to_drop = ['ships', 'ports', 'routes', 'current_routes', 'predicted_routes']
    schema_name_to_drop = 'ship_schema'
    for name in table_names_to_drop:
        drop_table(name, schema_name_to_drop)

    with engine.connect() as connection:
        with connection.begin():
            create_schema_if_not_exists()
            create_tables_if_not_exists()
        print("Схема и таблицы успешно созданы или уже существуют.")

    feed_ports()
    feed_ships()
    feed_route()


if __name__ == "__main__":
    main()
