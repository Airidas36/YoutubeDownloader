#!/usr/bin/env python3
from pytube import YouTube
from pytube import Stream
from pytube import Playlist

import os
import shutil

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
    path = root + '/' + 'Single_Songs'
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.mkdir(path)
        os.chdir(path)
    video = input("Paste your link here:\n")
    video = YouTube(video)
    try:
        stream = video.streams.filter(only_audio=True).asc().first()
        stream.download()
    except:
        print("------------" + video.title + "Couldn't be downloaded!")
    else:
        print(video.title + " downloaded.")

def downloadPlaylist():
    root = os.getcwd()
    playlist = input("Paste your link here:\n")
    playlist = Playlist(playlist)
    new_folder = root + '/' + playlist.title
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)
    os.mkdir(new_folder)
    os.chdir(new_folder)
    print(os.listdir())
    for video in playlist.videos:
        try:
            stream = video.streams.filter(only_audio=True).asc().first()
            stream.download()
        except:
            print("------------" + video.title + "Couldn't be downloaded!")
        else:
            print(video.title + " downloaded.")
    os.chdir(root)

def main():
    menu()

if __name__ == "__main__":
    main()
