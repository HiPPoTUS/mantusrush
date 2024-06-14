from app.db.migrations import *


def drop_table(table_name, schema_name):
    with engine.connect() as connection:
        try:
            connection.execute(text(f"DROP TABLE {schema_name}.{table_name} CASCADE"))
            print(f"Таблица {table_name} в схеме {schema_name} успешно удалена с использованием CASCADE.")
        except Exception as e:
            print(f"Ошибка при удалении таблицы: {e}")

    # metadata = MetaData()
    # metadata.reflect(bind=engine, schema=schema_name)
    # table = metadata.tables.get(f"{schema_name}.{table_name}")
    # if table is not None:
    #     table.drop(engine, checkfirst=True, cascade=True)
    #     print(f"Таблица {table_name} в схеме {schema_name} успешно удалена.")
    # else:
    #     print(f"Таблица {table_name} в схеме {schema_name} не найдена.")


def to_common(string: str) -> str:
    string = string.lower()
    string = string.replace(" - ", " ")
    return string
