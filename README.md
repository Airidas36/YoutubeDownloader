# YoutubeDownloader

Simple tool for downloading music from Youtube.

Options to download whole playlist or a single video.

All your downloaded files are converted to your desired format (.mp3, .ogg, .wav) and stored in folders named by the playlist you've downloaded.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
pip install -r requirements.txt
```
## Selecting output format
The **default** output format is **.mp3** with **320Kbps** bitrate

Pass one of the following **(ogg, wav)** as an argument to change the output format
```bash
python downloader.py wav
```
Leaving the arguments list blank, will default to **.mp3**
```bash
python downloader.py
```
