from aiogram.fsm.state import StatesGroup, State

# Состояния для работы с аккаунтом пользователя
class UserAccountStates(StatesGroup):
    VIEWING_ACCOUNT = State()          # Просмотр информации о профиле
    VIEWING_SUBSCRIPTIONS = State()    # Просмотр подписок
    VIEWING_LIKES = State()            # Просмотр лайкнутых видео
