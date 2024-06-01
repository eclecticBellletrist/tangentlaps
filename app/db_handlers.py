import gridfs
from pymongo import MongoClient


def get_database():
    """
    Подключение к локальной базе данных MongoDB.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client['tangent_db']  # Замените 'your_database_name' на название вашей базы данных
    return db


def save_model_to_gridfs(db, user_id, file_path):
    """
    Сохранение файла модели в GridFS, ассоциируя его с пользователем.

    :param db: База данных MongoDB.
    :param user_id: Идентификатор пользователя.
    :param file_path: Путь к файлу модели.
    """
    fs = gridfs.GridFS(db)
    with open(file_path, 'rb') as f:
        fs.put(f, filename=f"{user_id}_model")


def get_model_from_gridfs(db, user_id, output_path):
    """
    Извлечение файла модели из GridFS, ассоциированного с пользователем.

    :param db: База данных MongoDB.
    :param user_id: Идентификатор пользователя.
    :param output_path: Путь для сохранения извлеченного файла модели.
    :return: True, если файл успешно извлечен, иначе False.
    """
    fs = gridfs.GridFS(db)
    file_data = fs.find_one({"filename": f"{user_id}_model"})
    if file_data:
        with open(output_path, 'wb') as f:
            f.write(file_data.read())
        return True
    return False

# Пример использования:
# db = get_database()
# save_model_to_gridfs(db, 'user_id_example', 'path/to/your/model/file')
# get_model_from_gridfs(db, 'user_id_example', 'path/to/save/model/file')
