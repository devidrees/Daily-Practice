"""
UI components for the Time Tracker application.
Contains reusable UI elements and styling configurations.
"""

import tkinter as tk
from tkinter import ttk

class MaterialButton(tk.Button):
    """A custom button class with Material Design styling."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            **kwargs
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, e):
        """Handle mouse enter event."""
        if "state" not in self.config() or self.config()["state"][-1] != "disabled":
            current_bg = self.cget("bg")
            if current_bg.startswith("#"):
                # Lighten the color by 20%
                r = int(current_bg[1:3], 16)
                g = int(current_bg[3:5], 16)
                b = int(current_bg[5:7], 16)
                r = min(int(r * 1.2), 255)
                g = min(int(g * 1.2), 255)
                b = min(int(b * 1.2), 255)
                new_color = f"#{r:02x}{g:02x}{b:02x}"
                self.configure(bg=new_color)
    
    def _on_leave(self, e):
        """Handle mouse leave event."""
        if "state" not in self.config() or self.config()["state"][-1] != "disabled":
            if hasattr(self, "_original_bg"):
                self.configure(bg=self._original_bg)

class MaterialFrame(ttk.Frame):
    """A custom frame class with Material Design styling."""
    def __init__(self, master, theme, **kwargs):
        style = ttk.Style()
        style.configure(
            "Material.TFrame",
            background=theme["frame_bg"],
            relief="flat"
        )
        super().__init__(master, style="Material.TFrame", **kwargs)

class MaterialLabel(ttk.Label):
    """A custom label class with Material Design styling."""
    def __init__(self, master, theme, is_title=False, **kwargs):
        style = ttk.Style()
        style_name = "MaterialTitle.TLabel" if is_title else "MaterialText.TLabel"
        
        style.configure(
            style_name,
            font=("Segoe UI", 36 if is_title else 10, "bold" if is_title else "normal"),
            foreground=theme["text_primary"],
            background=theme["frame_bg"],
            padding=(0, 20 if is_title else 5)
        )
        super().__init__(master, style=style_name, **kwargs)

def configure_treeview_style(theme):
    """Configure the Treeview widget style with Material Design."""
    style = ttk.Style()
    style.configure(
        "Treeview",
        background=theme["frame_bg"],
        foreground=theme["text_primary"],
        fieldbackground=theme["frame_bg"],
        borderwidth=0,
        font=("Segoe UI", 10)
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        padding=10,
        background=theme["frame_bg"],
        foreground=theme["text_primary"]
    )
    style.map(
        "Treeview",
        background=[("selected", theme["button"])],
        foreground=[("selected", theme["button_fg"])]
    ) 