import time
import os
import json
import shutil
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystmeEventHandler
from watchdog.events import LoggingEventHandler

your_name = input("insert your username: ")


#directories for the cleaner folders
desktop_main_dir = f'C:/Users/{your_name}/Desktop'
texts_dir = f'C:/Users/{your_name}/Desktop/text_files'
image_dir = f'C:/Users/{your_name}/Desktop/image_files'
audio_dir = f'C:/Users/{your_name}/Desktop/audio_files'
video_dir = f'C:/Users/{your_name}/Desktop/video_files'
compressed_dir = f'C:/Users/{your_name}/Desktop/compressed_files'
data_dir = f'C:/Users/{your_name}/Desktop/data_files'

#downloads
downloads_main_dir = f'C:/Users/{your_name}/Downloads'

try:
    os.mkdir(texts_dir)
    os.mkdir(image_dir)
    print("Folders %s succesfully created" % texts_dir, image_dir)
except FileExistsError:
    print("Folders %s already exists" % texts_dir, image_dir)
except FileNotFoundError:
   print("Folder cannot be created check username")
except Exception as e:
    print("Unknown error occured: ",e)
 

track_dir = input("would you like to clean the downloads folder or desktop?")
#main_dir = ''
if track_dir in ["downloads", "downloads folder", "downloaded", "downloaded folder", "download", "downloaded fiels"]:
    main_dir = downloads_main_dir

elif track_dir in ["desktop", "Desktop", "DESKTOP"]:
    main_dir = desktop_main_dir

else:
    print("not recognized")


#function for moving the files:
def move_to(destination, file, name):
    file_exists = os.path.isfile(destination + '/' + name)  #checking if file of the same name exists
    if file_exists:
        i = 0
        while file_exists:
            i+=1
            current_name, ext = os.path.splitext(name)
            new_name = f"{current_name}_{i}{ext}"

            file_exists = os.path.isfile(destination + '/' + new_name)
        name = new_name
        os.rename(file,new_name)
    
    shutil.move(file, os.path.join(destination, name)) #move(file,destination)


#scandir returns list of all the files in selected folder
   
class MoveHandler(FileSystmeEventHandler):
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