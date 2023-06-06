"""
Copyright (c) 2023 NewPolygons.

This file is part of DuckyReverb.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import time, wave, contextlib, os, spotipy, eyed3, colorgram, requests
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
from django.conf import settings
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment
from PIL import Image

def parseLink(link):
    parsed_uri = urlparse(link)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    if (result == 'https://open.spotify.com/'):
        goodLink = getSpotify(link)
        data = slowAndReverb(goodLink[0], goodLink[1], goodLink[2], goodLink[3], goodLink[4], goodLink[5])
        return data
    elif (result == 'https://www.youtube.com/'  or result == 'https://youtu.be/'):
        goodLink = getYoutube(link)
        data = slowAndReverb(goodLink[0], goodLink[1], goodLink[2], goodLink[3], goodLink[4], goodLink[5])
        return data
    elif (result == 'https://soundcloud.com/' or result == 'https://m.soundcloud.com/'):
        goodLink = getSoundcloud(link)
        data = slowAndReverb(goodLink[0], goodLink[1], goodLink[2], goodLink[3], goodLink[4], goodLink[5])
        return data

    else:
        return

def tiktok():
    pass

def getSpotify(link):
    link = checkParameters(link)
    speed = 2
    # Spotify Image

    clientCredentialsManager = SpotifyClientCredentials(client_id='', client_secret='')
    sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)
    
    track = sp.track(link)
    image = track['album']['images'][0]['url']
    name = track['name']
    infoList = [ image, name]
    #create folder for music to sleep
    
    dirPath = createFolderName()
    newDir = os.path.join(settings.MEDIA_ROOT, dirPath)
    os.makedirs(newDir)
    
    #fuck new spotdl
    os.system("spotdl " + link + " --format mp3" + " --output " + newDir)

    #find mp3
    for file in os.listdir(newDir):
        if file.endswith('.mp3'):
            mp3Song = (newDir + '/' + file)

    
    
    #convert mp3 to wav for processing
    sound = AudioSegment.from_mp3(mp3Song)
    sound.export(mp3Song, format='wav')
    
    os.rename(mp3Song, newDir + '/' + 'stretched.wav')


    for file in os.listdir(newDir):
        if file.endswith(".wav"):
            song = (newDir + "/" + file)
            

    
    
    factor = (float(speed) / 10) + 1.0


    #save local copy of image for color extraction
    response = requests.get(image)
    file = open(newDir + '/temp.png', 'wb')
    file.write(response.content)
    file.close()

    colors = getImageColors(newDir + '/temp.png')
    print(colors)
    length = checkLengthOfAudio(song)
    if length:
        return song, factor, newDir, dirPath ,infoList, colors

def getYoutube(link):

    #create fix for playlists
    speed = 1
    dirPath = createFolderName()
    newDir = os.path.join(settings.MEDIA_ROOT, dirPath)
    os.makedirs(newDir)

    duration = 1
    ytPath = newDir + "/'%(title)s.%(ext)s'"
    if duration < 721:
        os.system("yt-dlp -f bestaudio --extract-audio --audio-format wav --write-thumbnail --output " + ytPath + " " + link)
    
        for file in os.listdir(newDir):
            if file.endswith(".wav"):
                title = os.path.basename(newDir + "/" + file)
                song = (newDir + "/" + file)
            if file.endswith(".webp"):
                image = Image.open(newDir + "/"  + file).convert("RGB")
                image.save(newDir + "/" + file + ".png", "png")
        
        for file in os.listdir(newDir):
            if file.endswith(".png"):
                image = (newDir + "/" + file)

        
        factor = (float(speed) / 10) + 1.0

        
        infoList = [image, title]

        colors = getImageColors(image)


        return song, factor, newDir, dirPath, infoList, colors

def getSoundcloud(link, speed):
    
    link = checkParameters(link)

    #move this code into its own function
    dirPath = createFolderName()
    newDir = os.path.join(settings.MEDIA_ROOT, dirPath)
    os.makedirs(newDir)

    os.system('scdl -l ' + link + " --path " + newDir + " --onlymp3 --original-art")

    #find mp3
    for file in os.listdir(newDir):
        if file.endswith('.mp3'):
            mp3Song = (newDir + '/' + file)

    

    #GET ARTWORK FROM MP3 FILE

    audioFile = eyed3.load(mp3Song)
    albumName = audioFile.tag.album
    trackName = audioFile.tag.title
    artistName = audioFile.tag.artist
    for image in audioFile.tag.images:
        imageFile = open(mp3Song + "{0} - {1}({2}).jpg".format(artistName, albumName, image.picture_type), "wb")
        imageFile.write(image.image_data)
        imageFile.close()


    
    songDir = (mp3Song + 'song.wav')
    
    
    #convert mp3 to wav for processing
    sound = AudioSegment.from_mp3(mp3Song)
    sound.export(songDir, format='wav')

    #GET NAME OF IMAGE FILE
    for file in os.listdir(newDir):
            if file.endswith(".jpg"):
                os.rename(newDir + '/' + file, newDir + '/' + 'temp.jpg')
                imageName = ('media/' + dirPath + "/" + 'temp.jpg')
                im1 = Image.open(imageName)
                im1.save(imageName[:-3] + "png")
                os.remove(imageName)
                imageName = ('media/' + dirPath + "/" + 'temp.png')
    
    
    
    infoList = [imageName, trackName]
    
    
    #GET NAME OF SONG FILE
    for file in os.listdir(newDir):
            if file.endswith(".wav"):
                song = (newDir + "/" + file)

    factor = (float(speed) / 10) + 1.0

    colors = getImageColors(imageName)

    length = checkLengthOfAudio(song)
    if length:
        return song, factor, newDir, dirPath , infoList, colors
    
def cleanupFiles(path):
    #Function To Remove Original Media
    for file in os.listdir(path):
        if (file.endswith('.wav')) or (file.endswith('.mp3')):
            if file != 'stretched.wav':
                os.remove(path + '/' + file)
                


    


def slowAndReverb(fname, factor, dir, justEND, infoList, colors):
    ''' Shoutout  Manarabdelaty for stretch imp 
        https://github.com/Manarabdelaty/Audio-Stretching'''
    infile=wave.open( fname, 'rb')
    rate= infile.getframerate()
    channels=infile.getnchannels()
    swidth=infile.getsampwidth()
    nframes= infile.getnframes()
    audio_signal= infile.readframes(nframes)
    outfile = wave.open(dir + "/" 'stretched.wav', 'wb')
    outfile.setnchannels(channels)
    outfile.setsampwidth(swidth)
    outfile.setframerate(rate/factor)
    outfile.writeframes(audio_signal)
    outfile.close()
    
    with AudioFile(dir + '/stretched.wav', 'r') as f:
        audio = f.read(f.frames)
        samplerate = f.samplerate

    board = Pedalboard([Reverb()])
    
    effected = board(audio, samplerate)
    with AudioFile(dir + "/stretched.wav", 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)

    slowSong = dir + '/stretched.wav'
    print("DIRECT" + dir)
    cleanupFiles(dir)
    return slowSong, dir , justEND, infoList, colors

    
def checkParameters(link):
    #PARSE LINK FURTHER
    if '?' in link:
        stringSplit = link.split('?', 1)
        substring = stringSplit[0]
        link = substring
    return link

    

def createFolderName():
    return str(round(time.time() * 1000))

def getWorkingDirectory():
    return os.getcwd()


def checkLengthOfAudio(song):
    with contextlib.closing(wave.open(song, 'r')) as f:
        frame = f.getnframes()
        rate = f.getframerate()
        duration = frame / float(rate)

        if (duration > 720):
            return False
        else:
            return True



def getImageColors(image):
    colors  = colorgram.extract(image, 1)
    color = colors[0]
    rbg = color.rgb
    print("RGB: " + str(rbg))
    
    
    return  rbg
    

