"""
Main entry point for the Time Tracker application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pytz
import sys
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.time_tracking import TimeTrackingModel
from src.utils.sound_manager import SoundManager
from src.constants.themes import THEMES
from src.ui.components import MaterialButton, MaterialFrame, MaterialLabel, configure_treeview_style

class TimeTrackerApp:
    def __init__(self, root):
        """Initialize the Time Tracker application."""
        self.root = root
        self.root.title("Time Tracker")
        
        # Initialize models and utilities
        self.time_model = TimeTrackingModel()
        self.sound_manager = SoundManager()
        
        # Initialize UI state
        self.menu_expanded = False
        self.is_popup_mode = False
        self.current_theme_name = "dark"
        self.current_theme = THEMES[self.current_theme_name]
        
        # Configure window
        self.normal_geometry = "800x600"  # Increased window size
        self.root.geometry(self.normal_geometry)
        self.root.configure(bg=self.current_theme["bg"])
        self.root.resizable(True, True)
        
        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)  # Main content
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create header
        self._create_header()
        
        # Create UI components
        self._create_side_menu()
        self._create_main_content()
        
        # Start update loops
        self._update_timer()
        self._update_datetime()

    def _create_header(self):
        """Create the application header."""
        # Header frame with shadow
        self.header_frame = MaterialFrame(
            self.root,
            self.current_theme,
            has_shadow=True,
            padding="10"
        )
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # App title with shadow
        self.title_label = MaterialLabel(
            self.header_frame,
            self.current_theme,
            is_title=True,
            has_shadow=True,
            text="⏱️ Time Tracker"
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Top buttons frame
        top_buttons_frame = MaterialFrame(self.header_frame, self.current_theme)
        top_buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Resize button with tooltip
        self.resize_btn = MaterialButton(
            top_buttons_frame,
            text="🔍",
            command=self._toggle_compact_view,
            fontsize=12,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.resize_btn.grid(row=0, column=0, padx=(0, 10))
        self._create_tooltip(self.resize_btn, "Toggle window size")
        
        # Theme button with tooltip
        self.theme_btn = MaterialButton(
            top_buttons_frame,
            text=self.current_theme["name"],
            command=self._toggle_theme,
            fontsize=12,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.theme_btn.grid(row=0, column=1)
        self._create_tooltip(self.theme_btn, "Change theme")

    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                justify=tk.LEFT,
                background=self.current_theme["button"],
                foreground=self.current_theme["button_fg"],
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 9)
            )
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)

    def _create_side_menu(self):
        """Create the side menu and its buttons."""
        # Side menu frame with shadow
        self.menu_frame = MaterialFrame(
            self.root,
            self.current_theme,
            has_shadow=True,
            padding="10"
        )
        self.menu_frame.grid(row=1, column=0, sticky="ns", padx=(10, 0), pady=10)
        self.menu_frame.grid_rowconfigure(6, weight=1)  # Last row expands
        
        # Menu toggle button with tooltip
        self.menu_btn = MaterialButton(
            self.menu_frame,
            text="☰",
            command=self._toggle_menu,
            fontsize=16,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.menu_btn.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self._create_tooltip(self.menu_btn, "Toggle menu")
        
        # Save button with tooltip
        self.save_btn = MaterialButton(
            self.menu_frame,
            text="💾",
            command=self._save_data,
            fontsize=16,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.save_btn.grid(row=1, column=0, sticky="ew", pady=5)
        self._create_tooltip(self.save_btn, "Save records")
        
        # Export button with tooltip
        self.export_btn = MaterialButton(
            self.menu_frame,
            text="📊",
            command=self._export_data,
            fontsize=16,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.export_btn.grid(row=2, column=0, sticky="ew", pady=5)
        self._create_tooltip(self.export_btn, "Export to Excel")
        
        # History button with tooltip
        self.history_btn = MaterialButton(
            self.menu_frame,
            text="📅",
            command=self._show_history,
            fontsize=16,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.history_btn.grid(row=3, column=0, sticky="ew", pady=5)
        self._create_tooltip(self.history_btn, "View history")
        
        # About button with tooltip
        self.about_btn = MaterialButton(
            self.menu_frame,
            text="ℹ️",
            command=self._show_about,
            fontsize=16,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.about_btn.grid(row=4, column=0, sticky="ew", pady=5)
        self._create_tooltip(self.about_btn, "About")
        
        # Sound toggle button with tooltip
        self.sound_btn = MaterialButton(
            self.menu_frame,
            text="🔊",
            command=self._toggle_mute,
            fontsize=16,
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        self.sound_btn.grid(row=5, column=0, sticky="ew", pady=5)
        self._create_tooltip(self.sound_btn, "Toggle sound")
        
        # Initially hide menu buttons except toggle
        self._hide_menu_buttons()

    def _create_main_content(self):
        """Create the main content area."""
        # Main content frame with shadow
        self.main_frame = MaterialFrame(
            self.root,
            self.current_theme,
            has_shadow=True,
            padding="20"
        )
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # Configure grid
        self.main_frame.grid_rowconfigure(2, weight=1)  # Timer row
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Status display with shadow
        self.status_label = MaterialLabel(
            self.main_frame,
            self.current_theme,
            is_status=True,
            has_shadow=True,
            text="Ready to start"
        )
        self.status_label.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Timer display with shadow
        self.timer_label = MaterialLabel(
            self.main_frame,
            self.current_theme,
            is_timer=True,
            has_shadow=True,
            text="00:00:00"
        )
        self.timer_label.grid(row=2, column=0, sticky="nsew", pady=20)
        
        # Buttons frame
        self.buttons_frame = MaterialFrame(self.main_frame, self.current_theme)
        self.buttons_frame.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        self.buttons_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        # IN button with tooltip
        self.in_button = MaterialButton(
            self.buttons_frame,
            text="IN",
            command=self._time_in_click,
            fontsize=12,
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            width=10
        )
        self.in_button.grid(row=0, column=0, padx=5)
        self._create_tooltip(self.in_button, "Start timing")
        
        # PAUSE button with tooltip
        self.pause_button = MaterialButton(
            self.buttons_frame,
            text="PAUSE",
            command=self._pause_click,
            fontsize=12,
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            width=10,
            state="disabled"
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        self._create_tooltip(self.pause_button, "Pause timing")
        
        # RESUME button with tooltip
        self.resume_button = MaterialButton(
            self.buttons_frame,
            text="RESUME",
            command=self._resume_click,
            fontsize=12,
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            width=10,
            state="disabled"
        )
        self.resume_button.grid(row=0, column=2, padx=5)
        self._create_tooltip(self.resume_button, "Resume timing")
        
        # OUT button with tooltip
        self.out_button = MaterialButton(
            self.buttons_frame,
            text="OUT",
            command=self._time_out_click,
            fontsize=12,
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"],
            width=10,
            state="disabled"
        )
        self.out_button.grid(row=0, column=3, padx=5)
        self._create_tooltip(self.out_button, "Stop timing")
        
        # Date and time display with shadow
        self.datetime_label = MaterialLabel(
            self.main_frame,
            self.current_theme,
            is_datetime=True,
            has_shadow=True,
            text=self._get_current_datetime()
        )
        self.datetime_label.grid(row=4, column=0, sticky="ew", pady=(20, 0))

    def _toggle_menu(self):
        """Toggle the side menu visibility."""
        if self.menu_expanded:
            self._hide_menu_buttons()
            self.menu_frame.configure(width=50)
        else:
            self._show_menu_buttons()
            self.menu_frame.configure(width=60)
        self.menu_expanded = not self.menu_expanded

    def _hide_menu_buttons(self):
        """Hide all menu buttons except the toggle button."""
        for btn in [self.save_btn, self.export_btn, self.history_btn, 
                   self.about_btn, self.sound_btn]:
            btn.grid_remove()

    def _show_menu_buttons(self):
        """Show all menu buttons."""
        for btn in [self.save_btn, self.export_btn, self.history_btn, 
                   self.about_btn, self.sound_btn]:
            btn.grid()

    def _toggle_theme(self):
        """Toggle between available themes."""
        themes = list(THEMES.keys())
        current_index = themes.index(self.current_theme_name)
        next_index = (current_index + 1) % len(themes)
        self.current_theme_name = themes[next_index]
        self.current_theme = THEMES[self.current_theme_name]
        self._apply_theme()

    def _toggle_compact_view(self):
        """Toggle between compact and full size views."""
        current_width = self.root.winfo_width()
        if current_width > 400:  # If currently in full view
            self.root.geometry("400x450")
            self.resize_btn.configure(text="🔎")  # Magnifying glass with plus
        else:  # If currently in compact view
            self.root.geometry("600x450")
            self.resize_btn.configure(text="🔍")  # Regular magnifying glass

    def _toggle_mute(self):
        """Toggle sound mute state."""
        is_muted = self.sound_manager.toggle_mute()
        if hasattr(self, 'mute_btn'):
            self.mute_btn.configure(text="🔇 Muted" if is_muted else "🔊 Sound")

    def _time_in_click(self):
        """Handle IN button click."""
        if self.time_model.start_timing():
            self.in_button.configure(bg=self.current_theme["button"])
            self.out_button.configure(bg=self.current_theme["button"])
            self.pause_button.grid()
            self.sound_manager.play_sound('in')

    def _pause_click(self):
        """Handle PAUSE button click."""
        if self.time_model.pause_timing():
            self.pause_button.grid_remove()
            self.resume_button.grid()
            self.sound_manager.play_sound('pause')

    def _resume_click(self):
        """Handle RESUME button click."""
        if self.time_model.resume_timing():
            self.resume_button.grid_remove()
            self.pause_button.grid()
            self.sound_manager.play_sound('resume')

    def _time_out_click(self):
        """Handle OUT button click."""
        if self.time_model.end_timing():
            self.out_button.configure(bg=self.current_theme["button"])
            self.in_button.configure(bg=self.current_theme["button"])
            self.pause_button.grid_remove()
            self.resume_button.grid_remove()
            
            # Update labels
            self.status_label.configure(text="Last Time Out: " + self.time_model.time_out.strftime('%H:%M:%S'))
            duration = self.time_model.time_out - self.time_model.time_in - self.time_model.total_pause_duration
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)
            self.datetime_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.sound_manager.play_sound('out')

    def _save_data(self):
        """Save the current time record."""
        if self.time_model.save_record():
            messagebox.showinfo("Success", "Data saved successfully!")
        else:
            messagebox.showerror("Error", "Please click OUT before saving!")

    def _export_data(self):
        """Export time tracking data."""
        if self.time_model.export_data():
            messagebox.showinfo("Success", "Data exported successfully!")
        else:
            messagebox.showerror("Error", "No data to export!")

    def _show_history(self):
        """Show the history window."""
        df = self.time_model.load_history()
        if df is None:
            messagebox.showinfo("Info", "No history available!")
            return
        
        # Create history window
        history_window = tk.Toplevel(self.root)
        history_window.title("Time Tracking History")
        history_window.geometry("1000x600")
        history_window.configure(bg=self.current_theme["bg"])
        
        # Configure history window
        history_window.grid_rowconfigure(0, weight=1)
        history_window.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        history_frame = MaterialFrame(history_window, self.current_theme, padding="20")
        history_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create title
        title_label = MaterialLabel(
            history_frame,
            self.current_theme,
            is_title=True,
            text="Time Tracking History"
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="n")
        
        # Configure treeview style
        configure_treeview_style(self.current_theme)
        
        # Create treeview
        columns = ('Date', 'Time In', 'Time Out', 'Total Time', 'Pause Time', 'Actual Time')
        tree = ttk.Treeview(history_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        
        # Add data
        for _, row in df.iterrows():
            tree.insert('', 'end', values=list(row))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid tree and scrollbar
        tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure grid weights
        history_frame.grid_rowconfigure(1, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = MaterialButton(
            history_frame,
            text="Back",
            command=history_window.destroy,
            font=("Segoe UI", 11),
            bg=self.current_theme["button"],
            fg=self.current_theme["button_fg"]
        )
        back_btn.grid(row=2, column=0, pady=(20, 0))

    def _show_about(self):
        """Show information about the app."""
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

    def _update_timer(self):
        """Update the timer display."""
        if self.time_model.is_timing:
            duration = self.time_model.get_current_duration()
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)
            self.timer_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self._update_timer)

    def _update_datetime(self):
        """Update the time and date labels."""
        current_time = datetime.now()
        local_tz = current_time.astimezone().tzinfo
        
        time_text = current_time.strftime("%I:%M:%S %p")
        self.datetime_label.configure(text=time_text)
        
        date_tz_text = f"{current_time.strftime('%Y-%m-%d')} {str(local_tz)}"
        self.datetime_label.configure(text=date_tz_text)
        
        self.root.after(1000, self._update_datetime)

    def _get_current_datetime(self):
        """Get the current date and time formatted string."""
        current_time = datetime.now()
        local_tz = current_time.astimezone().tzinfo
        return f"{current_time.strftime('%I:%M:%S %p')} - {current_time.strftime('%Y-%m-%d')} {str(local_tz)}"

    def _apply_theme(self):
        """Apply the current theme to all widgets."""
        # Update window background
        self.root.configure(bg=self.current_theme["bg"])
        
        # Update header
        self.header_frame.configure(style="Material.TFrame")
        self.title_label.configure(
            fg=self.current_theme["text_primary"],
            bg=self.current_theme["frame_bg"]
        )
        
        # Update theme button
        self.theme_btn.configure(
            text=self.current_theme["name"],
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        
        # Update resize button
        self.resize_btn.configure(
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"]
        )
        
        # Update main frame
        self.main_frame.configure(style="Material.TFrame")
        
        # Update status and timer labels
        self.status_label.configure(
            fg=self.current_theme["text_primary"],
            bg=self.current_theme["frame_bg"]
        )
        self.timer_label.configure(
            fg=self.current_theme["text_primary"],
            bg=self.current_theme["frame_bg"]
        )
        
        # Update control buttons
        for button in [self.in_button, self.pause_button, self.resume_button, self.out_button]:
            button.configure(
                bg=self.current_theme["button"],
                fg=self.current_theme["button_fg"]
            )
        
        # Update datetime label
        self.datetime_label.configure(
            fg=self.current_theme["text_secondary"],
            bg=self.current_theme["frame_bg"]
        )
        
        # Update side menu
        self.menu_frame.configure(style="Material.TFrame")
        for btn in [self.menu_btn, self.save_btn, self.export_btn,
                   self.history_btn, self.about_btn, self.sound_btn]:
            btn.configure(
                bg=self.current_theme["frame_bg"],
                fg=self.current_theme["text_primary"]
            )
        
        # Configure ttk styles
        style = ttk.Style()
        style.configure(
            "Material.TFrame",
            background=self.current_theme["frame_bg"]
        )
        style.configure(
            "Material.TLabel",
            background=self.current_theme["frame_bg"],
            foreground=self.current_theme["text_primary"]
        )
        style.configure(
            "Material.Treeview",
            background=self.current_theme["frame_bg"],
            foreground=self.current_theme["text_primary"],
            fieldbackground=self.current_theme["frame_bg"]
        )
        style.configure(
            "Material.Treeview.Heading",
            background=self.current_theme["button"],
            foreground=self.current_theme["button_fg"]
        )
        style.map(
            "Material.Treeview",
            background=[("selected", self.current_theme["button"])],
            foreground=[("selected", self.current_theme["button_fg"])]
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop() 