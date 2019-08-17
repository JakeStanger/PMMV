import datetime
import time

from flask import render_template
from flask_login import login_required

from plugins.webui_static.routes import ui
from plugins.base.music.models import Artist, Album, Track
import database


@ui.route('/music/artists')
@login_required
def artists():
    artist_list = database.db.session.query(Artist).all()

    render_data = [{'name': artist.name,
                    'count': len(artist.albums),
                    'id': artist.id,
                    'name_sort': artist.name_sort}
                   for artist in artist_list if len(artist.albums) > 0]
    render_data.sort(key=lambda artist: artist['name_sort'])

    return render_template('table.html',
                           headers=['name', 'count'],
                           data=render_data,
                           title='Artists',
                           link='ui_static.albums')


@ui.route('/music/artists/<int:key>')
def albums(key: int):
    album_list = database.db.session.query(Album).filter(Album.artist.has(id=key)).all()

    render_data = [{'name': album.name,
                    'released': album.release_date,
                    'count': len(album.tracks),
                    'id': album.id}
                   for album in album_list if len(album.tracks) > 0]

    render_data.sort(key=lambda album: album['released'] or datetime.date.fromtimestamp(-9999999999))

    return render_template('table.html',
                           headers=['name', 'released', 'count'],
                           data=render_data,
                           title='Albums',
                           link='ui_static.tracks')


@ui.route('/music/albums/<int:key>')
def tracks(key: int):
    track_list = database.db.session.query(Track).filter(Track.album.has(id=key)).all()

    render_data = [{
        'name': track.name,
        'duration': time.strftime('%M:%S', time.gmtime(track.duration)),
        'track_num': track.track_num if type(track.track_num) == int else int(track.track_num.split('/')[0]) if track.track_num else 0,
        'disc_num': track.disc_num if type(track.disc_num) == int else int(track.disc_num.split('/')[0]) if track.disc_num else 1,
        'disc_name': track.disc_name
    }
        for track in track_list]

    render_data.sort(key=lambda track: (track['disc_num'], track['track_num']))

    return render_template('table.html',
                           headers=['name', 'duration', 'track_num', 'disc_num'],
                           data=render_data,
                           title='Tracks')
