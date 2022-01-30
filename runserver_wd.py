import time
import subprocess
from datetime import datetime, timedelta
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler


os.environ["DJANGO_SETTINGS_MODULE"] = "__core__.settings.base"
proc = []


def run_server():
    global proc
    proc = subprocess.Popen(["python", "manage.py", "runserver", "--noreload"])
    print(
        "------------------------ RUNNING RUNSERVER WD ----------------------- PID: ",
        proc.pid,
    )
    return proc


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None):
        super(MyHandler, self).__init__(patterns=patterns)
        self.last_modified = datetime.now()

    def on_modified(self, event):
        global proc
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            print(f"Event type: {event.event_type} path : {event.src_path}")

            if event.src_path.endswith(".py"):
                if proc:
                    proc.kill()
                    print(
                        "---------------------------------------------------------------- KILL PID: ",
                        proc.pid,
                    )
                run_server()

    # def on_modified(self, event):
    # 	global proc
    # 	if datetime.now() - self.last_modified < timedelta(seconds=1):
    # 		self.last_modified = datetime.now()
    # 		# print(f'true')
    # 		print(f'Event type: {event.event_type} path : {event.src_path}')
    # 		if proc:
    # 			proc.kill()
    # 			print('---------------------------------------------------------------- KILL PID: ', proc.pid)
    # 		run_server()
    # 	else:
    # 		self.last_modified = datetime.now()
    # 		# print(f'false')
    # 		print(f'Event type: {event.event_type} path : {event.src_path}')
    # 		if proc:
    # 			proc.kill()
    # 			print('---------------------------------------------------------------- KILL PID: ', proc.pid)
    # 		run_server()


if __name__ == "__main__":
    run_server()
    event_handler = MyHandler(patterns=["*.py"])
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# import sys, os.path, time, logging
# from watchdog.observers import Observer
# from watchdog.events import PatternMatchingEventHandler


# class MyEventHandler(PatternMatchingEventHandler):
#     def on_moved(self, event):
#         super(MyEventHandler, self).on_moved(event)
#         logging.info("File %s was just moved" % event.src_path)

#     def on_created(self, event):
#         super(MyEventHandler, self).on_created(event)
#         logging.info("File %s was just created" % event.src_path)

#     def on_deleted(self, event):
#         super(MyEventHandler, self).on_deleted(event)
#         logging.info("File %s was just deleted" % event.src_path)

#     def on_modified(self, event):
#         super(MyEventHandler, self).on_modified(event)
#         logging.info("File %s was just modified" % event.src_path)

# def main(file_path=None):
#     logging.basicConfig(level=logging.INFO,
#         format='%(asctime)s - %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S')
#     watched_dir = os.path.split(file_path)[0]
#     print 'watched_dir = {watched_dir}'.format(watched_dir=watched_dir)
#     patterns = [file_path]
#     print 'patterns = {patterns}'.format(patterns=', '.join(patterns))
#     event_handler = MyEventHandler(patterns=patterns)
#     observer = Observer()
#     observer.schedule(event_handler, watched_dir, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         path = sys.argv[1]
#         main(file_path=path.strip())
#     else:
#         sys.exit(1)
