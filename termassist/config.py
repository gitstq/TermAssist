#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for TermAssist
配置管理模块
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class LLMConfig:
    """LLM provider configuration"""
    provider: str = "ollama"  # ollama, openai, anthropic
    model: str = "llama3.2"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 2048


@dataclass
class AppConfig:
    """Application configuration"""
    # UI settings
    theme: str = "auto"  # auto, dark, light
    language: str = "zh"  # zh, en, zh-tw
    show_emoji: bool = True
    
    # Behavior settings
    auto_copy: bool = False
    confirm_before_run: bool = True
    save_history: bool = True
    max_history: int = 100
    
    # Safety settings
    dangerous_commands: list = None
    
    def __post_init__(self):
        if self.dangerous_commands is None:
            self.dangerous_commands = [
                "rm -rf /", "rm -rf /*", "> /dev/sda", "dd if=/dev/zero",
                "mkfs.", "fdisk", "format", "del /f /s /q",
            ]


class ConfigManager:
    """Configuration manager"""
    
    DEFAULT_CONFIG = {
        "llm": {
            "provider": "ollama",
            "model": "llama3.2",
            "api_key": None,
            "api_base": None,
            "temperature": 0.3,
            "max_tokens": 2048,
        },
        "app": {
            "theme": "auto",
            "language": "zh",
            "show_emoji": True,
            "auto_copy": False,
            "confirm_before_run": True,
            "save_history": True,
            "max_history": 100,
            "dangerous_commands": [
                "rm -rf /", "rm -rf /*", "> /dev/sda", "dd if=/dev/zero",
                "mkfs.", "fdisk", "format", "del /f /s /q",
            ],
        }
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "termassist"
        self.config_file = self.config_dir / "config.yaml"
        self.llm = LLMConfig()
        self.app = AppConfig()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self._apply_config(data)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                self._save_default_config()
        else:
            self._save_default_config()
    
    def _apply_config(self, data: Dict[str, Any]):
        """Apply loaded configuration"""
        if "llm" in data:
            llm_data = data["llm"]
            self.llm = LLMConfig(
                provider=llm_data.get("provider", "ollama"),
                model=llm_data.get("model", "llama3.2"),
                api_key=llm_data.get("api_key"),
                api_base=llm_data.get("api_base"),
                temperature=llm_data.get("temperature", 0.3),
                max_tokens=llm_data.get("max_tokens", 2048),
            )
        
        if "app" in data:
            app_data = data["app"]
            self.app = AppConfig(
                theme=app_data.get("theme", "auto"),
                language=app_data.get("language", "zh"),
                show_emoji=app_data.get("show_emoji", True),
                auto_copy=app_data.get("auto_copy", False),
                confirm_before_run=app_data.get("confirm_before_run", True),
                save_history=app_data.get("save_history", True),
                max_history=app_data.get("max_history", 100),
                dangerous_commands=app_data.get("dangerous_commands"),
            )
    
    def _save_default_config(self):
        """Save default configuration"""
        self.save_config()
    
    def save_config(self):
        """Save current configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        config_data = {
            "llm": {
                "provider": self.llm.provider,
                "model": self.llm.model,
                "api_key": self.llm.api_key,
                "api_base": self.llm.api_base,
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens,
            },
            "app": {
                "theme": self.app.theme,
                "language": self.app.language,
                "show_emoji": self.app.show_emoji,
                "auto_copy": self.app.auto_copy,
                "confirm_before_run": self.app.confirm_before_run,
                "save_history": self.app.save_history,
                "max_history": self.app.max_history,
                "dangerous_commands": self.app.dangerous_commands,
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    
    def get_llm_config(self) -> LLMConfig:
        """Get LLM configuration"""
        return self.llm
    
    def get_app_config(self) -> AppConfig:
        """Get app configuration"""
        return self.app
    
    def update_llm_config(self, **kwargs):
        """Update LLM configuration"""
        for key, value in kwargs.items():
            if hasattr(self.llm, key):
                setattr(self.llm, key, value)
        self.save_config()
    
    def update_app_config(self, **kwargs):
        """Update app configuration"""
        for key, value in kwargs.items():
            if hasattr(self.app, key):
                setattr(self.app, key, value)
        self.save_config()


# Global config instance
config = ConfigManager()
