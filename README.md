# Spotify-Slide

Small(and slightly unstable) program that allows the user to move songs between playlists with one click,
rather than the multiple that spotify requires. 
(at least 2(more if you have playlist folders) to move song and two to delete song saving 3 clicks)

Can move Songs directly into playlists without deleting from source if there is no source playlist e.g. from play queue
Can delete songs from he 3 main playlists.

Has a fail safe that if song doesn't move to destination it does not delete song from source playlist.

Program alerts when a fault has occcured:
- unable to find currently playing song
- Failed to move/delete song

Description of playlists(for me but this is only an example to explain how/why the code works as it does)
  I probably use spotify weirdly but the Three playlists in the code are:
  - tempPlaylist
      These are songs i have never listened to and if i like them i place them into the holdingPlaylist and if not i delete them
  - holdingPlaylist
      Songs i have listened to a couple of times and i'm still deciding if they are good enough for the main
  - mainPlaylist
      I definitely like these song and have listened to them quite a lot and never want to get rid of
      
  Therefore the desired flow is to
  - move song from temp to holding(or main if i really like the song)
  - delete song from temp
  - move song from holding to main
  - delete song from main
  normally this would take at least 8 clicks but just 2 with program
  
Misc notes:
- When moving songs between playlists this program only deletes songs from the temp and holding playlists
- Program does not check if song is already in destination playlist
- this is a m.v.p. and i am not good at coding so don't expect much

Requrements:
- Needs PyQt5 and spotipy python modules
- Windows OS (i am using 11 but i don't see why it woudnt work on 7 and up)
- Spotify premium account so you can create apps
- Spotify Client Id and Secret to be placed in the Spotify-Access.txt file
  (https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- This Url as your redirect Uri(https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcS1voCPUYTtXj3TlsWOrJVAzHNh1gP0c59mFXE7Ke29HmlkYZzavHNlXxmdHNHMpD7cKPLVeVigv5TFr78)
  (yes it has to be that exact one do not change it in the code (●'◡'●) )
- Three playlists ids pasted in the Playlists dictionary (line 10 of main code)
  
