import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint


# Load env variables
load_dotenv()
DIRECTUS_URL = os.getenv("DIRECTUS_URL")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "money_operations")

HEADERS = {
    "Authorization": f"Bearer {DIRECTUS_TOKEN}",
    "Content-Type": "application/json",
}

# Переименование столбцов
COLUMN_MAP = {
    "Дата операции": "datetime",
    "Номер карты": "card_number",
    "Сумма операции": "ammount",
    "Категория": "category",
    "Описание": "description",
    "Статус": "status",
    "Валюта платежа": "currency",
}


def convert_datetime(value):
    # преобразуем строку в datetime и затем в нужный формат
    try:
        return datetime.strptime(value, "%d.%m.%Y %H:%M:%S").strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
    except Exception as e:
        print(f"❌ Ошибка преобразования даты '{value}': {e}")
        return None


def load_mapping(filepath="configs/mapCategories.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_existing_operations():
    print("📡 Загружаем операции из Directus...")
    response = requests.get(
        f"{DIRECTUS_URL}/items/{COLLECTION_NAME}?limit=-1", headers=HEADERS
    )
    response.raise_for_status()
    data = response.json()["data"]
    return {row["datetime"]: row for row in data}


def map_categories(df, mapping):
    df["category"] = df["category"].map(mapping).fillna(df["category"])
    return df


def update_operation(item_id, payload):
    url = f"{DIRECTUS_URL}/items/{COLLECTION_NAME}/{item_id}"
    pprint(payload)
    response = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()


def create_operation(payload):
    url = f"{DIRECTUS_URL}/items/{COLLECTION_NAME}"
    pprint(payload)
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()


def main():
    print("📥 Загружаем CSV...")
    df = pd.read_csv(
        "input/input.csv",
        sep=";",
        encoding="utf-8",
    )
    df.rename(columns=COLUMN_MAP, inplace=True)

    # Подготовка данных
    df = df[list(COLUMN_MAP.values())]
    df["ammount"] = (
        df["ammount"]
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
        .astype(float)
    )
    df = df.fillna("NULL")

    # 🕓 Преобразование даты
    df["datetime"] = df["datetime"].apply(convert_datetime)

    # 📂 Загрузка маппинга
    mapping = load_mapping()
    df = map_categories(df, mapping)

    # 📡 Загрузка текущих данных из Directus
    existing = fetch_existing_operations()

    # 🔁 Обновление или добавление
    for _, row in df.iterrows():
        dt = row["datetime"]
        if not dt:
            continue
        payload = row.to_dict()
        if dt in existing:
            item_id = existing[dt]["id"]
            print(f"🔄 Обновление {dt}")
            update_operation(item_id, payload)
        else:
            print(f"➕ Добавление {dt}")
            create_operation(payload)


if __name__ == "__main__":
    main()
