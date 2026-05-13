#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for config module"""

import unittest
import tempfile
import shutil
from pathlib import Path

from termassist.config import ConfigManager, LLMConfig, AppConfig


class TestConfig(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".config" / "termassist"
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_llm_config_defaults(self):
        """Test LLM config default values"""
        config = LLMConfig()
        self.assertEqual(config.provider, "ollama")
        self.assertEqual(config.model, "llama3.2")
        self.assertIsNone(config.api_key)
        self.assertEqual(config.temperature, 0.3)
    
    def test_app_config_defaults(self):
        """Test app config default values"""
        config = AppConfig()
        self.assertEqual(config.theme, "auto")
        self.assertEqual(config.language, "zh")
        self.assertTrue(config.show_emoji)
        self.assertTrue(config.confirm_before_run)


if __name__ == '__main__':
    unittest.main()
