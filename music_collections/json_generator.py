import os
import natsort
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
import json
from shutil import copyfile


rootPath = "./src"


def execSong(album, song, num):
    song_obj = {
        "title": "",
        "artist": "",
        "duration": "",
        "src": ""
    }
    song_path = f"{rootPath}/{album}/{song}"
    track = MP3(song_path)
    tags = ID3(song_path)

    song_obj["src"] = f"{album}_{num}.{song.split('.')[-1]}"

    try:
        os.remove(song_obj["src"])
    except:
        try:
            os.rename(f"{rootPath}/{album}/{song}", f"{rootPath}/{album}/{song_obj['src']}")
        except:
            pass




    # album name
    # track.get("TALB")

    # title name
    # track.get("TIT2")
    song_obj["title"] = str(track.get("TIT2"))
    print(str(track.get("TIT2")))

    # track artist
    # track.get("TPE1")
    song_obj["artist"] = str(track.get("TPE1"))

    # album artist
    # track.get("TPE2")

    # duration
    # track.info.length
    song_obj["duration"] = str(track.info.length)

    # cover img
    imgPath = f"{rootPath}/{album}/imgs/{album}_{num}.png"
    if not os.path.exists(imgPath):
        try:
            pict = tags.getall('APIC')[0].data
            im = Image.open(BytesIO(pict)).resize((50, 50))
            im.save(imgPath)
        except:
            copyfile(f"{rootPath}/{album}/imgs/{getCover(album)}", imgPath)

    return song_obj


def execAlbum(album):
    local_obj = {
        "length": 0,
        "data": []
    }
    num = 0
    songs = os.listdir(rootPath + "/" + album)
    songs = natsort.natsorted(songs)
    for song in songs:
        if (song != 'imgs') & (song != 'data.json'):
            song_obj = execSong(album, song, num)
            local_obj["data"].append(song_obj)
            num += 1
    local_obj["length"] = num
    return local_obj


def getCover(album):
    imgs = os.listdir(f"{rootPath}/{album}/imgs/")
    for img in imgs:
        if img.split('.')[0] == 'cover':
            return img

def getAlbumName(album):
    f = open(f"{rootPath}/{album}/imgs/name", "r", encoding='utf-8')
    return f.readline()

def saveToFile(path, obj):
    # f = open(path ,"w")
    # f.write(json.dumps(obj, ensure_ascii=False))
    with open(path, "w", encoding='utf-8') as jsonfile:
        json.dump(obj, jsonfile, ensure_ascii=False)


if __name__ == "__main__":
    albums_obj = {
        "length": 0,
        "data": []
    }
    num = 0
    albums = os.listdir(rootPath)
    albums = natsort.natsorted(albums)
    for album in albums:
        if (album != 'data.json'):
            imgsPath = f"{rootPath}/{album}/imgs"
            if not os.path.exists(imgsPath):
                os.makedirs(imgsPath)
            local_obj = execAlbum(album)
            saveToFile(f"{rootPath}/{album}/data.json", local_obj)

            album_obj = {
                "id": album,
                "name": getAlbumName(album),
                "image": getCover(album)
            }

            albums_obj["data"].append(album_obj)
            num += 1
    albums_obj["length"] = num
    saveToFile(f"{rootPath}/data.json", albums_obj)
