# SC
[![Build Status](https://travis-ci.org/danieloconell/sc.svg?branch=master)](https://travis-ci.org/danieloconell/sc)

> Simple tool to download songs from SoundCloud.

### Why?
  - To listen to favourite songs off-line
  - I like to listen to :musical_note:
  - This was designed to be as simple as possible, this is why it is only 23kb

### Installation
`pip3 install git+https://github.com/danieloconell/sc`

### Usage:
```
usage: sc [-h] [--likes USER] [--tracks USER] [--playlists USER]
          [--search QUERY [QUERY ...]] [--url URL]

sc, download songs from SoundCloud.

optional arguments:
  -h, --help            show this help message and exit
  --likes USER, -l USER
  --tracks USER, -t USER
  --playlists USER, -p USER
  --search QUERY [QUERY ...], -s QUERY [QUERY ...]
  --url URL, -u URL
```

#### Download all tracks by a user
```
$ sc --tracks coleur
```
A folder called coleur will appear in your current directory with all their
tracks in it.

#### Download all playlists by a user
```
$ sc --playlists coleur
```
Similarly a folder called coleur will appear and in it will be separate
subfolders for each of the user's playlists.

#### Download a song by title
```
$ sc --search awesome song
```
The first 10 results will show up along with an index next to them
```
0: My God is Awesome - Charles Jenkins, Gone Ni Vanua Balavu
1: Everything Is AWESOME!!! - Tegan And Sara feat. The Lonely Island, WaterTowerMusic
2: Guardians of the Galaxy - Awesome Mix Vol. 1, Secara Stefan
3: Guardians Of The Galaxy - Awesome Mix Vol. 2 ( Guardians Of The Galaxy Soundtrack ), Josh
4: Big A feat Shy Glizzy - I'm So Awesome, Big A Cigarellos (H.D)
5: Awesome!, P.SUS
6: Naino Ki Jo Baat Naina Jaane Hai AWESOME SONG MUST WATCH!!(128kbps).M4A, D;j @YaAn.?
7: Awesome (feat. Matt Ox), Valee
8: Charles Jenkins - My God is Awesome, My Christian Walk
9: Onise Iyanu ( God of awesome wonders), Nathaniel Bassey
Enter song index to download: 
```
From here you type the index of the song you wish to download followed by <kbd>Enter</kbd>.
