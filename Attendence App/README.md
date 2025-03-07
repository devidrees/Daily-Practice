# Time Tracker Application

A modern time tracking application built with Python and Tkinter, featuring Material Design UI.

## Features

- Simple IN/OUT time tracking
- Pause/Resume functionality
- Multiple theme options
- Sound notifications (with mute option)
- Compact and full-size views
- History view with sorting
- Data export to Excel
- Detailed time statistics

## Project Structure

```
src/
├── constants/
│   └── themes.py          # Theme configurations
├── models/
│   └── time_tracking.py   # Time tracking logic
├── ui/
│   └── components.py      # Reusable UI components
├── utils/
│   └── sound_manager.py   # Sound handling
├── __init__.py           # Package initialization
└── main.py              # Main application entry point
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/time-tracker.git
cd time-tracker
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

### Basic Controls

- Click 'IN' to start timing
- Click 'PAUSE' to pause timing
- Click 'RESUME' to continue timing
- Click 'OUT' to end timing
- Use the side menu for additional options

### Features

1. **Theme Switching**
   - Click the theme button to cycle through available themes
   - Supports Light, Dark, Dracula, Nord, and Solarized themes

2. **View Modes**
   - Toggle between full and compact views
   - Switch to popup mode for minimal interface

3. **Sound Notifications**
   - Different sounds for IN, OUT, PAUSE, and RESUME actions
   - Mute option available in the side menu

4. **Data Management**
   - Save time records to Excel
   - Export data to separate files
   - View history with sorting options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 