"""
UI components for the Time Tracker application.
Contains reusable UI elements and styling configurations.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

class MaterialButton(tk.Button):
    """A custom button class with Material Design styling."""
    def __init__(self, master, hover_color: Optional[str] = None, **kwargs):
        # Handle font separately to avoid duplicate parameter
        font_size = kwargs.pop('fontsize', 11) if 'fontsize' in kwargs else 11
        if 'font' not in kwargs:
            kwargs['font'] = ("Segoe UI", font_size)
            
        # Add rounded corners and modern styling
        super().__init__(
            master,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=15,  # Increased padding
            pady=8,
            **kwargs
        )
        
        # Store original colors
        self._original_bg = self.cget("bg")
        self._hover_color = hover_color or self._lighten_color(self._original_bg, 1.2)
        
        # Add hover bindings
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Add pressed effect
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Configure modern style
        self.configure(
            highlightthickness=0,  # Remove highlight border
            activebackground=self._hover_color,  # Color when clicked
            activeforeground=self.cget("fg"),  # Keep text color consistent
        )
        
    def _on_enter(self, e):
        """Handle mouse enter with smooth transition."""
        if "state" not in self.config() or self.config()["state"][-1] != "disabled":
            self.configure(bg=self._hover_color)

    def _on_leave(self, e):
        """Handle mouse leave with smooth transition."""
        if "state" not in self.config() or self.config()["state"][-1] != "disabled":
            self.configure(bg=self._original_bg)

    def _on_press(self, e):
        """Handle mouse press with darkening effect."""
        if "state" not in self.config() or self.config()["state"][-1] != "disabled":
            dark_color = self._darken_color(self._original_bg, 0.9)
            self.configure(bg=dark_color)

    def _on_release(self, e):
        """Handle mouse release."""
        if "state" not in self.config() or self.config()["state"][-1] != "disabled":
            self.configure(bg=self._hover_color if self.winfo_containing(e.x_root, e.y_root) == self else self._original_bg)

    @staticmethod
    def _lighten_color(color: str, factor: float = 1.2) -> str:
        """Lighten a color by a factor."""
        if not color.startswith('#') or len(color) != 7:
            return color
        try:
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Lighten
            r = min(int(r * factor), 255)
            g = min(int(g * factor), 255)
            b = min(int(b * factor), 255)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return color

    @staticmethod
    def _darken_color(color: str, factor: float = 0.8) -> str:
        """Darken a color by a factor."""
        if not color.startswith('#') or len(color) != 7:
            return color
        try:
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Darken
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return color

class MaterialFrame(ttk.Frame):
    """A custom frame class with Material Design styling."""
    def __init__(self, master, theme, has_shadow: bool = False, **kwargs):
        style = ttk.Style()
        style.configure(
            "Material.TFrame",
            background=theme["frame_bg"],
            relief="flat"
        )
        super().__init__(master, style="Material.TFrame", **kwargs)
        
        if has_shadow:
            # Create shadow effect
            self.shadow = tk.Frame(
                master,
                bg='#000000',
                width=self.winfo_width(),
                height=self.winfo_height()
            )
            self.shadow.place(x=2, y=2)  # Place shadow slightly offset
            self.lift()  # Bring main frame to front

class MaterialLabel(ttk.Label):
    """A custom label class with Material Design styling."""
    def __init__(self, master, theme, is_title=False, is_timer=False, is_status=False, 
                 is_datetime=False, has_shadow=False, **kwargs):
        style = ttk.Style()
        
        # Remove custom parameters from kwargs
        for param in ['is_title', 'is_timer', 'is_status', 'is_datetime', 'has_shadow']:
            kwargs.pop(param, None)
        
        # Configure style based on label type
        if is_title:
            style_name = "MaterialTitle.TLabel"
            font_size = 36
            font_weight = "bold"
            padding = (0, 20)
        elif is_timer:
            style_name = "MaterialTimer.TLabel"
            font_size = 48
            font_weight = "bold"
            padding = (0, 10)
        elif is_status:
            style_name = "MaterialStatus.TLabel"
            font_size = 12
            font_weight = "normal"
            padding = (0, 5)
        elif is_datetime:
            style_name = "MaterialDateTime.TLabel"
            font_size = 10
            font_weight = "normal"
            padding = (0, 5)
        else:
            style_name = "MaterialText.TLabel"
            font_size = 10
            font_weight = "normal"
            padding = (0, 5)
        
        style.configure(
            style_name,
            font=("Segoe UI", font_size, font_weight),
            foreground=theme["text_primary"],
            background=theme["frame_bg"],
            padding=padding
        )
        
        super().__init__(master, style=style_name, **kwargs)
        
        if has_shadow:
            # Add shadow effect for titles
            shadow_color = self._darken_color(theme["frame_bg"])
            shadow_label = ttk.Label(
                master,
                text=kwargs.get('text', ''),
                style=style_name,
                foreground=shadow_color
            )
            shadow_label.place(x=2, y=2)  # Place shadow slightly offset
            self.lift()  # Bring main label to front

    @staticmethod
    def _darken_color(color: str, factor: float = 0.8) -> str:
        """Darken a color by a factor."""
        if not color.startswith('#') or len(color) != 7:
            return color
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return color

def configure_treeview_style(theme):
    """Configure the Treeview widget style with Material Design."""
    style = ttk.Style()
    
    # Configure basic treeview style
    style.configure(
        "Treeview",
        background=theme["frame_bg"],
        foreground=theme["text_primary"],
        fieldbackground=theme["frame_bg"],
        borderwidth=0,
        font=("Segoe UI", 10),
        rowheight=30  # Increased row height
    )
    
    # Configure headings
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        padding=10,
        background=theme["frame_bg"],
        foreground=theme["text_primary"]
    )
    
    # Configure selection colors
    style.map(
        "Treeview",
        background=[("selected", theme["button"])],
        foreground=[("selected", theme["button_fg"])]
    )
    
    # Add hover effect
    style.map(
        "Treeview",
        background=[
            ("selected", theme["button"]),
            ("!selected", theme["frame_bg"])
        ],
        foreground=[
            ("selected", theme["button_fg"]),
            ("!selected", theme["text_primary"])
        ]
    ) 