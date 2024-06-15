from datetime import datetime

import pandas as pd
from pathlib import Path

path = '/home/vladimir/Desktop/Tmp/mantusrush/raw_data'
path = Path(path)


def schedule() -> pd.DataFrame:
    table = pd.read_excel(path / Path('Расписание движения судов.xlsx'), sheet_name='Лист1', header=0, nrows=42, skiprows=0)
    # table_1.columns = [
    # 'Название судна',
    # 'Ледовый класс',
    # 'Скорость,
    # узлы(по чистой воде)',
    # 'Пункт начала плавания',
    # 'Пункт окончания плавания',
    # 'Дата начала плавания']
    return table


def ice_breakers() -> pd.DataFrame:
    table = pd.DataFrame({
        "Наименование": ["50 лет Победы", "Ямал", "Таймыр", "Вайгач"],
        "Скорость, узлы\n(по чистой воде)": [22, 21, 18.5, 18.5],
        "Ледовый класс": ["Arc 9", "Arc 9", "Arc 9", "Arc 9"],
        "Начальное положение": [
            "Пролив Лонга",
            "Рейд Мурманска",
            "Мыс Желания",
            "Победа месторождение"]
    })
    return table


def nodes() -> pd.DataFrame:
    table = pd.read_excel(path / Path('ГрафДанные.xlsx'), sheet_name='points', header=0, nrows=47,
                          skiprows=0, usecols="A,B,C,D,E")
    return table


def edges() -> pd.DataFrame:
    table = pd.read_excel(path / Path('ГрафДанные.xlsx'), sheet_name='edges', header=0, nrows=74,
                          skiprows=0, usecols="A,B,C,D,E,F")

    return table


def integr_velocity() -> (pd.DataFrame, pd.DataFrame, list[pd.DataFrame]):
    iv_path = path / Path('IntegrVelocity.xlsx')

    lon = pd.read_excel(iv_path, sheet_name='lon', header=None, nrows=269,
                        skiprows=0)

    lat = pd.read_excel(iv_path, sheet_name='lat', header=None, nrows=269,
                        skiprows=0)

    xl = pd.ExcelFile(iv_path)
    dfs = []
    dates = []

    date_format = '%d-%b-%Y'

    for sheet_name in xl.sheet_names[2:4]:
        df = pd.read_excel(iv_path, sheet_name=sheet_name, header=None, nrows=269,
                           skiprows=0)
        print(datetime.strptime(sheet_name, date_format))
        date = datetime.strptime(sheet_name, date_format).timestamp()
        dfs.append(df)
        dates.append(date)

    return lon, lat, dfs, dates

