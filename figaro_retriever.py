# A class that retrieves all lyrics from an artist from genius.com
# Author: Bo Volwiler
# Last Revision: June 8, 2020


# USAGE:
# Simply initate an instance of the class and the constructor will collect all lyrics automatically.
# Example:
# retriever = LyricRetriever("Pup")
# print(retriever.lyrics)


# Dependencies
from bs4 import BeautifulSoup
import requests
import re

class LyricRetriever:

    # -------- SOUP HELPER FUNCTIONS ---------------
    def decode_content(response,encoding):
        return (response.content.decode(encoding))

    def get_soup_obj(site):
        response = requests.get(site)
        markup = LyricRetriever.decode_content(response, "UTF-8")
        soup = BeautifulSoup(markup, 'html.parser')
        return soup

    # -------- CONSTRUCTOR --------
    def __init__(self, artist):
        self.artist = artist # name of artist
        self.lyrics = None # all artist lyrics
        self.artistPage = ("https://genius.com/artists/" + self.artist) # link to artist page
        self.albums = None # links to all artist albums

        self.get_albums()
        self.get_artist_lyrics()

    # gets all album links from artist page
    #   and assigns the list to self.albums
    def get_albums(self):
        artist_albums = []

        artist_soup = LyricRetriever.get_soup_obj(self.artistPage)

        for link in artist_soup.find_all('a'):
                link_text = link.get('href')
                if link_text[:26] == "https://genius.com/albums/":
                    artist_albums.append(link_text)
                    #TODO: Check for duplicates
                
        artist_albums = list(dict.fromkeys(artist_albums))
        
        self.albums = artist_albums

    # gets all lyrics for an album
    def get_album_lyrics(albumSite):

        site = LyricRetriever.get_soup_obj(albumSite)
        songs = LyricRetriever.get_songs(site)

        lyrics_list = []

        for song in songs:
            song = LyricRetriever.get_soup_obj(song)
            lyrics = LyricRetriever.get_lyrics(song)
            lyrics_list.append(lyrics)
        
        return lyrics_list

    def get_songs(albumSoupObj):

        link_list = []

        for link in albumSoupObj.find_all('a'):
            link_address = link.get('href')
            if link_address[-6:] == "lyrics":
                link_list.append(link_address)
                
        return link_list

    def get_lyrics(songSoupObj):
        song_lyrics = []

        for link in songSoupObj.find_all('p'):
            song_lyrics.append(link.get_text())

        song_lyrics = song_lyrics[0]
        #song_lyrics = song_lyrics.replace("\n", " ")

        return song_lyrics

    def clean_lyrics(lyrics):
        
        # removing all square bracketed words
        lyrics = re.sub("\[[^\]]*\]", "", lyrics)
        
        # removing all slashes
        #lyrics = re.sub("\\\\", "", lyrics)
        #lyrics = lyrics.decode('string_escape')
        lyrics = re.sub("'", "", lyrics) # there are apparently no backslashes, just backslash escaped apostrophes

        lyrics = re.sub("r'[^\x00-\x7f]", r'', lyrics)

        #lyrics = re.sub("")
        
        return lyrics

    def get_artist_lyrics(self):

        lyrics = []

        for x in self.albums:
            lyrics.append(LyricRetriever.get_album_lyrics(x))
            
        all_lyrics = ""

        for x in lyrics:
            for y in x:
                all_lyrics = " ".join([all_lyrics, y])
                
        all_lyrics = LyricRetriever.clean_lyrics(all_lyrics)
            
        self.lyrics = all_lyrics

#retriever = LyricRetriever("Snail Mail")
#print(retriever.lyrics)