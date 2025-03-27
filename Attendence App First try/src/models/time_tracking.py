"""
Time tracking model for managing time records and calculations.
"""

from datetime import datetime, timedelta
import pandas as pd
import os

class TimeTrackingModel:
    def __init__(self):
        """Initialize the time tracking model."""
        self.time_in = None
        self.time_out = None
        self.is_timing = False
        self.is_paused = False
        self.pause_start = None
        self.total_pause_duration = timedelta()

    def start_timing(self):
        """Start timing a new session."""
        if not self.is_timing:
            self.time_in = datetime.now()
            self.is_timing = True
            self.is_paused = False
            self.total_pause_duration = timedelta()
            return True
        return False

    def end_timing(self):
        """End the current timing session."""
        if self.is_timing:
            if self.is_paused:
                # If paused, add the current pause duration
                pause_duration = datetime.now() - self.pause_start
                self.total_pause_duration += pause_duration
            
            self.time_out = datetime.now()
            self.is_timing = False
            self.is_paused = False
            return True
        return False

    def pause_timing(self):
        """Pause the current timing session."""
        if self.is_timing and not self.is_paused:
            self.is_paused = True
            self.pause_start = datetime.now()
            return True
        return False

    def resume_timing(self):
        """Resume the paused timing session."""
        if self.is_timing and self.is_paused:
            pause_duration = datetime.now() - self.pause_start
            self.total_pause_duration += pause_duration
            self.is_paused = False
            self.pause_start = None
            return True
        return False

    def get_current_duration(self):
        """Calculate the current duration of the timing session."""
        if self.is_timing and self.time_in:
            if not self.is_paused:
                return datetime.now() - self.time_in - self.total_pause_duration
        return timedelta()

    def save_record(self):
        """Save the current time record to Excel file."""
        if not self.time_out:
            return False

        # Calculate total time and pause time
        total_duration = self.time_out - self.time_in
        pause_minutes = self.total_pause_duration.total_seconds() // 60
        actual_duration = total_duration - self.total_pause_duration
        
        data = {
            'Date': [self.time_in.date()],
            'Time In': [self.time_in.strftime('%H:%M:%S')],
            'Time Out': [self.time_out.strftime('%H:%M:%S')],
            'Total Time': [self._format_duration(total_duration)],
            'Pause Time': [f"{int(pause_minutes // 60):02d}:{int(pause_minutes % 60):02d}:00"],
            'Actual Time': [self._format_duration(actual_duration)]
        }
        df = pd.DataFrame(data)
        
        file_path = 'time_tracker.xlsx'
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_excel(file_path, index=False)
        return True

    def export_data(self, export_path=None):
        """Export time tracking data to a new Excel file."""
        if not os.path.exists('time_tracker.xlsx'):
            return False
            
        if export_path is None:
            base_name = 'time_tracker_export.xlsx'
            counter = 0
            export_path = base_name
            
            while os.path.exists(export_path):
                counter += 1
                export_path = f'time_tracker_export_{counter}.xlsx'
        
        df = pd.read_excel('time_tracker.xlsx')
        df.to_excel(export_path, index=False)
        return True

    @staticmethod
    def _format_duration(duration):
        """Format a timedelta duration into HH:MM:SS string."""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @staticmethod
    def load_history():
        """Load time tracking history from Excel file."""
        if not os.path.exists('time_tracker.xlsx'):
            return None
        return pd.read_excel('time_tracker.xlsx') 