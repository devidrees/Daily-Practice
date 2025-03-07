import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd
from PIL import Image, ImageTk

# Data storage
records = []
last_in_time = None
window_size_index = 0
window_sizes = [(400, 300), (600, 400), (800, 600)]

# File paths
SAVE_FILE = "time_tracker.xlsx"
EXPORT_FILE_BASE = "time_tracker_export"

# Create main application window
root = tk.Tk()
root.title("Time Tracker")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Function to update live timer
def update_live_timer():
    if last_in_time:
        elapsed_time = datetime.now() - last_in_time
        lbl_live_timer.config(text=f"Elapsed: {str(elapsed_time).split('.')[0]}")
        root.after(1000, update_live_timer)

# Function to record IN time
def mark_in():
    global last_in_time
    if last_in_time:
        return
    last_in_time = datetime.now()
    lbl_status.config(text=f"IN: {last_in_time.strftime('%H:%M:%S')}", fg="green")
    btn_in.config(bg="green", fg="white", state="disabled", relief="sunken")
    btn_out.config(state="normal")
    update_live_timer()

# Function to record OUT time
def mark_out():
    global last_in_time
    if not last_in_time:
        return
    time_out = datetime.now()
    total_time = time_out - last_in_time
    records.append({
        "Date": last_in_time.strftime('%Y-%m-%d'),
        "Time In": last_in_time.strftime('%H:%M:%S'),
        "Time Out": time_out.strftime('%H:%M:%S'),
        "Time Spent": str(total_time).split('.')[0]
    })
    lbl_status.config(text=f"OUT: {time_out.strftime('%H:%M:%S')}", fg="blue")
    btn_in.config(bg="#2196F3", fg="black", state="normal", relief="raised")
    btn_out.config(bg="red", fg="white", state="disabled", relief="sunken")
    last_in_time = None

# Function to save data to Excel
def save_data():
    if not records:
        lbl_status.config(text="No data to save!", fg="red")
        return
    df = pd.DataFrame(records)
    if os.path.exists(SAVE_FILE):
        existing_df = pd.read_excel(SAVE_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    total_hours = sum(pd.to_timedelta(df["Time Spent"]).dt.total_seconds()) / 3600
    df.loc[len(df)] = ["TOTAL", "", "", f"{round(total_hours, 2)} hrs"]
    df.to_excel(SAVE_FILE, index=False)
    lbl_status.config(text="Data saved successfully!", fg="blue")

# Function to export data to a new Excel file
def export_data():
    if not records:
        lbl_status.config(text="No data to export!", fg="red")
        return
    export_file = EXPORT_FILE_BASE + ".xlsx"
    counter = 1
    while os.path.exists(export_file):
        export_file = f"{EXPORT_FILE_BASE}_{counter}.xlsx"
        counter += 1
    df = pd.DataFrame(records)
    df.to_excel(export_file, index=False)
    lbl_status.config(text=f"Data exported to {export_file}", fg="blue")

# Function to toggle window size
def toggle_size():
    global window_size_index
    window_size_index = (window_size_index + 1) % len(window_sizes)
    new_size = window_sizes[window_size_index]
    root.geometry(f"{new_size[0]}x{new_size[1]}")

# Resize button
btn_resize = tk.Button(root, text="Resize", command=toggle_size, font=("Arial", 10), bg="#D3D3D3", relief="raised", bd=2)
btn_resize.pack(anchor="ne", padx=10, pady=5)

# UI Elements
frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(fill=tk.X, padx=10, pady=5)

button_style = {
    "font": ("Arial", 14, "bold"),
    "bg": "#2196F3",
    "fg": "black",
    "activebackground": "#1976D2",
    "activeforeground": "white",
    "bd": 5,
    "relief": "raised",
    "highlightthickness": 0,
    "borderwidth": 2,
    "padx": 10,
    "pady": 10,
    "width": 15
}

btn_in = tk.Button(frame_buttons, text="IN", command=mark_in, **button_style)
btn_in.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

btn_out = tk.Button(frame_buttons, text="OUT", command=mark_out, state="disabled", **button_style)
btn_out.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

lbl_live_timer = tk.Label(root, text="Elapsed: 00:00:00", font=("Arial", 10), fg="gray", bg="#f0f0f0")
lbl_live_timer.pack()

btn_save = tk.Button(root, text="Save", command=save_data, **button_style)
btn_save.pack(fill=tk.X, padx=20, pady=5)

btn_export = tk.Button(root, text="Export", command=export_data, **button_style)
btn_export.pack(fill=tk.X, padx=20, pady=5)

lbl_status = tk.Label(root, text="Click IN to Start", font=("Arial", 12), bg="#f0f0f0")
lbl_status.pack(pady=5)

root.mainloop()