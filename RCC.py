import os
import shutil
import tkinter as tk
from tkinter import ttk
from threading import Thread
import psutil

def is_roblox_running():
    for process in psutil.process_iter(['pid', 'name']):
        if "RobloxPlayerBeta.exe" in process.info['name']:
            return True
    return False

def cache_clean(progress_var, status_label):
    try:
        if is_roblox_running():
            status_label.config(text="Please close Roblox before clearing cache.")
            return

        # Cache Paths so that it's organized
        cache_paths = [
            os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "logs"),
            os.path.join(os.getenv("temp"), "Roblox"),
        ]

        total_directories = len(cache_paths)
        deleted_at_least_one_directory = False

        for index, cache_path in enumerate(cache_paths):
            try:
                if os.path.exists(cache_path):
                    cache_name = os.path.basename(cache_path)
                    # Delete folder so it's faster (It doesn't break roblox, don't worry.)
                    shutil.rmtree(cache_path)
                    progress_value = (index + 1) / total_directories * 100
                    progress_var.set(progress_value)
                    status_label.config(text=f"Deleted {cache_name}")
                    deleted_at_least_one_directory = True
                else:
                    status_label.config(text=f"There are no more Cache on {cache_name}")
            except Exception as e:
                status_label.config(text=f"Error deleting {cache_path}: {e}")

        if deleted_at_least_one_directory:
            status_label.config(text="Roblox Cache Cleaned!")

    except Exception as e:
        status_label.config(text=f"Error: {e}")

root = tk.Tk()
root.title("Roblox Cache Cleaner")

delete_button = tk.Button(root,text="Clear Cache",command=lambda: Thread(target=cache_clean,args=(progress_var, status_label),).start(),)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=290, mode="determinate")
status_label = tk.Label(root, text="")

delete_button.pack(pady=10)
progress_bar.pack(pady=10)
status_label.pack()

root.mainloop()
