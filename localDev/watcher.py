import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from data_store import DataStore

class TransactionHandler(FileSystemEventHandler):
    def __init__(self, data_store):
        self.data_store = data_store

    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        if filepath.endswith('.csv'):
            self.data_store.load_transaction_file(filepath)

def start_watching(transaction_dir, data_store):
    event_handler = TransactionHandler(data_store)
    observer = Observer()
    observer.schedule(event_handler, transaction_dir, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
