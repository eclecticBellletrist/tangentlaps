from aiogram.fsm.state import StatesGroup, State

# Состояния для работы с настройками
class SettingsStates(StatesGroup):
    VIEWING_SETTINGS = State()             # Просмотр настроек
    EDITING_NSFW = State()                 # Настройка NSFW-mode
    EDITING_BLACKLIST_TAGS = State()       # Редактирование черного списка тегов
    EDITING_BLACKLIST_AUTHORS = State()    # Редактирование черного списка авторов
    EDITING_CONTENT_TYPE = State()         # Настройка типов контента
