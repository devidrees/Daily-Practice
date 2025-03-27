import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
import time
import pytz  # Add this import for timezone support

# Try to import winsound, but don't fail if it's not available
try:
    import winsound
    SOUND_AVAILABLE = True
    # Define sound constants only if winsound is available
    SOUND_OK = 0x00000000
    SOUND_EXCLAMATION = 0x00000030
    SOUND_WARNING = 0x00000030
    SOUND_INFORMATION = 0x00000040
except ImportError:
    SOUND_AVAILABLE = False
    # Define dummy sound constants
    SOUND_OK = 0
    SOUND_EXCLAMATION = 0
    SOUND_WARNING = 0
    SOUND_INFORMATION = 0

class TimeTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        
        # Initialize variables
        self.time_in = None
        self.time_out = None
        self.is_timing = False
        self.is_paused = False
        self.pause_start = None
        self.total_pause_duration = timedelta()
        self.menu_expanded = False
        self.is_popup_mode = False
        self.is_muted = not SOUND_AVAILABLE  # Muted by default if sound not available
        
        # Sound types for different actions (only if sound is available)
        self.sound_effects = {
            'in': SOUND_OK,
            'out': SOUND_EXCLAMATION,
            'pause': SOUND_WARNING,
            'resume': SOUND_INFORMATION
        }
        
        # Store original window size and position
        self.normal_geometry = "600x450"
        
        # Set fixed window size
        self.root.geometry(self.normal_geometry)
        
        # Theme colors
        self.current_theme_name = "dark"
        self.themes = {
            "light": {
                "name": "☀️ Light",
                "bg": "#FAFAFA",  # Material Light Background
                "fg": "#212121",  # Material Dark Text
                "button": "#6200EE",  # Material Primary
                "button_fg": "#FFFFFF",
                "green": "#00C853",  # Material Green A700
                "red": "#D50000",    # Material Red A700
                "frame_bg": "#FFFFFF",
                "secondary": "#03DAC6",  # Material Secondary
                "surface": "#FFFFFF",
                "error": "#B00020",
                "text_primary": "#212121",
                "text_secondary": "#757575"
            },
            "dark": {
                "name": "🌙 Dark",
                "bg": "#121212",  # Material Dark Background
                "fg": "#FFFFFF",
                "button": "#BB86FC",  # Material Dark Primary
                "button_fg": "#000000",
                "green": "#00E676",  # Material Green A400
                "red": "#FF5252",    # Material Red A200
                "frame_bg": "#1E1E1E",
                "secondary": "#03DAC6",
                "surface": "#1E1E1E",
                "error": "#CF6679",
                "text_primary": "#FFFFFF",
                "text_secondary": "#B3B3B3"
            },
            "dracula": {
                "name": "🧛 Dracula",
                "bg": "#282a36",
                "fg": "#f8f8f2",
                "button": "#bd93f9",
                "button_fg": "#282a36",
                "green": "#50fa7b",
                "red": "#ff5555",
                "frame_bg": "#44475a",
                "text_primary": "#f8f8f2",
                "text_secondary": "#6272a4"
            },
            "nord": {
                "name": "❄️ Nord",
                "bg": "#2e3440",
                "fg": "#eceff4",
                "button": "#5e81ac",
                "button_fg": "#eceff4",
                "green": "#a3be8c",
                "red": "#bf616a",
                "frame_bg": "#3b4252",
                "text_primary": "#eceff4",
                "text_secondary": "#d8dee9"
            },
            "solarized": {
                "name": "🌞 Solarized",
                "bg": "#002b36",
                "fg": "#839496",
                "button": "#268bd2",
                "button_fg": "#fdf6e3",
                "green": "#859900",
                "red": "#dc322f",
                "frame_bg": "#073642",
                "text_primary": "#93a1a1",
                "text_secondary": "#657b83"
            }
        }
        
        # Set initial theme
        self.current_theme = self.themes[self.current_theme_name]
        
        # Configure root
        self.root.configure(bg=self.current_theme["bg"])
        
        # Enable window resizing
        self.root.resizable(True, True)
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create side menu
        self.create_side_menu()
        
        # Create main content
        self.create_main_content()
        
        # Start update loop
        self.update_timer()

    def create_side_menu(self):
        """Create the side menu and its buttons"""
        # Style configuration
        style = ttk.Style()
        style.configure("Material.TFrame",
            background=self.current_theme["frame_bg"],
            relief="flat"
        )
        
        # Side menu frame
        self.side_menu = ttk.Frame(self.root, style="Material.TFrame", padding="10")
        self.side_menu.grid(row=0, column=0, sticky="ns")
        self.side_menu.grid_rowconfigure(5, weight=1)  # Push buttons to top
        
        # Menu toggle button
        self.menu_btn = tk.Button(
            self.side_menu,
            text="☰",
            font=("Segoe UI", 16),
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"],
            relief="flat",
            borderwidth=0,
            command=self.toggle_menu,
            cursor="hand2"
        )
        self.menu_btn.grid(row=0, column=0, pady=(0, 20), sticky="nw")
        
        # Side menu buttons style
        button_style = {
            'font': ("Segoe UI", 11),
            'relief': "flat",
            'borderwidth': 0,
            'padx': 20,
            'pady': 10,
            'cursor': "hand2",
            'bg': "#424242",
            'fg': "#FFFFFF",
            'activebackground': "#616161",
            'activeforeground': "#FFFFFF",
            'anchor': 'w',
            'width': 10
        }
        
        # Side menu buttons
        self.save_btn = tk.Button(
            self.side_menu,
            text="💾 Save",
            command=self.save_data,
            **button_style
        )
        
        self.export_btn = tk.Button(
            self.side_menu,
            text="📤 Export",
            command=self.export_data,
            **button_style
        )
        
        self.history_btn = tk.Button(
            self.side_menu,
            text="📋 History",
            command=self.show_history,
            **button_style
        )
        
        self.about_btn = tk.Button(
            self.side_menu,
            text="ℹ️ About",
            command=self.show_about,
            **button_style
        )
        
        # Add mute button only if sound is available
        if SOUND_AVAILABLE:
            self.mute_btn = tk.Button(
                self.side_menu,
                text="🔊 Sound" if not self.is_muted else "🔇 Muted",
                command=self.toggle_mute,
                **button_style
            )
            # Add mute button to the list of buttons to show/hide
            self.menu_buttons = [self.save_btn, self.export_btn, self.history_btn, self.about_btn, self.mute_btn]
        else:
            self.menu_buttons = [self.save_btn, self.export_btn, self.history_btn, self.about_btn]
        
        # Initially hide the buttons
        self.hide_menu_buttons()

    def create_main_content(self):
        """Create the main content area"""
        # Create btn_frame first as it will be needed for buttons
        self.btn_frame = ttk.Frame(self.root, style="Material.TFrame")
        
        # Mode toggle button (Normal/Popup)
        self.mode_btn = tk.Button(
            self.root,
            text="🗗" if not self.is_popup_mode else "🗖",
            font=("Segoe UI", 10),
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"],
            relief="flat",
            borderwidth=0,
            command=self.toggle_window_mode,
            cursor="hand2",
            width=2
        )
        self.mode_btn.place(relx=1.0, rely=0, anchor="ne")

        # Main content frame
        self.main_frame = ttk.Frame(self.root, padding="10", style="Material.TFrame")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure main frame grid weights
        self.main_frame.grid_rowconfigure(2, weight=3)  # Give more weight to button row
        self.main_frame.grid_rowconfigure(4, weight=0)  # Add row for datetime label
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure("MaterialTimer.TLabel",
            font=("Segoe UI", 36, "bold"),
            foreground=self.current_theme["fg"],
            background=self.current_theme["frame_bg"],
            padding=(0, 20)
        )
        
        style.configure("MaterialStatus.TLabel",
            font=("Segoe UI", 10),
            foreground=self.current_theme["fg"],
            background=self.current_theme["frame_bg"],
            padding=(0, 5)
        )
        
        style.configure("MaterialToggle.TButton",
            font=("Segoe UI", 10),
            padding=5
        )
        
        # Create a frame for the top buttons
        top_buttons_frame = ttk.Frame(self.main_frame, style="Material.TFrame")
        top_buttons_frame.grid(row=0, column=2, sticky="e", padx=10, pady=5)
        
        # Resize button
        self.resize_btn = ttk.Button(
            top_buttons_frame,
            text="🔍",  # Magnifying glass icon
            command=self.toggle_compact_view,
            style="MaterialToggle.TButton"
        )
        self.resize_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Theme toggle button
        self.theme_btn = ttk.Button(
            top_buttons_frame,
            text=self.current_theme["name"],
            command=self.toggle_theme,
            style="MaterialToggle.TButton"
        )
        self.theme_btn.grid(row=0, column=1)
        
        # Timer display
        self.timer_label = ttk.Label(
            self.main_frame,
            text="00:00:00",
            style="MaterialTimer.TLabel"
        )
        self.timer_label.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="n")
        
        # IN/OUT buttons frame
        self.btn_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
        self.btn_frame.grid_rowconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        self.btn_frame.grid_columnconfigure(2, weight=1)
        
        # IN button
        self.in_btn = tk.Button(
            self.btn_frame,
            text="IN",
            command=self.time_in_click,
            font=("Segoe UI", 16, "bold"),
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            relief="flat",
            borderwidth=0,
            padx=40,
            pady=20,
            cursor="hand2"
        )
        self.in_btn.grid(row=0, column=0, padx=10, sticky="nsew")
        
        # Pause button
        self.pause_btn = tk.Button(
            self.btn_frame,
            text="⏸️ PAUSE",
            command=self.pause_click,
            font=("Segoe UI", 16, "bold"),
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            relief="flat",
            borderwidth=0,
            padx=40,
            pady=20,
            cursor="hand2"
        )
        self.pause_btn.grid(row=0, column=1, padx=10, sticky="nsew")
        self.pause_btn.grid_remove()  # Initially hidden
        
        # Resume button
        self.resume_btn = tk.Button(
            self.btn_frame,
            text="▶️ RESUME",
            command=self.resume_click,
            font=("Segoe UI", 16, "bold"),
            bg=self.current_theme["green"],
            fg=self.current_theme["button_fg"],
            relief="flat",
            borderwidth=0,
            padx=40,
            pady=20,
            cursor="hand2"
        )
        self.resume_btn.grid(row=0, column=1, padx=10, sticky="nsew")
        self.resume_btn.grid_remove()  # Initially hidden
        
        # OUT button
        self.out_btn = tk.Button(
            self.btn_frame,
            text="OUT",
            command=self.time_out_click,
            font=("Segoe UI", 16, "bold"),
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            relief="flat",
            borderwidth=0,
            padx=40,
            pady=20,
            cursor="hand2"
        )
        self.out_btn.grid(row=0, column=2, padx=10, sticky="nsew")
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_frame, style="Material.TFrame")
        self.status_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=15)
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        # Status labels
        self.last_out_label = ttk.Label(
            self.status_frame,
            text="Last Time Out: --:--:--",
            style="MaterialStatus.TLabel"
        )
        self.last_out_label.grid(row=0, column=0, pady=2, sticky="n")
        
        self.last_spent_label = ttk.Label(
            self.status_frame,
            text="Last Time Spent: --:--:--",
            style="MaterialStatus.TLabel"
        )
        self.last_spent_label.grid(row=1, column=0, pady=2, sticky="n")
        
        # Add time label at the bottom left
        self.time_label = ttk.Label(
            self.main_frame,
            text="",
            style="MaterialStatus.TLabel",
            padding=(5, 10)
        )
        self.time_label.grid(row=4, column=0, sticky="sw")
        
        # Add date and timezone label at the bottom right
        self.date_tz_label = ttk.Label(
            self.main_frame,
            text="",
            style="MaterialStatus.TLabel",
            padding=(5, 10)
        )
        self.date_tz_label.grid(row=4, column=2, sticky="se")
        
        # Add hover effects
        self._add_button_hover_effects()
        
        # Start datetime update
        self.update_datetime()

    def update_datetime(self):
        """Update the time and date labels"""
        current_time = datetime.now()
        local_tz = current_time.astimezone().tzinfo
        
        # Update time in 12-hour format
        time_text = current_time.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
        self.time_label.configure(text=time_text)
        
        # Update date and timezone
        date_tz_text = f"{current_time.strftime('%Y-%m-%d')} {str(local_tz)}"
        self.date_tz_label.configure(text=date_tz_text)
        
        self.root.after(1000, self.update_datetime)

    def toggle_theme(self):
        # Get list of theme names and find next theme
        theme_names = list(self.themes.keys())
        current_index = theme_names.index(self.current_theme_name)
        next_index = (current_index + 1) % len(theme_names)
        self.current_theme_name = theme_names[next_index]
        self.current_theme = self.themes[self.current_theme_name]
        
        # Update root background
        self.root.configure(bg=self.current_theme["bg"])
        
        # Update theme button text
        self.theme_btn.configure(text=self.current_theme["name"])
        
        # Update mode button colors
        self.mode_btn.configure(
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        
        # Update button colors
        self.in_btn.configure(
            bg=self.current_theme["green"] if self.is_timing else self.current_theme["button"],
            fg=self.current_theme["button_fg"]
        )
        self.out_btn.configure(
            bg=self.current_theme["red"] if not self.is_timing and self.time_out 
            else self.current_theme["button"],
            fg=self.current_theme["button_fg"]
        )
        
        # Update action buttons - keep dark grey regardless of theme
        action_button_style = {
            'bg': "#424242",
            'fg': "#FFFFFF",
            'activebackground': "#616161",
            'activeforeground': "#FFFFFF"
        }
        for btn in [self.save_btn, self.export_btn, self.history_btn]:
            btn.configure(**action_button_style)
        
        # Update labels
        style = ttk.Style()
        style.configure("MaterialTimer.TLabel", 
            foreground=self.current_theme["text_primary"],
            background=self.current_theme["frame_bg"]
        )
        style.configure("MaterialStatus.TLabel", 
            foreground=self.current_theme["text_secondary"],
            background=self.current_theme["frame_bg"]
        )
        
        # Update datetime labels style
        self.time_label.configure(style="MaterialStatus.TLabel")
        self.date_tz_label.configure(style="MaterialStatus.TLabel")
        
        # Update frames
        style.configure("Material.TFrame", background=self.current_theme["frame_bg"])
        
        # Update Treeview style if history window is open
        style.configure("Treeview",
            background=self.current_theme["frame_bg"],
            foreground=self.current_theme["text_primary"],
            fieldbackground=self.current_theme["frame_bg"]
        )
        style.configure("Treeview.Heading",
            background=self.current_theme["frame_bg"],
            foreground=self.current_theme["text_primary"]
        )
        style.map("Treeview",
            background=[("selected", self.current_theme["button"])],
            foreground=[("selected", self.current_theme["button_fg"])]
        )
        
        # Update all frames
        for frame in [self.main_frame, self.status_frame]:  # Removed action_frame reference
            frame.configure(style='Material.TFrame')

    def play_sound(self, sound_type):
        """Play a sound effect if not muted and sound is available"""
        if SOUND_AVAILABLE and not self.is_muted:
            try:
                if sound_type in self.sound_effects:
                    winsound.MessageBeep(self.sound_effects[sound_type])
            except:
                pass  # Silently continue if sound fails

    def toggle_mute(self):
        """Toggle sound mute state"""
        if SOUND_AVAILABLE:
            self.is_muted = not self.is_muted
            if hasattr(self, 'mute_btn'):
                self.mute_btn.configure(text="🔇 Muted" if self.is_muted else "🔊 Sound")

    def time_in_click(self):
        if not self.is_timing:
            self.time_in = datetime.now()
            self.is_timing = True
            self.is_paused = False
            self.total_pause_duration = timedelta()
            self.in_btn.configure(bg=self.current_theme["green"])
            self.out_btn.configure(bg=self.current_theme["button"])
            self.pause_btn.grid()  # Show pause button
            self.play_sound('in')

    def pause_click(self):
        if self.is_timing and not self.is_paused:
            self.is_paused = True
            self.pause_start = datetime.now()
            self.pause_btn.grid_remove()  # Hide pause button
            self.resume_btn.grid()  # Show resume button
            self.play_sound('pause')

    def resume_click(self):
        if self.is_timing and self.is_paused:
            pause_duration = datetime.now() - self.pause_start
            self.total_pause_duration += pause_duration
            self.is_paused = False
            self.pause_start = None
            self.resume_btn.grid_remove()  # Hide resume button
            self.pause_btn.grid()  # Show pause button
            self.play_sound('resume')

    def time_out_click(self):
        if self.is_timing:
            if self.is_paused:
                # If paused, add the current pause duration
                pause_duration = datetime.now() - self.pause_start
                self.total_pause_duration += pause_duration
            
            self.time_out = datetime.now()
            self.is_timing = False
            self.is_paused = False
            self.out_btn.configure(bg=self.current_theme["red"])
            self.in_btn.configure(bg=self.current_theme["button"])
            self.pause_btn.grid_remove()  # Hide pause button
            self.resume_btn.grid_remove()  # Hide resume button
            
            # Update labels
            self.last_out_label.configure(text=f"Last Time Out: {self.time_out.strftime('%H:%M:%S')}")
            duration = self.time_out - self.time_in - self.total_pause_duration
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.last_spent_label.configure(text=f"Last Time Spent: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.play_sound('out')

    def update_timer(self):
        if self.is_timing and self.time_in:
            if not self.is_paused:
                duration = datetime.now() - self.time_in - self.total_pause_duration
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.timer_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)

    def save_data(self):
        if not self.time_out:
            messagebox.showerror("Error", "Please click OUT before saving!")
            return
            
        # Calculate total time and pause time
        total_duration = self.time_out - self.time_in
        pause_minutes = self.total_pause_duration.total_seconds() // 60
        actual_duration = total_duration - self.total_pause_duration
        
        data = {
            'Date': [self.time_in.date()],
            'Time In': [self.time_in.strftime('%H:%M:%S')],
            'Time Out': [self.time_out.strftime('%H:%M:%S')],
            'Total Time': [f"{total_duration.seconds // 3600:02d}:{(total_duration.seconds % 3600) // 60:02d}:{total_duration.seconds % 60:02d}"],
            'Pause Time': [f"{int(pause_minutes // 60):02d}:{int(pause_minutes % 60):02d}:00"],
            'Actual Time': [f"{actual_duration.seconds // 3600:02d}:{(actual_duration.seconds % 3600) // 60:02d}:{actual_duration.seconds % 60:02d}"]
        }
        df = pd.DataFrame(data)
        
        file_path = 'time_tracker.xlsx'
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Data saved successfully!")

    def export_data(self):
        if not os.path.exists('time_tracker.xlsx'):
            messagebox.showerror("Error", "No data to export!")
            return
            
        base_name = 'time_tracker_export.xlsx'
        counter = 0
        export_path = base_name
        
        while os.path.exists(export_path):
            counter += 1
            export_path = f'time_tracker_export_{counter}.xlsx'
        
        df = pd.read_excel('time_tracker.xlsx')
        df.to_excel(export_path, index=False)
        messagebox.showinfo("Success", f"Data exported to {export_path}!")

    def show_history(self):
        if not os.path.exists('time_tracker.xlsx'):
            messagebox.showinfo("Info", "No history available!")
            return
            
        history_window = tk.Toplevel(self.root)
        history_window.title("Time Tracking History")
        history_window.geometry("1000x600")  # Made taller to accommodate summary
        history_window.configure(bg=self.current_theme["bg"])
        
        # Configure history window grid
        history_window.grid_rowconfigure(0, weight=1)
        history_window.grid_columnconfigure(0, weight=1)
        
        # Create main frame for history with Material styling
        history_frame = ttk.Frame(
            history_window,
            style="Material.TFrame",
            padding="20"
        )
        history_frame.grid(row=0, column=0, sticky="nsew")
        history_frame.grid_rowconfigure(1, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)
        
        # Create title label
        title_label = ttk.Label(
            history_frame,
            text="Time Tracking History",
            style="MaterialTimer.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="n")
        
        # Create Treeview with Material styling
        style = ttk.Style()
        style.configure("Treeview",
            background=self.current_theme["frame_bg"],
            foreground=self.current_theme["text_primary"],
            fieldbackground=self.current_theme["frame_bg"],
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure("Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            padding=10,
            background=self.current_theme["frame_bg"],
            foreground=self.current_theme["text_primary"]
        )
        style.map("Treeview",
            background=[("selected", self.current_theme["button"])],
            foreground=[("selected", self.current_theme["button_fg"])]
        )
        
        # Create frame for treeview and scrollbar
        tree_frame = ttk.Frame(history_frame, style="Material.TFrame")
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Updated columns to include pause information
        columns = ('Date', 'Time In', 'Time Out', 'Total Time', 'Pause Time', 'Actual Time')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Set column headings and widths
        column_widths = {
            'Date': 100,
            'Time In': 100,
            'Time Out': 100,
            'Total Time': 100,
            'Pause Time': 100,
            'Actual Time': 100
        }
        
        # Add sorting functionality
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)
            
            # Rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
                
            # Reverse sort next time
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
            
            # Update row colors after sorting
            update_row_colors()
        
        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
            tree.column(col, width=column_widths.get(col, 150), anchor="center")
        
        # Add scrollbar with Material styling
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid tree and scrollbar
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Load data
        df = pd.read_excel('time_tracker.xlsx')
        
        # Function to update row colors
        def update_row_colors():
            for i, item in enumerate(tree.get_children()):
                if i % 2 == 0:
                    tree.tag_configure(f"row{i}", background=self.current_theme["frame_bg"])
                else:
                    tree.tag_configure(f"row{i}", background=self._lighten_color(self.current_theme["frame_bg"]))
                tree.item(item, tags=(f"row{i}",))
                
                # Color code time columns
                values = tree.item(item)['values']
                if values:
                    pause_time = values[4]  # Pause Time column
                    if pause_time and pause_time != "00:00:00":
                        tree.tag_configure(f"pause{item}", foreground="#FF5252")  # Red for pause time
                        tree.item(item, tags=(f"row{i}", f"pause{item}"))
                    
                    actual_time = values[5]  # Actual Time column
                    if actual_time:
                        tree.tag_configure(f"actual{item}", foreground="#00E676")  # Green for actual time
                        tree.item(item, tags=(f"row{i}", f"actual{item}"))
        
        # Insert data and apply colors
        for _, row in df.iterrows():
            tree.insert('', 'end', values=list(row))
        update_row_colors()
        
        # Calculate and display totals
        total_frame = ttk.Frame(history_frame, style="Material.TFrame")
        total_frame.grid(row=2, column=0, sticky="ew", pady=(20, 20))
        total_frame.grid_columnconfigure(1, weight=1)
        
        # Calculate totals
        total_actual_time = pd.to_timedelta(df['Actual Time'].astype(str)).sum()
        total_pause_time = pd.to_timedelta(df['Pause Time'].astype(str)).sum()
        total_hours = total_actual_time.total_seconds() / 3600
        
        # Format totals
        total_actual_str = f"{int(total_actual_time.total_seconds() // 3600):02d}:{int((total_actual_time.total_seconds() % 3600) // 60):02d}:{int(total_actual_time.total_seconds() % 60):02d}"
        total_pause_str = f"{int(total_pause_time.total_seconds() // 3600):02d}:{int((total_pause_time.total_seconds() % 3600) // 60):02d}:{int(total_pause_time.total_seconds() % 60):02d}"
        
        # Create summary labels with Material styling
        summary_style = {
            'font': ("Segoe UI", 11),
            'background': self.current_theme["frame_bg"],
            'foreground': self.current_theme["text_primary"],
            'padding': 10
        }
        
        ttk.Label(
            total_frame,
            text=f"Total Work Time: {total_actual_str}",
            style="MaterialStatus.TLabel",
            **summary_style
        ).grid(row=0, column=0, padx=5, sticky="w")
        
        ttk.Label(
            total_frame,
            text=f"Total Pause Time: {total_pause_str}",
            style="MaterialStatus.TLabel",
            **summary_style
        ).grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(
            total_frame,
            text=f"Total Days: {len(df)}",
            style="MaterialStatus.TLabel",
            **summary_style
        ).grid(row=0, column=2, padx=5, sticky="e")
        
        # Back button with Material styling
        back_btn = tk.Button(
            history_frame,
            text="Back",
            command=history_window.destroy,
            font=("Segoe UI", 11),
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        back_btn.grid(row=3, column=0, pady=(0, 0))

    def set_window_size(self, size):
        # Adjust visibility of elements
        self.last_out_label.grid()
        self.last_spent_label.grid()
        self.export_btn.grid(row=0, column=2, padx=5)
        self.history_btn.grid(row=0, column=3, padx=5)

    def _add_button_hover_effects(self):
        """Add hover effects to buttons"""
        def on_enter(e):
            if e.widget == self.in_btn:
                if not self.is_timing:
                    e.widget.configure(bg=self._lighten_color(self.current_theme["button"]))
            elif e.widget == self.out_btn:
                if self.is_timing:
                    e.widget.configure(bg=self._lighten_color(self.current_theme["button"]))
            elif e.widget == self.mode_btn:
                e.widget.configure(bg=self._lighten_color(self.current_theme["frame_bg"]))
            else:  # Action buttons
                e.widget.configure(bg="#616161")  # Lighter grey for hover

        def on_leave(e):
            if e.widget == self.in_btn:
                e.widget.configure(
                    bg=self.current_theme["green"] if self.is_timing 
                    else self.current_theme["button"]
                )
            elif e.widget == self.out_btn:
                e.widget.configure(
                    bg=self.current_theme["red"] if not self.is_timing and self.time_out 
                    else self.current_theme["button"]
                )
            elif e.widget == self.mode_btn:
                e.widget.configure(bg=self.current_theme["frame_bg"])
            else:  # Action buttons
                e.widget.configure(bg="#424242")  # Back to dark grey

        # Add hover effects to buttons
        for btn in [self.in_btn, self.out_btn, self.mode_btn]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Add hover effects to action buttons
        for btn in [self.save_btn, self.export_btn, self.history_btn]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def _lighten_color(self, color):
        """Lighten a color by 20%"""
        # Handle invalid color values
        if not color.startswith('#') or len(color) != 7:
            return color
            
        try:
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Lighten by 20%
            r = min(int(r * 1.2), 255)
            g = min(int(g * 1.2), 255)
            b = min(int(b * 1.2), 255)
            
            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return color

    def toggle_menu(self):
        """Toggle the side menu expansion"""
        if self.menu_expanded:
            self.hide_menu_buttons()
        else:
            self.show_menu_buttons()
        self.menu_expanded = not self.menu_expanded

    def show_menu_buttons(self):
        """Show the side menu buttons"""
        for i, btn in enumerate(self.menu_buttons, start=1):
            btn.grid(row=i, column=0, pady=5, sticky="ew")

    def hide_menu_buttons(self):
        """Hide the side menu buttons"""
        for btn in self.menu_buttons:
            btn.grid_remove()

    def show_about(self):
        """Show information about the app"""
        about_text = """Time Tracker App

This application helps you track your work hours efficiently:

• Click 'IN' when you start working
• Click 'OUT' when you finish
• Save your time records
• Export data to Excel
• View your time history

The app automatically calculates your work duration
and maintains a history of all your time records."""

        messagebox.showinfo("About Time Tracker", about_text)

    def toggle_window_mode(self):
        """Toggle between normal and popup modes"""
        self.is_popup_mode = not self.is_popup_mode
        
        if self.is_popup_mode:
            # Store current geometry before switching to popup mode
            self.normal_geometry = self.root.geometry()
            
            # Configure popup mode
            self.root.overrideredirect(True)  # Remove window decorations
            self.root.geometry("200x100")  # Small size for popup
            
            # Hide all non-essential elements
            self.side_menu.grid_remove()
            self.status_frame.grid_remove()
            self.theme_btn.grid_remove()
            self.time_label.grid_remove()
            self.date_tz_label.grid_remove()
            
            # Adjust timer and buttons for popup mode
            self.timer_label.configure(font=("Segoe UI", 16, "bold"))  # Smaller font
            self.in_btn.configure(font=("Segoe UI", 12, "bold"), padx=10, pady=5)
            self.out_btn.configure(font=("Segoe UI", 12, "bold"), padx=10, pady=5)
            if hasattr(self, 'pause_btn'):
                self.pause_btn.configure(font=("Segoe UI", 12, "bold"), padx=10, pady=5)
            if hasattr(self, 'resume_btn'):
                self.resume_btn.configure(font=("Segoe UI", 12, "bold"), padx=10, pady=5)
            
            # Center the timer label
            self.timer_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")
            
            # Update mode button
            self.mode_btn.configure(text="🗖")
            
            # Make window stay on top
            self.root.attributes('-topmost', True)
            
            # Add drag functionality
            self.root.bind('<Button-1>', self.start_drag)
            self.root.bind('<B1-Motion>', self.drag_window)
            
        else:
            # Restore normal mode
            self.root.overrideredirect(False)
            self.root.geometry(self.normal_geometry)
            
            # Show all elements
            self.side_menu.grid()
            self.status_frame.grid()
            self.theme_btn.grid()
            self.time_label.grid()
            self.date_tz_label.grid()
            
            # Restore original sizes
            self.timer_label.configure(font=("Segoe UI", 36, "bold"))
            self.in_btn.configure(font=("Segoe UI", 16, "bold"), padx=40, pady=20)
            self.out_btn.configure(font=("Segoe UI", 16, "bold"), padx=40, pady=20)
            if hasattr(self, 'pause_btn'):
                self.pause_btn.configure(font=("Segoe UI", 16, "bold"), padx=40, pady=20)
            if hasattr(self, 'resume_btn'):
                self.resume_btn.configure(font=("Segoe UI", 16, "bold"), padx=40, pady=20)
            
            # Restore timer label position
            self.timer_label.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="n")
            
            # Update mode button
            self.mode_btn.configure(text="🗗")
            
            # Remove stay on top
            self.root.attributes('-topmost', False)
            
            # Remove drag bindings
            self.root.unbind('<Button-1>')
            self.root.unbind('<B1-Motion>')

    def start_drag(self, event):
        """Start window drag"""
        if self.is_popup_mode:  # Only allow dragging in popup mode
            self._drag_data = {'x': event.x, 'y': event.y}

    def drag_window(self, event):
        """Handle window dragging"""
        if self.is_popup_mode and hasattr(self, '_drag_data'):  # Only allow dragging in popup mode
            x = self.root.winfo_x() + (event.x - self._drag_data['x'])
            y = self.root.winfo_y() + (event.y - self._drag_data['y'])
            self.root.geometry(f"+{x}+{y}")

    def toggle_compact_view(self):
        """Toggle between compact and full size views"""
        current_width = self.root.winfo_width()
        if current_width > 400:  # If currently in full view
            self.root.geometry("400x450")
            self.resize_btn.configure(text="🔎")  # Magnifying glass with plus
        else:  # If currently in compact view
            self.root.geometry("600x450")
            self.resize_btn.configure(text="🔍")  # Regular magnifying glass

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTracker(root)
    root.mainloop() 