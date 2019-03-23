# SC
[![Build Status](https://travis-ci.org/danieloconell/sc.svg?branch=master)](https://travis-ci.org/danieloconell/sc)

> Simple tool to download songs from SoundCloud.

### Why?
  - To listen to favourite songs off-line
  - I like to listen to :musical_note:

### Installation
`pip3 install git+https://github.com/danieloconell/sc`

### Usage:
```
sc, download songs from SoundCloud.

Usage:
    sc <username> likes
    sc <username> tracks
    sc <username> playlists
    sc <url>

Options:
    -h, --help    Show this screen.
    --version     Show version.
```
Download all tracks by a user
```
$ sc coleur tracks
```
A folder called coleur will appear in your current directory with all their
tracks in it.

Download all playlists by a user
```
$ sc coleur playlists
```
Similarly a folder called coleur will appear and in it will be separate
subfolders for each of the user's playlists.
