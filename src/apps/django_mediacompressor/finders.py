from staticfiles.finders import AppDirectoriesFinder
from staticfiles.storage import LegacyAppMediaStorage

# finder for staticfiles which finds mediafile in old-style folders 'media'
class LegacyAppDirectoriesFinder(AppDirectoriesFinder):
    storage_class = LegacyAppMediaStorage