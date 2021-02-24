#!/usr/bin/env python3
from pytube import YouTube
from pytube import Stream
from pytube import Playlist
from pydub import AudioSegment
import os
import shutil
import glob
import re

def menu():
    while(True):
        choice = input("Select your options:\n1. Download songs from a playlist\n2. Download a single song\n")
        choice = int(choice)
        if(choice == 1):
            downloadPlaylist()
            break
        elif(choice == 2):
            downloadSong()
            break
        else:
            print("No such option.")

def downloadSong():
    root = os.getcwd()
    path = root + '/' + 'Single_Songs' #Path to folder, where single downloads are stored
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.mkdir(path)
        os.chdir(path)
    video = input("Paste your link here:\n")
    video = YouTube(video)
    download(video)
    convert_playlist()
    os.chdir(root)

def downloadPlaylist():
    root = os.getcwd()
    playlist = input("Paste your link here:\n")
    playlist = Playlist(playlist)
    new_folder = root + '/' + playlist.title #Create folder for particular playlist
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder) #Overwrite if exists
    os.mkdir(new_folder)
    os.chdir(new_folder)
    for video in playlist.videos:
        download(video)
    convert_playlist()
    os.chdir(root)

def download(video):
    try:
        bitrate = re.search('\w*kbps', str(video.streams.filter(only_audio=True).order_by("abr").desc().first())).group(0) #Extract average bitrate from stream
        if bitrate:
            print("Average bitrate for " + video.title +" is " + bitrate)
        stream = video.streams.filter(only_audio=True).order_by("abr").desc().first() #Sort streams by average bitrate, pick the highest
        stream.download()
    except Exception as e:
        print("----------" + video.title + " could not be downloaded.")
        print(e)
    else:
        print(video.title + " downloaded.")

def convert_to_mp3(file):
    mp3_filename = re.subn('(\.mp4|\.webm)$', '.mp3', file) #Replace .mp4 or.webm with .mp3
    if mp3_filename[1] > 0: #If replacement was made, try to convert
        try:
            print("Trying to convert " + mp3_filename[0])
            AudioSegment.from_file(file).export(mp3_filename[0], format='mp3', bitrate="320k")
        except Exception as e:
            print(e)
        else:
            print("Successfully converted " + mp3_filename[0])
            remove_old(file)

def remove_old(file): #Removing the .mp4/.webm after conversion to .mp3
    if os.path.exists(file):
        try:
            os.remove(file)
        except:
            print("Failed to remove the old version of " + file)

def convert_playlist():
    extension_list = ('*.mp4', '*.webm')
    for extension in extension_list: #Recursively iterate through folder and check for files with .mp4 and .webm extensions
        for file in glob.glob(extension):
            convert_to_mp3(file)

def main():
    menu()

if __name__ == "__main__":
    main()
