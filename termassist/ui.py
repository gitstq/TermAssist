#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI components for TermAssist
用户界面组件
"""

import os
import platform
import pyperclip
from typing import Optional, List, Tuple
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from .config import AppConfig
from .prompts import UIStrings


class TerminalUI:
    """Terminal UI manager"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.console = Console()
        self.language = config.language
        self.history: List[Tuple[str, str, str]] = []  # (input, output, mode)
        self.session = PromptSession()
        
    def _get_string(self, key: str) -> str:
        """Get localized string"""
        return UIStrings.get(self.language, key)
    
    def show_welcome(self):
        """Display welcome message"""
        title = Text()
        title.append("╔══════════════════════════════════════════════════════════╗\n", style="cyan")
        title.append("║  ", style="cyan")
        title.append("TermAssist", style="bold bright_cyan")
        title.append(" - Terminal AI Command Assistant", style="cyan")
        title.append("  ║\n", style="cyan")
        title.append("╚══════════════════════════════════════════════════════════╝", style="cyan")
        
        subtitle = Text(self._get_string("welcome_sub"), style="dim")
        
        self.console.print()
        self.console.print(Align.center(title))
        self.console.print(Align.center(subtitle))
        self.console.print()
    
    def show_help(self):
        """Display help information"""
        help_text = self._get_string("help")
        panel = Panel(
            help_text,
            title="[bold cyan]TermAssist Help[/bold cyan]",
            border_style="cyan"
        )
        self.console.print(panel)
    
    def show_config(self, llm_config):
        """Display current configuration"""
        table = Table(title=self._get_string("config_title"))
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("LLM Provider", llm_config.provider)
        table.add_row("Model", llm_config.model)
        table.add_row("Temperature", str(llm_config.temperature))
        table.add_row("Max Tokens", str(llm_config.max_tokens))
        table.add_row("Theme", self.config.theme)
        table.add_row("Language", self.config.language)
        table.add_row("Auto Copy", "Yes" if self.config.auto_copy else "No")
        table.add_row("Confirm Before Run", "Yes" if self.config.confirm_before_run else "No")
        
        self.console.print(table)
    
    def show_history(self):
        """Display command history"""
        if not self.history:
            self.console.print(f"[dim]{self._get_string('no_history')}[/dim]")
            return
        
        table = Table(title=self._get_string("history_title"))
        table.add_column("#", style="cyan", width=4)
        table.add_column("Mode", style="magenta", width=12)
        table.add_column("Input", style="green")
        table.add_column("Output", style="yellow")
        
        for i, (input_text, output, mode) in enumerate(self.history[-20:], 1):
            # Truncate long strings
            input_display = input_text[:50] + "..." if len(input_text) > 50 else input_text
            output_display = output[:50] + "..." if len(output) > 50 else output
            table.add_row(str(i), mode, input_display, output_display)
        
        self.console.print(table)
    
    def get_input(self) -> str:
        """Get user input"""
        try:
            prompt_text = f"{self._get_string('input_prompt')}: "
            return self.session.prompt(prompt_text)
        except KeyboardInterrupt:
            return "/exit"
        except EOFError:
            return "/exit"
    
    def show_generating(self):
        """Show generating indicator"""
        return self.console.status(
            f"[cyan]{self._get_string('generating')}[/cyan]",
            spinner="dots"
        )
    
    def show_result(self, result: str, is_command: bool = True):
        """Display result"""
        if is_command:
            # Try to detect shell type
            shell = "bash"
            if platform.system() == "Windows":
                shell = "powershell"
            
            syntax = Syntax(result, shell, theme="monokai", line_numbers=False)
            panel = Panel(
                syntax,
                title=f"[bold cyan]{self._get_string('result')}[/bold cyan]",
                border_style="green"
            )
        else:
            panel = Panel(
                result,
                title=f"[bold cyan]{self._get_string('result')}[/bold cyan]",
                border_style="green"
            )
        
        self.console.print(panel)
        
        # Check for dangerous commands
        if is_command and self._is_dangerous(result):
            self.console.print(f"[bold red]{self._get_string('dangerous_warning')}[/bold red]")
    
    def _is_dangerous(self, command: str) -> bool:
        """Check if command is potentially dangerous"""
        command_lower = command.lower()
        for dangerous in self.config.dangerous_commands:
            if dangerous.lower() in command_lower:
                return True
        return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard"""
        try:
            pyperclip.copy(text)
            self.console.print(f"[green]{self._get_string('copy_success')}[/green]")
            return True
        except Exception:
            self.console.print(f"[red]{self._get_string('copy_fail')}[/red]")
            return False
    
    def confirm_execute(self, command: str) -> bool:
        """Ask user to confirm command execution"""
        if not self.config.confirm_before_run:
            return True
        
        self.console.print(f"\n[yellow]{self._get_string('execute_confirm')}[/yellow]")
        self.console.print(f"[cyan]{command}[/cyan]")
        
        try:
            response = self.session.prompt("(y/n): ").lower().strip()
            return response in ('y', 'yes', '是', '确认')
        except (KeyboardInterrupt, EOFError):
            return False
    
    def add_to_history(self, input_text: str, output: str, mode: str):
        """Add entry to history"""
        if self.config.save_history:
            self.history.append((input_text, output, mode))
            # Keep only last N entries
            if len(self.history) > self.config.max_history:
                self.history = self.history[-self.config.max_history:]
    
    def show_error(self, message: str):
        """Display error message"""
        self.console.print(f"[bold red]Error: {message}[/bold red]")
    
    def show_success(self, message: str):
        """Display success message"""
        self.console.print(f"[bold green]{message}[/bold green]")
    
    def show_info(self, message: str):
        """Display info message"""
        self.console.print(f"[cyan]{message}[/cyan]")
    
    def clear_screen(self):
        """Clear terminal screen"""
        self.console.clear()
        self.show_welcome()
    
    def show_exit(self):
        """Display exit message"""
        self.console.print(f"\n[green]{self._get_string('exit')}![/green]\n")


def detect_shell() -> str:
    """Detect current shell"""
    shell = os.environ.get('SHELL', '')
    if 'bash' in shell:
        return 'bash'
    elif 'zsh' in shell:
        return 'zsh'
    elif 'fish' in shell:
        return 'fish'
    elif platform.system() == 'Windows':
        return 'powershell'
    else:
        return 'bash'


def detect_os() -> str:
    """Detect operating system"""
    system = platform.system()
    if system == 'Darwin':
        return 'macOS'
    elif system == 'Windows':
        return 'Windows'
    elif system == 'Linux':
        return 'Linux'
    else:
        return system
