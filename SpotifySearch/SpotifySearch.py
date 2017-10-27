import spotipy, re
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup

class SpotifySearch(object):
    def __init__(self, url):
        self.url = url
        self.main(url)

    def main(self, url):
        client = req(url)
        page_html = client.read()
        client.close()
        page_soup = soup(page_html, "html.parser")
        containers = []

        if page_soup.find('ol'):
           ol = page_soup.find('ol')
           num = 0
           for li in ol.findAll('li'):
               containers.insert(num, li.text)
               num =+ 1
        elif page_soup.find('div', {"class": "list"}):
            div = page_soup.find('div', {"class": "list"})
            num = 0
            for div in div.findAll('div', {"class": "list-track"}):
                containers.insert(num, div.text)
                num =+ 1
        filename = 'SpotifySearch_' + (url.split('com/w/')[1]) + '.txt'
        file = open(filename, 'w')

        client_id = 'YOUR_SPOTIFY_API_CLIENT_ID'
        client_secret = 'YOUR_SPOTIFY_API_CLIENT_SECRET'
        redirect_uri = 'http://localhost:8888/callback'

        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        username = 'YOUR_SPOTIFY_USERNAME'
        scope='playlist-read-private'
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

        if token and containers:
            for container in containers:
                if '] ' in container and '] ?' not in container:
                    title_str = str(container).split('] ')[1]
                    if 'amp;' in title_str:
                        title_str = re.sub('[amp;]', '', title_str)
                    if '[' in title_str:
                        title_str = title_str.split('[')[0]
                    artist_search = title_str.split(' - ')[0].rstrip()
                    track_search = title_str.split(' - ')[1].rstrip()
                    result = sp.search(track_search, limit=1, offset=0, type='track', market=None)
                    if (result['tracks']['items'] and str(result['tracks']['items'][0]['artists'][0]['name']).lower() == artist_search.lower()):
                        artist = result['tracks']['items'][0]['artists'][0]['name']
                        track = result['tracks']['items'][0]['name']
                        file.write(artist + ' - ' + track + '\n')
                    else:
                        file.write('UNIDENTIFIED: ' + title_str.rstrip() + '\n')
            print('Finished search, see results in: ' + filename)
        else:
            print("Can't get token for", username)
