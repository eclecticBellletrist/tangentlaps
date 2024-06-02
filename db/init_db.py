import datetime
import gridfs
from uuid import uuid4

from pymongo import MongoClient


def init_database(database):
    # region Создание коллекций
    user_collection = database['Users']  # Коллекция Users
    user_document = {
        "user_id": str(uuid4()),  # Уникальный идентификатор пользователя
        "username": "example_user",  # Имя пользователя
        "lang_code": "en",  # Код языка пользователя ('en' или 'ru')
        "nsfw_enable": False,  # Настройки NSFW (True/False)
        "blacklist_tags": ["tag_id1"],  # Список ID тегов в черном списке
        "blacklist_authors": ["author_id1"],  # Список ID авторов в черном списке
        "telegram_channel_link": "https://t.me/channel",  # Ссылка на Telegram канал пользователя
        "author_nickname": "author_nick",  # Ник автора
        "liked_videos": ["video_id1"],  # Список ID понравившихся видео
        "authored_videos": ["video_id2"],  # Список ID видео, созданных пользователем
        "subscribed_authors": ["author_id2"],  # Список ID подписанных авторов
        "registration_date": datetime.datetime.utcnow()  # Дата регистрации пользователя
    }
    user_collection.insert_one(user_document)

    laps_collection = database['Laps']  # Коллекция Laps
    laps_document = {
        "video_id": str(uuid4()),
        "file_id": "file_123",  # Для доступа к файлу через API Telegram
        "author_id": "author_id1",
        "status": "Posted",  # ('Posted', 'On Moderation', 'On Auto-Moderation', 'Deleted')
        "tags": ["tag_id1", "tag_id2"],
        "description": "Video description",
        "like_count": 0,
        "view_count": 0,
        "posted_date": datetime.datetime.utcnow()
    }
    laps_collection.insert_one(laps_document)

    mods_collection = database['Moderators']  # Коллекция Moderators
    moderator_document = {
        "moderator_id": str(uuid4()),  # Уникальный идентификатор модератора
        "username": "moderator_user",  # Имя пользователя модератора
        "lang_code": "en"  # Код языка модератора ('en' или 'ru')
    }
    mods_collection.insert_one(moderator_document)

    tags_collection = database['Tags']  # Коллекция Tags
    tags_document = {
        "tag_id": str(uuid4()),  # Уникальный идентификатор тега
        "tag_name": "example_tag",  # Имя тега
        "video_count": 0  # Количество видео с этим тегом
    }
    tags_collection.insert_one(tags_document)

    tags_collection = database['UserActions']  # Коллекция UserActions
    user_action_document = {
        "action_id": str(uuid4()),
        "user_id": "user_id1",
        "action_type": "Like",  # ('Post', 'Like', 'View', 'Complaint',
        # 'Approve', 'Reject', 'DeleteVideo', 'BanUser')
        "action_time": datetime.datetime.utcnow(),
        "video_id": "video_id1",
        "reason": "Inappropriate content"  # Причина действия (если применимо)
    }
    tags_collection.insert_one(user_action_document)
    # endregion

    # region Создание индексов для коллекций
    # Индексы для Users
    database.Users.create_index("username", unique=True)
    database.Users.create_index("lang_code")
    database.Users.create_index("nsfw_enable")
    database.Users.create_index("authored_videos")

    # Индексы для коллекции Laps
    database.Laps.create_index("file_id")
    database.Laps.create_index("author_id")
    database.Laps.create_index("status")
    database.Laps.create_index("posted_date")

    # Индексы для коллекции Moderators
    database.Moderators.create_index("username", unique=True)
    database.Moderators.create_index("lang_code")

    # Индексы для коллекции Tags
    database.Tags.create_index("tag_name", unique=True)

    # Индексы для коллекции UserActions
    database.UserActions.create_index("user_id")
    database.UserActions.create_index("action_type")
    database.UserActions.create_index("video_id")
    # endregion


def main():  #TODO Заменить print() на Logging, добавить документацию
    client = MongoClient("mongodb://mongodb:27017/")  # Подключение к MongoDB
    db = client['tangent_db']
    fs = gridfs.GridFS(db)  # Настройка GridFS

    if db.list_collection_names():
        print("Database already contains data.")
    # Проверяем, есть ли уже какие-то данные
    else:
        init_database(db)  # Если коллекция пуста, инициализируем базу данных
        print("Database initialized.")
