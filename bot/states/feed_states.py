from aiogram.fsm.state import StatesGroup, State

# Состояния для работы с лентой (Feed)
class FeedStates(StatesGroup):
    VIEWING_FEED = State()         # Просмотр текущей ленты
    LOADING_NEW_VIDEOS = State()   # Загрузка новых видео
