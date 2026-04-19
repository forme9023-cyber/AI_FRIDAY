import logging
import os
import sys
from datetime import datetime
from config import (
    LOG_FILE, LOGS_DIR, DEBUG_MODE, AUTO_START_ENABLED,
    MORNING_BRIEF_TIME, FEATURES, VOICE_PROFILES, LANGUAGES
)
from ui.animations import Animations
from core.voice_engine import VoiceEngine
from core.wake_word import WakeWordDetector, ListeningLoop
from core.intent_handler import IntentHandler
from core.ai_brain import AIBrain
from system.file_manager import FileManager
from system.autostart import AutoStartManager
from features.morning_brief import MorningBrief
from features.command_memory import CommandMemory
from features.voice_profiles import VoiceProfileManager
from system.performance import PerformanceMonitor
from system.wifi_manager import WiFiManager
from features.ambient_mode import AmbientMode
from features.news_weather import NewsWeatherManager
from features.productivity import ProductivityTools
from features.music_control import MusicController
from features.file_search import FileSearcher
from features.language_support import LanguageManager

# Setup logging
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class FRIDAYAssistant:
    def __init__(self):
        logger.info("Initializing FRIDAY Assistant with Phase 1-4 Features...")
        
        # Phase 1: GUI & Core Components
        self.voice_engine = VoiceEngine()
        self.wake_detector = WakeWordDetector()
        self.listening_loop = ListeningLoop(self.voice_engine, self.wake_detector)
        self.intent_handler = IntentHandler()
        self.ai_brain = AIBrain()
        self.file_manager = FileManager()
        
        # Phase 2: Memory & Profiles
        self.command_memory = CommandMemory()
        self.voice_profile_manager = VoiceProfileManager()
        self.current_profile = "serious"
        
        # Phase 3: System Integration
        self.performance_monitor = PerformanceMonitor()
        self.wifi_manager = WiFiManager()
        
        # Phase 4: Smart Features
        self.ambient_mode = AmbientMode()
        self.news_weather = NewsWeatherManager()
        self.productivity_tools = ProductivityTools()
        self.music_controller = MusicController()
        self.file_searcher = FileSearcher()
        self.language_manager = LanguageManager()
        self.morning_brief = MorningBrief()
        
        # Ensure directories exist
        self.file_manager.ensure_dirs()
        
        logger.info("FRIDAY Assistant initialized successfully with all Phase 1-4 features.")
    
    def boot_sequence(self):
        """Execute boot sequence with all features"""
        logger.info("Boot sequence started.")
        Animations.boot_animation()
        
        if AUTO_START_ENABLED:
            AutoStartManager.setup_autostart()
            logger.info("Autostart enabled.")
        
        # Show morning brief if during morning hours
        if self.is_morning_hours():
            brief = self.morning_brief.get_brief()
            self.voice_engine.speak(brief)
        
        # Initialize ambient mode
        if FEATURES.get("ambient_mode"):
            self.ambient_mode.start_idle_display()
    
    def is_morning_hours(self):
        """Check if it's morning"""
        current_hour = datetime.now().hour
        return 6 <= current_hour < 12
    
    def handle_command_with_features(self, user_input):
        """Enhanced command handler with all Phase 1-4 features"""
        try:
            # Store in memory
            self.command_memory.add_command(user_input)
            
            # Identify intent
            intent = self.ai_brain.identify_intent(user_input)
            
            # Route to appropriate feature handler
            if intent == "music":
                return self.music_controller.handle_command(user_input)
            elif intent == "file":
                return self.file_searcher.handle_command(user_input)
            elif intent == "productivity":
                return self.productivity_tools.handle_command(user_input)
            elif intent == "weather":
                return self.news_weather.get_weather()
            elif intent == "news":
                return self.news_weather.get_news()
            elif intent == "wifi":
                return self.wifi_manager.handle_command(user_input)
            elif intent == "performance":
                return self.performance_monitor.get_system_status()
            elif intent == "profile":
                return self.switch_voice_profile(user_input)
            elif intent == "language":
                return self.language_manager.handle_language_switch(user_input)
            else:
                # Default: use AI brain
                return self.ai_brain.process_command(user_input, intent)
        
        except Exception as e:
            logger.error(f"Command handling error: {e}")
            return f"Sorry boss, error processing command: {str(e)}"
    
    def switch_voice_profile(self, user_input):
        """Switch between voice profiles"""
        for profile in VOICE_PROFILES:
            if profile.lower() in user_input.lower():
                self.current_profile = profile
                self.voice_profile_manager.set_profile(profile)
                return f"Switched to {profile} mode."
        return "Profile not recognized."
    
    def main_loop(self):
        """Main listening and command execution loop"""
        logger.info("Entering main loop with all Phase 1-4 features.")
        
        try:
            while True:
                # Listen for wake word or clap
                is_awake = self.listening_loop.start_listening()
                
                if is_awake:
                    Animations.wake_animation()
                    self.voice_engine.speak("Yes boss, I'm listening.")
                    
                    # Listen for command
                    Animations.listening_animation()
                    user_input = self.voice_engine.listen_for_command()
                    
                    if user_input:
                        # Process command with all features
                        Animations.processing_animation()
                        response = self.handle_command_with_features(user_input)
                        
                        # Speak response with current voice profile
                        self.voice_engine.speak(response, profile=self.current_profile)
                        
                        Animations.success_message(response)
                    
                # Return to listening
                self.listening_loop.is_listening = False
        
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.voice_engine.speak("Going to sleep, boss. Talk soon.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            self.voice_engine.speak(f"Error: {str(e)}")

def main():
    """Main entry point"""
    try:
        assistant = FRIDAYAssistant()
        assistant.boot_sequence()
        assistant.main_loop()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()