#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for LLM client module"""

import unittest
from unittest.mock import Mock, patch

from termassist.llm_client import (
    OllamaClient, OpenAIClient, AnthropicClient,
    create_llm_client
)
from termassist.config import LLMConfig


class TestLLMClients(unittest.TestCase):
    """Test LLM client implementations"""
    
    def test_ollama_client_creation(self):
        """Test Ollama client creation"""
        config = LLMConfig(provider="ollama", model="llama3.2")
        client = create_llm_client(config)
        self.assertIsInstance(client, OllamaClient)
    
    def test_openai_client_creation(self):
        """Test OpenAI client creation"""
        config = LLMConfig(provider="openai", model="gpt-4")
        client = create_llm_client(config)
        self.assertIsInstance(client, OpenAIClient)
    
    def test_anthropic_client_creation(self):
        """Test Anthropic client creation"""
        config = LLMConfig(provider="anthropic", model="claude-3")
        client = create_llm_client(config)
        self.assertIsInstance(client, AnthropicClient)
    
    def test_unsupported_provider(self):
        """Test unsupported provider raises error"""
        config = LLMConfig(provider="unsupported")
        with self.assertRaises(ValueError):
            create_llm_client(config)


if __name__ == '__main__':
    unittest.main()
