from staticfiles.finders import AppDirectoriesFinder
from staticfiles.storage import LegacyAppMediaStorage

class LegacyAppDirectoriesFinder(AppDirectoriesFinder):
    storage_class = LegacyAppMediaStorage