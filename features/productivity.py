import logging
import threading
import time
from config import FOCUS_MODE_DURATION, FOCUS_BREAK_DURATION, LONG_BREAK_DURATION

logger = logging.getLogger(__name__)

class ProductivityTools:
    def __init__(self):
        self.focus_duration = FOCUS_MODE_DURATION * 60  # Convert to seconds
        self.break_duration = FOCUS_BREAK_DURATION * 60
        self.long_break_duration = LONG_BREAK_DURATION * 60
        self.is_running = False
        self.session_count = 0
    
    def start_pomodoro(self):
        """Start Pomodoro timer"""
        try:
            self.is_running = True
            self.session_count += 1
            
            message = f"Starting Pomodoro Session {self.session_count}. Focus time: {self.focus_duration // 60} minutes."
            logger.info(message)
            
            # Run timer in background thread
            timer_thread = threading.Thread(
                target=self._run_focus_timer,
                daemon=True
            )
            timer_thread.start()
            
            return message
        except Exception as e:
            logger.error(f"Error starting Pomodoro: {e}")
            return "Failed to start Pomodoro timer."
    
    def _run_focus_timer(self):
        """Run focus timer in background"""
        try:
            time.sleep(self.focus_duration)
            
            if self.session_count % 4 == 0:
                logger.info("Time for a long break!")
                # Long break after 4 sessions
            else:
                logger.info("Time for a short break!")
                # Short break
            
            self.is_running = False
        except Exception as e:
            logger.error(f"Error in focus timer: {e}")
    
    def stop_pomodoro(self):
        """Stop current Pomodoro session"""
        self.is_running = False
        logger.info(f"Pomodoro session stopped. Completed: {self.session_count}")
        return f"Pomodoro session stopped. Sessions completed today: {self.session_count}"
    
    def enable_focus_mode(self):
        """Enable focus mode (disable notifications)"""
        try:
            logger.info("Focus mode enabled.")
            # In production, would disable system notifications
            return "Focus mode activated. Minimizing distractions..."
        except Exception as e:
            logger.error(f"Error enabling focus mode: {e}")
            return "Failed to enable focus mode."
    
    def disable_focus_mode(self):
        """Disable focus mode"""
        try:
            logger.info("Focus mode disabled.")
            return "Focus mode deactivated."
        except Exception as e:
            logger.error(f"Error disabling focus mode: {e}")
            return "Failed to disable focus mode."
    
    def get_status(self):
        """Get productivity status"""
        status = f"Sessions completed: {self.session_count}\n"
        status += f"Focus mode: {'Active' if self.is_running else 'Inactive'}\n"
        return status
    
    def handle_command(self, user_input):
        """Handle productivity-related commands"""
        user_lower = user_input.lower()
        
        if "pomodoro" in user_lower or "timer" in user_lower:
            if "start" in user_lower or "begin" in user_lower:
                return self.start_pomodoro()
            elif "stop" in user_lower or "end" in user_lower:
                return self.stop_pomodoro()
        
        elif "focus" in user_lower:
            if "enable" in user_lower or "start" in user_lower:
                return self.enable_focus_mode()
            elif "disable" in user_lower or "stop" in user_lower:
                return self.disable_focus_mode()
        
        elif "status" in user_lower:
            return self.get_status()
        
        return "Productivity tools ready. Try: start pomodoro, enable focus mode, or check status."