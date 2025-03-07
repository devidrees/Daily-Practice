"""
Main entry point for the Time Tracker application.
"""

import tkinter as tk
from datetime import datetime
import pytz

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
        self.normal_geometry = "600x450"
        self.root.geometry(self.normal_geometry)
        self.root.configure(bg=self.current_theme["bg"])
        self.root.resizable(True, True)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create UI components
        self._create_side_menu()
        self._create_main_content()
        
        # Start update loops
        self._update_timer()
        self._update_datetime()

    def _create_side_menu(self):
        """Create the side menu and its buttons."""
        # Create menu frame
        self.side_menu = MaterialFrame(self.root, self.current_theme, padding="10")
        self.side_menu.grid(row=0, column=0, sticky="ns")
        self.side_menu.grid_rowconfigure(5, weight=1)
        
        # Create menu buttons
        self._create_menu_buttons()
        
        # Initially hide the buttons
        self._hide_menu_buttons()

    def _create_menu_buttons(self):
        """Create all menu buttons."""
        # Menu toggle button
        self.menu_btn = MaterialButton(
            self.side_menu,
            text="☰",
            font=("Segoe UI", 16),
            bg=self.current_theme["frame_bg"],
            fg=self.current_theme["text_primary"],
            command=self._toggle_menu
        )
        self.menu_btn.grid(row=0, column=0, pady=(0, 20), sticky="nw")
        
        # Common button style
        button_style = {
            'font': ("Segoe UI", 11),
            'bg': "#424242",
            'fg': "#FFFFFF",
            'activebackground': "#616161",
            'activeforeground': "#FFFFFF",
            'anchor': 'w',
            'width': 10
        }
        
        # Create action buttons
        self.menu_buttons = []
        
        # Save button
        self.save_btn = MaterialButton(
            self.side_menu,
            text="💾 Save",
            command=self._save_data,
            **button_style
        )
        self.menu_buttons.append(self.save_btn)
        
        # Export button
        self.export_btn = MaterialButton(
            self.side_menu,
            text="📤 Export",
            command=self._export_data,
            **button_style
        )
        self.menu_buttons.append(self.export_btn)
        
        # History button
        self.history_btn = MaterialButton(
            self.side_menu,
            text="📋 History",
            command=self._show_history,
            **button_style
        )
        self.menu_buttons.append(self.history_btn)
        
        # About button
        self.about_btn = MaterialButton(
            self.side_menu,
            text="ℹ️ About",
            command=self._show_about,
            **button_style
        )
        self.menu_buttons.append(self.about_btn)
        
        # Add mute button if sound is available
        if self.sound_manager.is_sound_available:
            self.mute_btn = MaterialButton(
                self.side_menu,
                text="🔊 Sound" if not self.sound_manager.is_muted else "🔇 Muted",
                command=self._toggle_mute,
                **button_style
            )
            self.menu_buttons.append(self.mute_btn)

    def _create_main_content(self):
        """Create the main content area."""
        # Create main frame
        self.main_frame = MaterialFrame(self.root, self.current_theme, padding="10")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure main frame grid
        self._configure_main_grid()
        
        # Create UI elements
        self._create_top_buttons()
        self._create_timer_display()
        self._create_control_buttons()
        self._create_status_display()
        self._create_datetime_display()

    def _configure_main_grid(self):
        """Configure the main frame's grid layout."""
        self.main_frame.grid_rowconfigure(2, weight=3)
        self.main_frame.grid_rowconfigure(4, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

    # ... More methods for UI creation and event handling ...
    # The rest of the implementation would follow the same pattern,
    # breaking down the functionality into smaller, focused methods

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop() 