import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ImageMaker import start

directory = '/Users/abigailmarks/Downloads/'
def check_imput_path(string):
        if string[-4:]== ".png" or string[-4:]== ".jpg" or string[-5:]== ".jpeg":
            return True
        else:
            return False

class NewFileHandler(FileSystemEventHandler):
    

    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            
            if os.path.exists(filename):
                print(filename)
                file_size = os.path.getsize(filename)
                if check_imput_path(filename):

                    print(f"New file created: {filename}. File size: {file_size} bytes.")
                    if file_size > 10:
                        print("size is more than 10 starting")
                        start(filename)

    
        

event_handler = NewFileHandler()
observer = Observer()
observer.schedule(event_handler, directory, recursive=False)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()