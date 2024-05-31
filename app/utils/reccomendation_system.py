import os
import pickle
import asyncio
from datetime import datetime, timedelta
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
import numpy as np

# Подключение к MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client.your_database_name  # Замените 'your_database_name' на название вашей базы данных

MODEL_PATH = 'models/'  # Директория для хранения моделей

# Создание директории для хранения моделей, если она не существует
os.makedirs(MODEL_PATH, exist_ok=True)


# Загрузка данных из MongoDB в DataFrame
async def load_data():
    user_actions = await db.UserActions.find({"action_type": "Like"}).to_list(length=None)
    user_data = pd.DataFrame(user_actions, columns=["user_id", "video_id", "action_type"])
    return user_data


# Обработка данных для библиотеки Surprise
def prepare_data(data):
    reader = Reader(rating_scale=(1, 1))  # Поскольку у нас бинарные лайки, рейтинг 1 означает лайк
    dataset = Dataset.load_from_df(data[['user_id', 'video_id', 'action_type']], reader)
    return dataset


# Обучение модели
def train_model(dataset):
    trainset, testset = train_test_split(dataset, test_size=0.25)
    algo = SVD()
    algo.fit(trainset)
    return algo


# Сохранение модели в файл
def save_model(model, user_id):
    with open(os.path.join(MODEL_PATH, f'{user_id}_model.pkl'), 'wb') as f:
        pickle.dump(model, f)


# Загрузка модели из файла
def load_model(user_id):
    try:
        with open(os.path.join(MODEL_PATH, f'{user_id}_model.pkl'), 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None


# Получение рекомендаций для пользователя
async def get_recommendations(user_id, algo, n=10):
    all_videos = await db.Laps.find().to_list(length=None)
    video_ids = [video['video_id'] for video in all_videos]

    user = await db.Users.find_one({"user_id": user_id})
    watched_videos = set(user.get('liked_videos', [])) | set(user.get('authored_videos', []))
    watched_videos |= set(action['video_id'] for action in
                          await db.UserActions.find({"user_id": user_id, "action_type": "View"}).to_list(length=None))

    candidates = [vid for vid in video_ids if vid not in watched_videos]

    predictions = [algo.predict(user_id, vid) for vid in candidates]
    predictions.sort(key=lambda x: x.est, reverse=True)

    top_n = predictions[:n]

    return [pred.iid for pred in top_n]


# Гибридная фильтрация
async def hybrid_recommendations(user_id, algo, top_n=10):
    cf_recommendations = await get_recommendations(user_id, algo, top_n * 2)

    user = await db.Users.find_one({"user_id": user_id})
    blacklist_tags = set(user.get("blacklist_tags", []))
    blacklist_authors = set(user.get("blacklist_authors", []))

    filtered_recommendations = []
    for video_id in cf_recommendations:
        video = await db.Laps.find_one({"video_id": video_id})
        if not (set(video["tags"]) & blacklist_tags) and video["author_id"] not in blacklist_authors:
            filtered_recommendations.append(video)

    filtered_recommendations.sort(key=lambda x: (x["posted_date"], x["view_count"]), reverse=True)

    return filtered_recommendations[:top_n]


# Основная функция для получения рекомендаций
async def recommend_videolist(user, n=10):
    user_id = user['user_id']

    data = await load_data()
    if data[data['user_id'] == user_id].empty:
        # Новый пользователь, используем контентную фильтрацию
        popular_videos = await db.Laps.find().sort([("view_count", -1)]).to_list(length=n)
        return popular_videos

    model = load_model(user_id)
    if not model:
        dataset = prepare_data(data)
        model = train_model(dataset)
        save_model(model, user_id)

    recommendations = await hybrid_recommendations(user_id, model, n)

    return recommendations


# Функция для периодического обновления модели каждые 3 дня
async def update_models():
    data = await load_data()
    if data.empty:
        return

    dataset = prepare_data(data)
    all_users = await db.Users.find().to_list(length=None)
    for user in all_users:
        user_id = user['user_id']
        user_data = data[data['user_id'] == user_id]
        if len(user_data) < 5:
            continue

        model = train_model(dataset)
        save_model(model, user_id)
