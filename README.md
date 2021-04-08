
# This project created to grab maps and skins from osu!lazer (UwU).

### _maybe a bad beatmap!!!_

DB - _**client.db**_ (sqlite3)

Skin and Beatmap files located in `` <osu path>/files ``

## How to a grab

## Grab Beatmap

`` BeatmapSetInfo `` -> mapID

`` BaetmapSetFileIfon `` + mapID -> fileID's

`` FileInfo `` + fileID's -> list of file's and file name's

pack all to .osz archive

## Grab Skin

`` SkinInfo ``-> skinID

`` SkinFileInfo `` + skinID -> fileID's

`` FileInfo `` + fileID's -> list of file's and file name's

pack all to .osk archive

## Default Path

for Linux:
    `` <home>/.local/share/osu ``

for Windows:
    `` Haven`t installed yet. ``

for Mac:
    `` Say me please, I don`t think. ``