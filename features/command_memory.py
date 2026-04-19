import time

class CommandMemory:
    def __init__(self):
        self.commands = []  # Stores commands and their timestamps

    def add_command(self, command):
        # Add new command with current timestamp, keeping only the last 10
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        self.commands.append({'command': command, 'timestamp': timestamp})
        if len(self.commands) > 10:
            self.commands.pop(0)  # Maintain only the last 10 commands

    def search(self, keyword):
        # Search for commands containing the keyword
        return [cmd for cmd in self.commands if keyword in cmd['command']]

    def export_history(self):
        # Export commands history as a list of strings
        return [f"[{cmd['timestamp']}] {cmd['command']}" for cmd in self.commands]

    def repeat_command(self, index):
        # Repeat a command given its index (1-based index)
        if 0 < index <= len(self.commands):
            return self.commands[index - 1]['command']
        raise IndexError('Command index out of range')
