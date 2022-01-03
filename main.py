import os
import glob
import eyed3
import json
import shutil
from tinytag import TinyTag
from time import sleep
from tkinter import Tk, filedialog

# This is because Python is just annoying at times
true = True

# A local db to store all the directories (basically like a config)
db = {
    'output_root': '',
    'artists': []
}


def write_to_db(data: str):
    open('./.mp3sortdb', 'w').write(data)


def read_db_content() -> str:
    return open('./.mp3sortdb', 'r').read()


def load_db():
    db_content = read_db_content()

    if db_content.startswith('{'):
        db = json.loads(db_content)
    elif db_content.startswith(''):
        db['artists'] = []
    else:
        print("DB file empty or modified incorrectly!")


def new_artist(output_dir: str, artist: str):
    print(f"New artist found! Creating new folder for {artist}...")
    os.mkdir(f"{output_dir}/{artist}")
    print(f"Folder created at {output_dir}/{artist}")
    db['artists'].append(artist)
    write_to_db(json.dumps(db))

    return 0


def main():
    print("A dialog will popup asking where do you want this program to scan for audio files")
    input("Press [Enter] to trigger popup")
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    scan_dir = filedialog.askdirectory()
    file_locations = []
    output_dir = None

    print("Scanning through " + scan_dir + "...")

    print()
    print("Scanning for mp3 files...")
    mp3_files = glob.glob(scan_dir + "/**/*.mp3", recursive=True)
    print(f"Found {len(mp3_files)} mp3 files! ")

    print()
    print("Scanning for m4a files...")
    m4a_files = glob.glob(scan_dir + "/**/*.m4a", recursive=True)
    print(f"Found {len(m4a_files)} mp4a files!")

    file_locations = mp3_files + m4a_files

    if db['output_root'] == '':
        print("A dialog will popup asking where to output all the sorted music...")
        input("Press [Enter] to trigger popup")
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        output_dir = filedialog.askdirectory()
        db['output_root'] = output_dir
    else:
        output_dir = db['output_root']

    for file_location in file_locations:
        audio = TinyTag.get(file_location)
        # print(audio.artist)

        if audio.artist in [None, '']:
            if 'noartistdir' in db.keys() or not os.path.isdir(output_dir + '/noartisttag'):
                db['noartistdir'] = True
                os.mkdir(output_dir + '/noartisttag')
                write_to_db(json.dumps(db))

            shutil.copy2(file_location, output_dir + '/noartisttag')
            print(f'No artist tag found for {audio.title}! Copied to {output_dir}/noartisttag')
            continue
        
        if not audio.artist in db['artists']:
            new_artist(output_dir, audio.artist)

        print(f"Artist tag found: {audio.artist} | Copying to {output_dir}/{audio.artist}")
        shutil.copy2(file_location, output_dir + '/' + audio.artist)



if __name__ == "__main__":
    # look for config file
    load_db()

    main()

