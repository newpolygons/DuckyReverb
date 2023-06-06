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





import os, wave, requests, spotipy, random, colorgram, tweepy, time
from spotipy.oauth2 import SpotifyClientCredentials
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
from pydub import AudioSegment
from PIL import Image
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip
from requests_oauthlib import OAuth1
from instagrapi import Client


# Chill Pop https://open.spotify.com/playlist/37i9dQZF1DX0MLFaUdXnjA
# phonk https://open.spotify.com/playlist/37i9dQZF1DWWY64wDtewQt
# creamy https://open.spotify.com/playlist/37i9dQZF1DXdgz8ZB7c2CP
#futives https://open.spotify.com/playlist/7rVe8GFBoX8y3UDp0sFq8c?si=7ab0ae1b446a4cfd
#majestic https://open.spotify.com/playlist/6wjCvkAFovrVIRM8VfZLZG?si=540fa1f58a6a4886
def getPlaylistTrack():
    clientCredentialsManager = SpotifyClientCredentials(client_id='', client_secret='')
    sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)

    #SELECT RANDOM PLAYLEST
    playlistList = ['37i9dQZF1DX0MLFaUdXnjA', '37i9dQZF1DWWY64wDtewQt' , '37i9dQZF1DXdgz8ZB7c2CP' , '7rVe8GFBoX8y3UDp0sFq8c', '6wjCvkAFovrVIRM8VfZLZG']
    playlist = random.choice(playlistList)
    tracks = sp.playlist_tracks(playlist, fields='items(track(name,external_urls(spotify)))', limit=50)
    
    
    songList = []
    for i in tracks['items']:
        song = str(i['track']['external_urls']['spotify'])
        songList.append(song)

    link = random.choice(songList)
     
    getSpotify(link)
    


def getSpotify(link):

    #PARSE LINK FURTHER
    if '?' in link:
        stringSplit = link.split('?', 1)
        substring = stringSplit[0]
        link = substring
    
    clientCredentialsManager = SpotifyClientCredentials(client_id='', client_secret='')
    sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)
    
    track = sp.track(link)
    image = track['album']['images'][0]['url']
    name = track['name']


    #Check if song was used before
    with open('names.txt') as file:
        for line in file:
            if line == name:
                getPlaylistTrack()
    file.close()
    #Setup song name for posting and make sure we arnt posting duplicates.
    hs = open('names.txt', "a")
    hs.write(name + "\n")
    hs.close()




    infoList = [ image, name] 
    #create folder for music to sleep 
    newDir = os.getcwd()
    os.system("spotdl " + link + " --output-format wav" + " --output " + newDir)

    for file in os.listdir(newDir):
        if file.endswith(".wav"):
            song = (newDir + "/" + file)
    
    factor = 1.3

    
    #save local copy of image for color extraction
    response = requests.get(image)
    file = open(newDir + '/temp.png', 'wb')
    file.write(response.content)
    file.close()

    

    slowAndReverb(song, factor, newDir)
    


def slowAndReverb(fname, factor, dir):
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
    createVideo()
    
    


def createVideo():
    
    sound = AudioSegment.from_file(os.getcwd() +"/stretched.wav")
    
    #trim audio
    firstCutPoint = (30) * 1000
    lastCutPoint = (1*60) * 1000

    soundclip = sound[firstCutPoint:lastCutPoint]
    soundclip.export((os.getcwd() + "/clippedSound.mp3"), format = "mp3")

    # GET COLORS FROM IMAGE
    colors = colorgram.extract(os.getcwd() + '/temp.png', 2)
    if (len(colors) < 2):
        firstColor = colors[0]
        secondColor = firstColor
    else:
        firstColor = colors[0]
        secondColor = colors[1]

    img1 = Image.new('RGB', (1000, 500), firstColor.rgb)
    img2 = Image.new('RGB', (1000, 500), secondColor.rgb)

    combinedColors = Image.new('RGB', (img1.width, img1.height + img2.height))
    combinedColors.paste(img1, (0,0))
    combinedColors.paste(img2, (0, img1.height))

    #resize album image

    albumImage = Image.open(os.getcwd() + '/temp.png')
    newCover = albumImage.resize((500, 500))

    combinedColors.paste(newCover, (250, 250))
    combinedColors.save(os.getcwd() + "/videoImage.png")

    audioClip = AudioFileClip(os.getcwd() + '/clippedSound.mp3')
    imageClip = ImageClip(os.getcwd() + '/videoImage.png')

    videoClip = imageClip.set_audio(audioClip)
    videoClip.duration = audioClip.duration
    videoClip.fps = 30
    videoClip.write_videofile(os.getcwd() + '/finalVideo.mp4', audio_codec="aac", codec="libx264")

    clip = VideoFileClip(os.getcwd() + "/" + 'finalVideo.mp4')
    clip = clip.subclip(0, 29)
    duration = clip.duration
    clip.write_videofile(os.getcwd() + "/" + "clippedVideo.mp4", audio_codec="aac", codec='libx264')

    postTwitter()





def postTwitter():
    os.system('python3 async-upload.py')
    postInstagram()




def postInstagram():
    with open('names.txt', 'r') as file:
        lastLine = file.readlines()[-1]

    file.close()
    
    
    cl = Client()
    cl.login('', '')

    cl.clip_upload((os.getcwd() + "/" + "clippedVideo.mp4"), (lastLine + '\n . \n . \n . \n #trending #music #audio #reelaudio #duckyReverb #audiosforedits'))

    cleanFolder()

def cleanFolder():
    currentDir = os.getcwd()
    for file in os.listdir(currentDir):
        if file.endswith(".py"):
            pass
        elif file.endswith('.txt'):
            pass
        else:
            os.remove(file)




getPlaylistTrack()