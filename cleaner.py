import time
import os
import json
import shutil
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
import datetime


desktop_main_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
texts_dir = os.path.join(desktop_main_dir, 'text_files')

#directories for the cleaner folders
desktop_main_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
texts_dir = os.path.join(desktop_main_dir, 'text_files')
image_dir = os.path.join(desktop_main_dir, 'image_files')
audio_dir = os.path.join(desktop_main_dir, 'audio_files')
video_dir = os.path.join(desktop_main_dir, 'video_files')
compressed_dir = os.path.join(desktop_main_dir, 'compressed_files')
data_dir = os.path.join(desktop_main_dir, 'data_files')

#downloads
downloads_main_dir = os.path.join(os.path.expanduser('~'), 'Downloads')


track_dir = input("would you like to clean the downloads folder or desktop?")

def correspondence_check(track_opt):
    main_dir = None
    try:
        os.mkdir(texts_dir)
        os.mkdir(image_dir)
        os.mkdir(audio_dir)
        os.mkdir(video_dir)
        os.mkdir(compressed_dir)
        os.mkdir(data_dir)
        print("Folders:  %s\t \nsuccesfully created" % texts_dir, image_dir, audio_dir, video_dir, compressed_dir, data_dir)

        if track_opt in ["downloads", "downloads folder", "downloaded", "downloaded folder", "download", "downloaded files"]:
            main_dir = downloads_main_dir
        elif track_opt in ["desktop", "DESKTOP","Desktop" , "desktop folder"]:
            main_dir = desktop_main_dir
        else:
            print("Main directory not recognized.")

    except FileExistsError:
        print("Folders:  %s\t \nalready exists" % texts_dir, image_dir, audio_dir, video_dir, compressed_dir, data_dir)
    except FileNotFoundError:
        print("Folder cannot be created check username")
    except Exception as e:
        print("Unknown error occured: ",e)
    
    return main_dir

#function for creating the year/month folder
def create_yr_mn(destination):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    yr_mn_folder = f"{year}_{month}"

    year_month_folder = os.path.join(destination, yr_mn_folder)

    if not os.path.exists(year_month_folder):
        os.mkdir(year_month_folder)

    return year_month_folder


#function for moving the files:
def move_to(destination, file, name):

    yr_mn_dir = create_yr_mn(destination)

    file_exists = os.path.isfile(os.path.join(yr_mn_dir, new_name))  #checking if file of the same name exists
    if file_exists:
        i = 0
        while file_exists:
            i+=1
            current_name, ext = os.path.splitext(name)
            new_name = f"{current_name}_{i}{ext}"

            file_exists = os.path.isfile(os.path.join(yr_mn_dir, new_name))
        name = new_name

        os.rename(file, os.path.join(yr_mn_dir, new_name))
    
    shutil.move(file, os.path.join(yr_mn_dir, name)) #move(file,destination)


main_dir = correspondence_check(track_dir)

#scandir returns list of all the files in selected folder
   
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
      with os.scandir(main_dir) as all_files:
          for file in all_files:
              name = file.name
              destination = main_dir

              if name.endswith(('.txt', '.doc', '.docx', '.rtf', '.msg', '.pdf', '.asc', '.wpd', '.wps')):
                  destination = texts_dir
                  move_to(destination, file,name)

              elif name.endswith(('.jpg', '.jpeg', '.png', '.ai', '.psd', '.gif', '.tiff', '.svg', '.webp')):
                  destination = image_dir
                  move_to(destination, file, name)
              
              elif name.endswith(('.mp3', '.wav', '.wma', '.midi', '.aac', '.aiff', '.flac')) or "SFX" in name:
                  destination = audio_dir
                  move_to(destination, file, name)
              
              elif name.endswith(('.mp4', '.avi', '.webm', '.mov', '.wmv', '.mpeg')):   
                  destination = video_dir
                  move_to(destination, file, name)
              
              elif name.endswith(('.zip', '.rar', '.7z', '.z', '.pkg', '.deb')):   
                  destination = compressed_dir
                  move_to(destination, file, name)
              
              elif name.endswith(('.csv', '.dat', '.db', '.dbf', '.log', '.xml','.json', '.sql', '.sav')):   
                  destination = data_dir
                  move_to(destination, file, name)

              
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = main_dir  #directory we track
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.stop()
        observer.join()