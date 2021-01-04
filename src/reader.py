import mutagen
import eyed3
import os
import csv
import sox
from tinytag import TinyTag as tt
from mutagen.flac import FLAC as flac
from mutagen.aiff import AIFF as aiff
from wavinfo import WavInfoReader as wav


def sox_length(path):
    try:
        length = sox.file_info.duration(path)
        return length
    except:
        return None


def extract(path):
    with open("song_metadata_i.csv", mode="w") as song_metadata:
        writer = csv.writer(song_metadata, delimiter=",",
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["FileName", "Title", "Artist",
                         "Album", "Year", "Genre", "BPM", "BitRate", "Duration", "Size(MB)"])

        for filename in os.listdir(path):
            towrite = []
            towrite.append(filename)
            fullname = os.path.join(path, filename)
            if filename.endswith(".mp3"):
                audiofile = eyed3.load(fullname)
                # print(audiofile)
                # print(audiofile.tag.title)
                towrite.append(str(audiofile.tag.title))
                # print(audiofile.tag.artist)
                towrite.append(str(audiofile.tag.artist))
                # print(audiofile.tag.album)
                towrite.append(str(audiofile.tag.album))
                # print(audiofile.tag.recording_date)
                towrite.append(str(audiofile.tag.recording_date))
                if(str(audiofile.tag.genre) == "None"):
                    # print("None")
                    towrite.append("None")
                else:
                    if(str(audiofile.tag.genre)[0] == "("):
                        towrite.append(str(audiofile.tag.genre)[4:])
                    else:
                        # print(str(audiofile.tag.genre)[4:])
                        towrite.append(str(audiofile.tag.genre))
                # print(audiofile.tag.bpm)
                towrite.append(str(audiofile.tag.bpm))
                # print(audiofile.info.bit_rate[1])
                towrite.append(str(audiofile.info.bit_rate[1]))
            elif filename.endswith(".flac") or filename.endswith(".wma") or filename.endswith(".m4a"):
                audiofile.tag = tt.get(fullname)
                # print(audiofile)
                # print(audiofile.tag.title)
                towrite.append(str(audiofile.tag.title))
                # print(audiofile.tag.artist)
                towrite.append(str(audiofile.tag.artist))
                # print(audiofile.tag.album)
                towrite.append(str(audiofile.tag.album))
                # print(audiofile.tag.year)
                towrite.append(str(audiofile.tag.year))
                # print(audiofile.tag.genre)
                towrite.append(str(audiofile.tag.genre))
                # print(audiofile.tag.bpm)
                towrite.append(str(-1))
                # print(audiofile.tag.bitrate)
                towrite.append(str(audiofile.tag.bitrate))
            elif filename.endswith(".wav"):
                audiofile = wav(fullname)
                # print(audiofile.info)
                # print(audiofile.info.product)
                towrite.append(audiofile.info.product)
                # print(audiofile.info.artist)
                towrite.append(audiofile.info.artist)
                # print(audiofile.info.album)
                towrite.append(audiofile.info.album)
                # print(audiofile.info.created_date)
                towrite.append(audiofile.info.created_date)
                # print(audiofile.info.genre)
                towrite.append(audiofile.info.genre)
                # print(-1)
                towrite.append(str(-1))
                # print(sox.file_info.bitrate(fullname))
                towrite.append(sox.file_info.bitrate(fullname))
            elif filename.endswith(".aiff"):
                audiofile = aiff(fullname)
                # print(audiofile.info.pprint())
                # print(audiofile.tags.pprint())
                # print(audiofile.tags.get("TIT2"))  # title
                # print(audiofile.tags.get("TCON"))  # genre
                # print(audiofile.tags.get("TPE1"))  # artist
                # print(audiofile.tags.get("TALB"))  # album name
                # print(audiofile.tags.get("TPE1"))  # arist name
                # print(audiofile.tags.get("TDRC"))  # release date
                towrite.append(str(audiofile.tags.get("TIT2")))
                towrite.append(str(audiofile.tags.get("TPE1")))
                towrite.append(str(audiofile.tags.get("TALB")))
                towrite.append(str(audiofile.tags.get("TDRC")))
                towrite.append(str(audiofile.tags.get("TCON")))
                towrite.append(str(-1))
                towrite.append(sox.file_info.bitrate(fullname))
            else:
                print("unsupported type!!!")

            length = sox_length(fullname)
            # print(length)
            # print("duration: " + str(int(length/60)) +
            #     ':' + str(int(length % 60)))
            towrite.append(str(int(length/60)) +
                           ':' + str(int(length % 60)))
            towrite.append(float(os.stat(fullname).st_size)/1000000)
            writer.writerow(towrite)

    text = open('song_metadata_i.csv', 'r', encoding="utf-8")
    text = ''.join([i for i in text]).replace('"', "")
    x = open("song_metadata.csv", "w")
    x.writelines(text)
    x.close()
    os.remove("song_metadata_i.csv")


def main():
    extract("example set")


if __name__ == "__main__":
    main()
