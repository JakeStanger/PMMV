from plugins.base.utils import auth_request
from .models import *
from .scanner import *
from .watcher import *


def init():
    import plugin_loader
    import settings
    import os

    settings.register_key('plugins.base.music.enable', True)
    settings.register_key('plugins.base.music.path', os.path.expanduser('~/Music'))

    if settings.get_key('plugins.base.music.enable'):
        plugin_loader.add_api_endpoints(Artist, ['GET'], exclude=['tracks', 'albums'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Album, ['GET'], exclude=['tracks'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Track, ['GET'], exclude=['playlists'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Genre, ['GET'], exclude=['albums'], auth_func=auth_request)
        plugin_loader.add_api_endpoints(Playlist, ['GET'], auth_func=auth_request)

        watch_music()
