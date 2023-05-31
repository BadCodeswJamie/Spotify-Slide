from os.path import exists, join, dirname, realpath
from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

# make sure main playlist is at the end
playlists= {'tempPlaylist': 'YourPlaylistID', 'holdingPlaylist': 'YourPlaylistID', 'mainPlaylist': 'YourPlaylistID'}
                #temp Songs | Short Snake | Worm on String

userId= 'YourUserID'
currentSong= {'name': 'none', 'id': 'none', 'origin': False}

def getSp(Id):
    scope = ['user-library-read', 'playlist-read-private', 'user-library-modify', 'user-read-currently-playing', 'playlist-modify-private', 'playlist-modify-public']
    def get_keys(): # returns client id, client secret
        accessLoc= join(dirname(realpath(__file__)),'Spotify-Access.txt')
        if not exists(accessLoc):
            cid=input('File %s does not exist\nInput client id: ' % accessLoc)

        else:
            with open(accessLoc,'r',encoding= 'utf-8') as keys:
                keys= keys.readlines()
                cid= keys[0].replace('\n','')
                secret= keys[1]
        return cid , secret
    
    cid, secret= get_keys()
    print('getting Sp')
    
    try:
        auth= SpotifyOAuth(scope=scope,client_id=cid, client_secret=secret,redirect_uri= 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcS1voCPUYTtXj3TlsWOrJVAzHNh1gP0c59mFXE7Ke29HmlkYZzavHNlXxmdHNHMpD7cKPLVeVigv5TFr78', username= Id, show_dialog=True)#, username= my_id
        sp = spotipy.Spotify(client_credentials_manager=auth)
        test= sp.current_user_playlists(limit=1)
        print('got authentication')
    except:
        print('Auth failed')
        return False
    return sp

def updateCurrentSong():
    global currentSong
    results= sp.current_user_playing_track()
    try:
        tempCurrentSong= currentSong
        tempCurrentSong['name']= results['item']['name']+ ' - '+ results['item']['artists'][0]['name']
        tempCurrentSong['id']= results['item']['id']
        tempCurrentSong['origin']= results['context']['uri'].split(':')[-1]
        currentSong= tempCurrentSong
        window.changeColour('green')
        window.changeStatusMsg('Updated Song')
    except:
        print('Failed to Update Song')
        window.changeStatusMsg('Failed to Update Song')
        window.changeColour('red')

def remFromPlaylist(songId, playlistId):
    try:
        sp.user_playlist_remove_all_occurrences_of_tracks(user= userId, playlist_id= playlistId, tracks= [songId])
        print('Success')
    except:
        print('Failed')
        window.changeStatusMsg('Failed to remove song')
        window.changeColour('red')
        return False
    window.changeStatusMsg('Removed song from playlist')
    window.changeColour('green')
    

def findPlaylistTypeFromId(playlistId):
    return list(playlists.keys())[list(playlists.values()).index(playlistId)]

def needToDelete():
    if currentSong['origin'] in list(playlists.values())[:-1]:
        print('removing from', findPlaylistTypeFromId(currentSong['origin']))
        remFromPlaylist(currentSong['id'], currentSong['origin'])

def moveToPlaylist(playlist):
    print('adding to', playlist)
    try:
        sp.user_playlist_add_tracks(user= userId, playlist_id= playlists[playlist], tracks= [currentSong['id']])
        print('Success')
    except:
        print('Failed')
        window.changeColour('red')
        window.changeStatusMsg('Failed to add Song')
        return False
    window.changeStatusMsg('Song Added')
    window.changeColour('green')
    needToDelete()



class gui(QWidget):

    def __init__(self):
        super(gui, self).__init__()
        # QApplication.font()
        # self.resize(150,150)
        self.bgColour= 'none'
        self.layout= QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        
        self.currentSong= QLabel(currentSong['name'])
        self.currentSong.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.currentSong)

        hLayout1= QHBoxLayout()

        button1= QPushButton("Main")
        button1.clicked.connect(lambda event : moveToPlaylist('mainPlaylist'))
        hLayout1.addWidget(button1)

        button2= QPushButton("Holding")
        button2.clicked.connect(lambda event : moveToPlaylist('holdingPlaylist'))
        hLayout1.addWidget(button2)

        button3= QPushButton("Temp")
        button3.clicked.connect(lambda event : moveToPlaylist('tempPlaylist'))
        hLayout1.addWidget(button3)

        self.layout.addLayout(hLayout1)

        self.statusMsg= ['None']
        self.status= QLabel('')
        self.status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status)
        
        self.setLayout(self.layout)
        self.setWindowTitle("none")
        
        self.startUpdate()
        self.show()

    def changeColour(self, colour):
        if colour != self.bgColour:
            colours= {'red':'#fa6666', 'green': '#a1fc95', 'yellow': '#fcfca4'}
            colour= colours[colour]
            window.setStyleSheet('background-color: %s' % colour)

    def changeTextBoxMsg(self, string,object):
        object.setText(string)

    def changeStatusMsg(self, string):
        if not string == self.statusMsg[-1]:
            self.statusMsg.append(string)
            self.statusMsg= self.statusMsg[-3:]
            self.changeTextBoxMsg('\n'.join(self.statusMsg), self.status)

    def changeSongMsg(self):
        self.changeTextBoxMsg(currentSong['name'], self.currentSong)

    def startUpdate(self):
        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)


        self.thread.started.connect(self.worker.run)
        self.worker.checked.connect(self.changeSongMsg)

        self.thread.start()


class Worker(QObject):
    checked = pyqtSignal()
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        while True:
            updateCurrentSong()
            self.checked.emit()
            sleep(5)



# on Start
if __name__ == '__main__':
    sp= getSp(userId)
    app = QApplication([])
    window = gui()
    window.show()
    app.exec()
