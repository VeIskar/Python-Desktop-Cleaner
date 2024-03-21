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
main_dir = f'C:/Users/{your_name}/Desktop'
texts_dir = f'C:/Users/{your_name}/Desktop/text_files'
#later add:downloads


try:
    os.mkdir(texts_dir)
    print("Folder %s succesfully created" % texts_dir)
except FileExistsError:
    print("Folder %s already exists" % texts_dir)
except FileNotFoundError:
   print("Folder cannot be created check username")
 

#function for moving the files:
def move_to(destination, file, name):
    file_exists = os.path.isfile(destination + '/' + name)
    if file_exists:
        i = 0
        while file_exists:
            i+=1
            current_name, ext = os.path.splitext(name)
            new_name = f"{current_name}_{i}{ext}"

            file_exists = os.path.isfile(destination + '/' + new_name)
    
    shutil.move(file, destination)


#scandir returns list of all the files in selected folder
   
class MoveHandler(FileSystmeEventHandler):
    def on_modified(self, event):
      with os.scandir(main_dir) as all_files:
          for file in all_files:
              name = file.name
              destination = main_dir

              if name.endswith(('.txt', '.doc', '.docx', '.rtf', '.msg', '.pdf', '.asc', '.wpd', '.wps')):
                  destination = texts_dir
                  #move function?

              
        

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