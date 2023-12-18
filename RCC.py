import os
import shutil
import tkinter as tk
from tkinter import ttk
from threading import Thread

def cache_clean(logs_directory, progress_var, status_label):
    try:
        log_files = [f for f in os.listdir(logs_directory) if f.endswith(".log")]
        total_files = len(log_files)

        for index, filename in enumerate(log_files):
            file_path = os.path.join(logs_directory, filename)
            os.remove(file_path)
            progress_value = (index + 1) / total_files * 100
            progress_var.set(progress_value)

        temp_roblox_directory = os.path.join(os.environ['temp'], 'Roblox')
        if os.path.exists(temp_roblox_directory):
            total_temp_files = sum([len(files) for _, _, files in os.walk(temp_roblox_directory)])
            progress_var.set(0)
            for root, dirs, files in os.walk(temp_roblox_directory):
                for index, file in enumerate(files):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    temp_progress_value = (index + 1) / total_temp_files * 100
                    progress_var.set(temp_progress_value)
            shutil.rmtree(temp_roblox_directory)
        else:
            pass

        status_label.config(text="Roblox Cache Cleaned!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

root = tk.Tk()
root.title("Roblox Cache Cleaner")

delete_button = tk.Button(root, text="Clear Cache", command=lambda: Thread(target=cache_clean, args=(os.path.expandvars(r"%localappdata%\Roblox\logs"), progress_var, status_label)).start())
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=290, mode="determinate")
status_label = tk.Label(root, text="")

delete_button.pack(pady=10)
progress_bar.pack(pady=10)
status_label.pack()

root.mainloop()
