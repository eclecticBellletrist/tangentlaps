# Импорт всех классов состояний для удобства
from .feed_states import FeedStates
from .user_account_states import UserAccountStates
from .settings_states import SettingsStates
from .upload_states import UploadStates

# Объявление того, что будет импортировано при импорте модуля states
__all__ = ['FeedStates', 'UserAccountStates', 'SettingsStates', 'UploadStates']
