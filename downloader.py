#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work")
'''
Ignoring the runtime warning for ffmpeg lib when script is run on Windows platform
'''
from pytube import YouTube
from pytube import Stream
from pytube import Playlist
from pydub import AudioSegment
import os
import shutil
import glob
import re
import platform
import concurrent.futures
import multiprocessing

def menu():
    while(True):
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input("Select your options:\n1. Download songs from a playlist\n2. Download a single song\n")
        try:
            choice = int(choice)
            if(choice == 1):
                downloadPlaylist()
                break
            elif(choice == 2):
                downloadSong()
                break
            else:
                print("No such option.")
        except Exception:
            print("Unsupported character")

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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, playlist.videos)
    convert_playlist()
    os.chdir(root)

def download(video):
    try:
        bitrate = re.search('\w*kbps', str(video.streams.filter(only_audio=True).order_by("abr").desc().first())).group(0) #Extract average bitrate from stream
        if bitrate:
            print("Average bitrate for " + video.title +" is " + bitrate)
        stream = video.streams.filter(only_audio=True).order_by("abr").desc().first() #Sort streams by average bitrate, pick the highes
        stream.download()
    except Exception as error:
        retry_success = False
        for _ in range(5):
            try:
                print(f'Retrying download of {video.title}')
                stream.download()
            except Exception:
                pass
            else:
                retry_success = True
                break
        if not retry_success:
            print(f'----------- {error}')
            print(f'---------- {video.title} could not be downloaded. Logging to file.\n')
            with open ("error_log.txt", 'a') as log:
                log.write(f'{video.title} - {video.watch_url}\n')
        else:
            print(f'{video.title} downloaded.')
    else:
        print(f'{video.title} downloaded.')

def convert_to_mp3(file):
    mp3_filename = re.subn('(\.mp4|\.webm)$', '.mp3', file) #Replace .mp4 or.webm with .mp3
    if mp3_filename[1] > 0: #If replacement was made, try to convert
        try:
            print(f'Trying to convert {file}')
            AudioSegment.from_file(file).export(mp3_filename[0], format='mp3', bitrate="320k")
        except Exception as e:
            print(e)
        else:
            print(f'Successfully converted {mp3_filename[0]}')
            remove_old(file)

def remove_old(file): #Removing the .mp4/.webm after conversion to .mp3
    if os.path.exists(file):
        try:
            os.remove(file)
        except:
            print(f'Failed to remove the old version of {file}')

def convert_playlist():
    extension_list = ('*.mp4', '*.webm')
    conversion_processes = [] # List of conversion processes that will be joined
    for extension in extension_list: #Recursively iterate through folder and check for files with .mp4 and .webm extensions
        for file in glob.glob(extension):
            process = multiprocessing.Process(target = convert_to_mp3, args = [file]) # Creating a process
            conversion_processes.append(process)
            process.start()
    for process in conversion_processes:
        process.join() # Joining the processes

def main():
    sys_type = platform.system()
    if sys_type == "Windows": #Check for Windows system
        app_path = os.path.join(os.getcwd(), 'ffmpeg\\bin')
        os.environ["PATH"] += os.pathsep + app_path #Add ffmpeg lib to PATH for this proccess
    menu()

if __name__ == "__main__":
    main()
