from pymongo import MongoClient, ASCENDING
from datetime import datetime
from uuid import uuid4
import gridfs

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['tangent_db']

# Настройка GridFS
fs = gridfs.GridFS(db)

# Коллекция Users
# Структура документа в коллекции Users
user_document = {
    "user_id": str(uuid4()),          # Уникальный идентификатор пользователя
    "username": "example_user",       # Имя пользователя
    "lang_code": "en",                # Код языка пользователя ('en' или 'ru')
    "nsfw_enable": False,             # Настройки NSFW (True/False)
    "blacklist_tags": ["tag_id1"],    # Список ID тегов в черном списке
    "blacklist_authors": ["author_id1"],  # Список ID авторов в черном списке
    "telegram_channel_link": "http://t.me/channel",  # Ссылка на Telegram канал пользователя
    "author_nickname": "author_nick",  # Ник автора
    "liked_videos": ["video_id1"],    # Список ID понравившихся видео
    "authored_videos": ["video_id2"],  # Список ID видео, созданных пользователем
    "subscribed_authors": ["author_id2"],  # Список ID подписанных авторов
    "registration_date": datetime.utcnow()  # Дата регистрации пользователя
}

# Коллекция Laps
# Структура документа в коллекции Laps
laps_document = {
    "video_id": str(uuid4()),        # Уникальный идентификатор видео
    "file_id": "file_123",           # Идентификатор файла
    "author_id": "author_id1",       # Уникальный идентификатор автора
    "status": "Posted",              # Статус видео ('Posted', 'On Moderation', 'On Auto-Moderation', 'Deleted')
    "tags": ["tag_id1", "tag_id2"],  # Список ID тегов, прикрепленных к видео
    "description": "Video description",  # Описание видео
    "like_count": 0,                 # Количество лайков
    "view_count": 0,                 # Количество просмотров
    "posted_date": datetime.utcnow()  # Дата публикации видео
}

# Коллекция Moderators
# Структура документа в коллекции Moderators
moderator_document = {
    "moderator_id": str(uuid4()),  # Уникальный идентификатор модератора
    "username": "moderator_user",  # Имя пользователя модератора
    "lang_code": "en"              # Код языка модератора ('en' или 'ru')
}

# Коллекция Tags
# Структура документа в коллекции Tags
tags_document = {
    "tag_id": str(uuid4()),  # Уникальный идентификатор тега
    "tag_name": "example_tag",  # Имя тега
    "video_count": 0            # Количество видео с этим тегом
}

# Коллекция UserActions
# Структура документа в коллекции UserActions
user_action_document = {
    "action_id": str(uuid4()),  # Уникальный идентификатор действия
    "user_id": "user_id1",      # Уникальный идентификатор пользователя
    "action_type": "Like",      # Тип действия ('Post', 'Like', 'View', 'Complaint', 'Approve', 'Reject',
    # 'DeleteVideo', 'BanUser')
    "action_time": datetime.utcnow(),  # Время действия
    "video_id": "video_id1",    # Уникальный идентификатор видео, с которым связано действие
    "reason": "Inappropriate content"  # Причина действия (если применимо)
}

# Создание индексов для всех коллекций
# Индексы для коллекции Users
db.Users.create_index("username", unique=True)  # Индекс для быстрого поиска по имени пользователя
db.Users.create_index("lang_code")  # Индекс для фильтрации по языковым предпочтениям
db.Users.create_index("nsfw_enable")  # Индекс для фильтрации контента по NSFW настройкам
db.Users.create_index("authored_videos")  # Индекс для быстрого доступа к видео, автором которых является пользователь

# Индексы для коллекции Laps
db.Laps.create_index("file_id")  # Индекс для быстрого доступа к файлам
db.Laps.create_index("author_id")  # Индекс для фильтрации видео по автору
db.Laps.create_index("status")  # Индекс для фильтрации видео по статусу
db.Laps.create_index("posted_date")  # Индекс для сортировки и поиска по дате публикации

# Индексы для коллекции Moderators
db.Moderators.create_index("username", unique=True)  # Индекс для быстрого поиска по имени пользователя модератора
db.Moderators.create_index("lang_code")  # Индекс для фильтрации модераторов по языку

# Индексы для коллекции Tags
db.Tags.create_index("tag_name", unique=True)  # Индекс для быстрого поиска по имени тега

# Индексы для коллекции UserActions
db.UserActions.create_index("user_id")  # Индекс для поиска действий по пользователю
db.UserActions.create_index("action_type")  # Индекс для фильтрации по типу действия
db.UserActions.create_index("video_id")  # Индекс для поиска действий, связанных с конкретным видео
