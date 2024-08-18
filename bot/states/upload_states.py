from aiogram.fsm.state import StatesGroup, State

# Состояния для загрузки видео
class UploadStates(StatesGroup):
    WAITING_FOR_VIDEO = State()            # Ожидание видео
    WAITING_FOR_TAGS = State()             # Ожидание тегов
    WAITING_FOR_MARKS_AND_LINKS = State()  # Ожидание меток и ссылок
    UPLOADING_VIDEO = State()              # Публикация видео
