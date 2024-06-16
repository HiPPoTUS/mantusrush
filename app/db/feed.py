from sqlalchemy.orm import sessionmaker
from app.db.utils import to_common
import data_parser.main as parser
from app.db.migrations import Ship, Port, engine, Route


def feed_ships():
    df = parser.schedule()
    df_breaker = parser.ice_breakers()

    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    # Преобразование данных из DataFrame в объекты модели Ship
    ships = []
    names = set()
    for index, row in df.iterrows():
        if row['Название судна'] in names:
            continue

        iceClass = row['Ледовый класс'].replace('Arc ', '')
        iceClass = int(iceClass) if iceClass != 'Нет' else 0
        ship = Ship(
            name=row['Название судна'],
            type='tmp',
            description='tmp',
            max_speed=row['Скорость, узлы\n(по чистой воде)'],
            ice_class=iceClass
        )

        ships.append(ship)
        names.add(row['Название судна'])
    for index, row in df_breaker.iterrows():
        ship = Ship(
            name=row['Наименование'],
            type='tmp',
            description='tmp',
            max_speed=row['Скорость, узлы\n(по чистой воде)'],
            ice_class=9
        )

        ships.append(ship)
        names.add(row['Наименование'])

    # Добавление объектов в сессию и фиксация изменений
    try:
        session.add_all(ships)
        session.commit()
        print("Данные успешно загружены в таблицу ships.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        session.close()


def feed_ports():
    df = parser.nodes()
    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    # Преобразование данных из DataFrame в объекты модели Ship
    ports = []
    for index, row in df.iterrows():
        port = Port(
            name=to_common(row['point_name']),
            coordinates=f'{row["latitude"]} {row["longitude"]}'
        )
        ports.append(port)

    port = Port(
        name=to_common("any"),
        coordinates='0 0'
    )
    ports.append(port)

    # Добавление объектов в сессию и фиксация изменений
    try:
        session.add_all(ports)
        session.commit()
        print("Данные успешно загружены в таблицу ports.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        session.close()


def feed_route():
    df = parser.schedule()
    df_breaker = parser.ice_breakers()
    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    # Преобразование данных из DataFrame в объекты модели Ship
    routes = []
    for index, row in df.iterrows():
        # print(row['Название судна'], row['Пункт начала плавания'], row['Пункт окончания плавания'])

        ship_id = session.query(Ship).filter(Ship.name == row['Название судна']).first().ship_id
        start_point = session.query(Port).filter(
            Port.name.like(f'%{to_common(row["Пункт начала плавания"])}%')
        ).first().port_id
        end_point = session.query(Port).filter(
            Port.name.like(f'%{to_common(row["Пункт окончания плавания"])}%')
        ).first().port_id
        route = Route(
            ship_id=ship_id,
            start_point=start_point,
            end_point=end_point,
            start_time=row['Дата начала плавания']
        )
        routes.append(route)

    for index, row in df_breaker.iterrows():
        ship_id = session.query(Ship).filter(Ship.name == row['Наименование']).first().ship_id
        start_point = session.query(Port).filter(
            Port.name.like(f'%{to_common(row["Начальное положение"])}%')
        ).first().port_id
        end_point = session.query(Port).filter(
            Port.name == 'any'
        ).first().port_id
        route = Route(
            ship_id=ship_id,
            start_point=start_point,
            end_point=end_point,
            start_time='2022-03-01 00:00:00'
        )
        routes.append(route)

    # Добавление объектов в сессию и фиксация изменений
    try:
        session.add_all(routes)
        session.commit()
        print("Данные успешно загружены в таблицу route.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    feed_ports()
    feed_ships()
    feed_route()
