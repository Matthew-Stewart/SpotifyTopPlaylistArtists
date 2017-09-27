from apiInfo import *
import sys
import spotipy
import spotipy.util as util
import re
from collections import Counter
from pprint import pprint

scope = 'user-library-read'

if len(sys.argv) == 3:
   user = sys.argv[1]
   playlist_id = sys.argv[2]
else:
   print "Usage: %s user playlist" % (sys.argv[0],)
   sys.exit()

token = util.prompt_for_user_token(username, scope, Client_ID, Client_Secret, Redirect_URI)

if token:
   sp = spotipy.Spotify(auth=token)
   next = ""
   offset = 0
   all_artists = list()
   while next is not None:
      results = sp.user_playlist_tracks(user, playlist_id, "items(track(name,artists(name))),limit,offset,next", 100, offset)
      next = results['next']
      offset = results['offset'] + results['limit']
      for item in results['items']:
         artists = set()
         track = item['track']
         # find all artist names in the title
         track_title_artists = re.split("\(|\)|\[|\]| - |[Ff]eat\.|[Rr]emix", track['name'])
         if len(track_title_artists) > 1:
            # loop through potential artist names
            for artist in track_title_artists[1:]:
               if artist is not None:
                  filter_words = ['feat.', 'remix', 'radio', 'edit', 'featuring']
                  words = artist.split()
                  result_words  = [word for word in words if word.lower() not in filter_words]
                  result = ' '.join(result_words)
                  # if actual artist
                  if len(result) > 0 and "mix" not in result.lower():
                     if result.find(" & "):
                        possible_artists = result.split(" & ")
                        if len(possible_artists) > 1:
                           artists.update([possible_artists[0]])
                           artists.update([possible_artists[1]])
                     artists.update([result])
         # find all artists from track info
         artists_names = [x['name'] for x in track['artists']]
         # use a set because the artist could be in both the title and artists
         artists.update(artists_names)
         # add found artists to total list
         all_artists.extend(artists)
   if len(all_artists) > 0:
      count = Counter(all_artists)
      # dont reinvent the wheel
      top_artists = count.most_common(25)
      # base spacing off the top artist's count
      padding = len(str(top_artists[0][1])) + 1
      for a in top_artists:
         print "%s %s" % (str(a[1]).ljust(padding), a[0])
else:
   print "Can't get token for", username


