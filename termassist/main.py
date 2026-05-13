#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TermAssist - Terminal AI Command Assistant
智能终端命令助手

Main entry point
"""

import os
import sys
import re
import subprocess
import argparse
from typing import Optional

from .config import config
from .llm_client import create_llm_client, BaseLLMClient
from .ui import TerminalUI, detect_shell, detect_os
from .prompts import Prompts
from .history import HistoryManager


class TermAssist:
    """Main application class"""
    
    def __init__(self):
        self.config = config
        self.llm_config = config.get_llm_config()
        self.app_config = config.get_app_config()
        self.ui = TerminalUI(self.app_config)
        self.llm_client: Optional[BaseLLMClient] = None
        self.history = HistoryManager()
        self.os_name = detect_os()
        self.shell = detect_shell()
        
    def initialize(self) -> bool:
        """Initialize the application"""
        try:
            self.llm_client = create_llm_client(self.llm_config)
            
            # Check connection
            if not self.llm_client.check_connection():
                self.ui.show_error(
                    f"Cannot connect to {self.llm_config.provider}. "
                    "Please check your configuration."
                )
                self.ui.show_info(
                    f"To configure: edit {config.config_file}"
                )
                return False
            
            return True
        except Exception as e:
            self.ui.show_error(f"Initialization failed: {e}")
            return False
    
    def is_command_like(self, text: str) -> bool:
        """Check if input looks like a command (not natural language)"""
        # Common command patterns
        command_patterns = [
            r'^[\w\-]+\s',  # command with args
            r'^\$\s',  # starts with $
            r'^[\|\&\;\>\<]',  # starts with shell operators
            r'^(ls|cd|cat|grep|awk|sed|curl|wget|ssh|git|docker|kubectl|npm|pip)\s',
            r'^(sudo|bash|sh|zsh|fish|python|node|java|go|ruby)\s',
            r'^(mkdir|rm|cp|mv|touch|chmod|chown|find|ps|top|htop|df|du)\s',
            r'^(echo|printf|export|source|alias|unset|env|which|whereis)\s',
        ]
        
        text = text.strip()
        for pattern in command_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        
        # If it contains shell special characters, likely a command
        if re.search(r'[\|\&\;\>\<\$\`]', text):
            return True
        
        return False
    
    def generate_command(self, query: str) -> str:
        """Generate command from natural language"""
        system_prompt = Prompts.get_system_prompt(
            self.app_config.language, self.os_name, self.shell
        )
        prompt = Prompts.get_generation_prompt(self.app_config.language, query)
        
        return self.llm_client.generate(prompt, system_prompt)
    
    def explain_command(self, command: str) -> str:
        """Explain a command"""
        system_prompt = Prompts.get_system_prompt(
            self.app_config.language, self.os_name, self.shell
        )
        prompt = Prompts.get_explain_prompt(self.app_config.language, command)
        
        return self.llm_client.generate(prompt, system_prompt)
    
    def execute_command(self, command: str) -> bool:
        """Execute a shell command"""
        try:
            # Remove comments and extract actual command
            lines = command.strip().split('\n')
            actual_commands = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    actual_commands.append(line)
            
            if not actual_commands:
                return False
            
            full_command = ' && '.join(actual_commands)
            
            # Confirm before execution
            if not self.ui.confirm_execute(full_command):
                return False
            
            # Execute
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=False,
                text=True
            )
            
            return result.returncode == 0
        except Exception as e:
            self.ui.show_error(f"Execution failed: {e}")
            return False
    
    def handle_input(self, user_input: str) -> bool:
        """Handle user input"""
        user_input = user_input.strip()
        
        if not user_input:
            return True
        
        # Handle special commands
        if user_input.startswith('/'):
            return self.handle_special_command(user_input)
        
        # Determine mode
        if self.is_command_like(user_input):
            # Explain mode
            with self.ui.show_generating():
                result = self.explain_command(user_input)
            
            self.ui.show_result(result, is_command=False)
            self.ui.add_to_history(user_input, result, "explain")
            self.history.add(user_input, result, "explain")
        else:
            # Generate mode
            with self.ui.show_generating():
                result = self.generate_command(user_input)
            
            self.ui.show_result(result, is_command=True)
            self.ui.add_to_history(user_input, result, "generate")
            entry_id = self.history.add(user_input, result, "generate")
            
            # Auto copy if enabled
            if self.app_config.auto_copy:
                self.ui.copy_to_clipboard(result)
            
            # Ask if user wants to execute
            if self.ui.confirm_execute(result):
                success = self.execute_command(result)
                self.history.update_execution_status(entry_id, success)
        
        return True
    
    def handle_special_command(self, command: str) -> bool:
        """Handle special commands"""
        cmd = command.lower().strip()
        
        if cmd in ('/exit', '/quit', '/q'):
            return False
        
        elif cmd == '/help':
            self.ui.show_help()
        
        elif cmd == '/config':
            self.ui.show_config(self.llm_config)
        
        elif cmd == '/history':
            self.ui.show_history()
            # Also show from database
            entries = self.history.get_recent(10)
            if entries:
                self.ui.show_info("Recent entries from database:")
                for entry in entries[:5]:
                    self.ui.console.print(f"  [{entry.mode}] {entry.input_text[:50]}...")
        
        elif cmd == '/clear':
            self.ui.clear_screen()
        
        elif cmd.startswith('/lang '):
            lang = command[6:].strip()
            if lang in ('zh', 'en', 'zh-tw'):
                self.app_config.language = lang
                self.config.update_app_config(language=lang)
                self.ui.language = lang
                self.ui.show_success(f"Language set to {lang}")
            else:
                self.ui.show_error("Supported languages: zh, en, zh-tw")
        
        elif cmd == '/stats':
            stats = self.history.get_stats()
            self.ui.console.print(f"[cyan]History Statistics:[/cyan]")
            self.ui.console.print(f"  Total entries: {stats['total']}")
            self.ui.console.print(f"  Generate mode: {stats['generate']}")
            self.ui.console.print(f"  Explain mode: {stats['explain']}")
            self.ui.console.print(f"  Executed: {stats['executed']}")
            self.ui.console.print(f"  Successful: {stats['success']}")
        
        else:
            self.ui.show_error(f"Unknown command: {command}")
            self.ui.show_info("Type /help for available commands")
        
        return True
    
    def run(self):
        """Main loop"""
        self.ui.show_welcome()
        
        if not self.initialize():
            sys.exit(1)
        
        self.ui.show_info(f"Connected to {self.llm_config.provider} ({self.llm_config.model})")
        self.ui.show_info("Type /help for usage information")
        self.ui.console.print()
        
        running = True
        while running:
            try:
                user_input = self.ui.get_input()
                running = self.handle_input(user_input)
                self.ui.console.print()
            except KeyboardInterrupt:
                running = False
            except EOFError:
                running = False
        
        self.ui.show_exit()


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="TermAssist - Terminal AI Command Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  termassist              # Start interactive mode
  termassist "find large files"  # One-shot command generation
  
Special commands in interactive mode:
  /help     - Show help
  /config   - Show configuration
  /history  - Show history
  /clear    - Clear screen
  /exit     - Exit program
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='Natural language query or command to explain'
    )
    
    parser.add_argument(
        '-e', '--explain',
        action='store_true',
        help='Explain mode: treat input as a command to explain'
    )
    
    parser.add_argument(
        '-c', '--copy',
        action='store_true',
        help='Copy result to clipboard'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    if args.query:
        # One-shot mode
        app = TermAssist()
        
        if not app.initialize():
            sys.exit(1)
        
        if args.explain or app.is_command_like(args.query):
            result = app.explain_command(args.query)
        else:
            result = app.generate_command(args.query)
        
        print(result)
        
        if args.copy:
            try:
                import pyperclip
                pyperclip.copy(result)
                print("\n[Copied to clipboard]")
            except Exception:
                pass
    else:
        # Interactive mode
        app = TermAssist()
        app.run()


if __name__ == '__main__':
    main()
