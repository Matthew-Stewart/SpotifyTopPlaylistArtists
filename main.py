from apiInfo import *
import sys
import spotipy
import spotipy.util as util
from pprint import pprint

scope = 'user-library-read'

if len(sys.argv) > 2:
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
   while next is not None:
      results = sp.user_playlist_tracks(user, playlist_id, "items(track(name,artists(name))),limit,offset,next", 100, offset)
      next = results['next']
      offset = results['offset'] + results['limit']
      for item in results['items']:
         track = item['track']
         pprint(track['name'] + ' - ' + track['artists'][0]['name'])
else:
   print "Can't get token for", username


