"""
Theme configurations for the Time Tracker application.
Contains color schemes and styling information for different themes.
"""

THEMES = {
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