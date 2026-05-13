#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt templates for TermAssist
提示词模板
"""

from typing import Dict


class Prompts:
    """Multi-language prompt templates"""
    
    SYSTEM_PROMPTS = {
        "zh": """你是一个专业的终端命令助手。你的任务是帮助用户将自然语言描述转换为准确的 shell 命令，或者解释复杂的命令。

规则：
1. 只返回命令本身，不要添加解释（除非用户要求）
2. 优先使用通用的、跨平台的命令
3. 对于危险操作，在命令前添加警告注释
4. 如果涉及多个步骤，按顺序列出所有命令
5. 使用中文注释说明每个命令的作用

当前操作系统: {os_name}
当前 Shell: {shell}""",
        
        "zh-tw": """你是一個專業的終端機命令助手。你的任務是幫助使用者將自然語言描述轉換為準確的 shell 命令，或者解釋複雜的命令。

規則：
1. 只返回命令本身，不要添加解釋（除非使用者要求）
2. 優先使用通用的、跨平台的命令
3.  對於危險操作，在命令前添加警告註釋
4. 如果涉及多個步驟，按順序列出所有命令
5. 使用繁體中文註釋說明每個命令的作用

目前作業系統: {os_name}
目前 Shell: {shell}""",
        
        "en": """You are a professional terminal command assistant. Your task is to help users convert natural language descriptions into accurate shell commands, or explain complex commands.

Rules:
1. Only return the command itself, without explanations (unless requested)
2. Prefer generic, cross-platform commands when possible
3. Add warning comments before dangerous operations
4. If multiple steps are involved, list all commands in order
5. Use comments to explain what each command does

Current OS: {os_name}
Current Shell: {shell}"""
    }
    
    COMMAND_GENERATION_PROMPTS = {
        "zh": """请将以下自然语言描述转换为 shell 命令：

描述: {query}

要求：
1. 返回可直接执行的命令
2. 如果需要多个命令，请用 && 连接或分行列出
3. 在命令前用 # 添加简短的中文说明
4. 如果命令可能有危险，请在前面加上 # ⚠️ 警告

只返回命令，不要其他解释。""",
        
        "zh-tw": """請將以下自然語言描述轉換為 shell 命令：

描述: {query}

要求：
1. 返回可直接執行的命令
2. 如果需要多個命令，請用 && 連接或分行列出
3. 在命令前用 # 添加簡短的繁體中文說明
4. 如果命令可能有危險，請在前面加上 # ⚠️ 警告

只返回命令，不要其他解釋。""",
        
        "en": """Please convert the following natural language description into shell commands:

Description: {query}

Requirements:
1. Return commands ready to execute
2. If multiple commands are needed, use && to connect or list them line by line
3. Add brief comments with # before each command
4. If the command might be dangerous, add # ⚠️ WARNING before it

Return only commands, no other explanations."""
    }
    
    COMMAND_EXPLAIN_PROMPTS = {
        "zh": """请解释以下 shell 命令的作用：

命令: {command}

要求：
1. 解释这个命令的整体功能
2. 分解每个参数和选项的含义
3. 说明可能的输出结果
4. 如果有潜在风险，请指出
5. 提供可能的替代方案（如果有）

用中文回答。""",
        
        "zh-tw": """請解釋以下 shell 命令的作用：

命令: {command}

要求：
1. 解釋這個命令的整體功能
2. 分解每個參數和選項的含義
3. 說明可能的輸出結果
4. 如果有潛在風險，請指出
5. 提供可能的替代方案（如果有）

用繁體中文回答。""",
        
        "en": """Please explain the following shell command:

Command: {command}

Requirements:
1. Explain the overall function of this command
2. Break down the meaning of each parameter and option
3. Describe possible output results
4. Point out potential risks if any
5. Provide possible alternatives if available

Answer in English."""
    }
    
    @classmethod
    def get_system_prompt(cls, lang: str, os_name: str, shell: str) -> str:
        """Get system prompt for specified language"""
        prompt = cls.SYSTEM_PROMPTS.get(lang, cls.SYSTEM_PROMPTS["en"])
        return prompt.format(os_name=os_name, shell=shell)
    
    @classmethod
    def get_generation_prompt(cls, lang: str, query: str) -> str:
        """Get command generation prompt"""
        prompt = cls.COMMAND_GENERATION_PROMPTS.get(lang, cls.COMMAND_GENERATION_PROMPTS["en"])
        return prompt.format(query=query)
    
    @classmethod
    def get_explain_prompt(cls, lang: str, command: str) -> str:
        """Get command explanation prompt"""
        prompt = cls.COMMAND_EXPLAIN_PROMPTS.get(lang, cls.COMMAND_EXPLAIN_PROMPTS["en"])
        return prompt.format(command=command)


class UIStrings:
    """Multi-language UI strings"""
    
    STRINGS = {
        "zh": {
            "welcome": "🚀 欢迎使用 TermAssist - 终端智能命令助手",
            "welcome_sub": "输入自然语言描述生成命令，或输入命令获取解释",
            "input_prompt": "💬 请输入",
            "generating": "🤔 正在思考...",
            "result": "📋 结果",
            "copy_success": "✅ 已复制到剪贴板",
            "copy_fail": "❌ 复制失败",
            "exit": "👋 再见",
            "mode_generate": "生成模式",
            "mode_explain": "解释模式",
            "help": """
[bold]快捷键:[/bold]
  [cyan]Ctrl+C[/cyan] - 退出程序
  [cyan]Ctrl+L[/cyan] - 清屏
  [cyan]/help[/cyan]  - 显示帮助
  [cyan]/config[/cyan] - 配置设置
  [cyan]/history[/cyan] - 查看历史

[bold]使用方式:[/bold]
  1. 直接输入自然语言描述，如："查找当前目录下所有大于100MB的文件"
  2. 输入命令获取解释，如："grep -r 'pattern' ."
            """,
            "config_title": "⚙️  当前配置",
            "history_title": "📜 历史记录",
            "no_history": "暂无历史记录",
            "dangerous_warning": "⚠️  警告：此命令可能存在风险，请谨慎执行！",
            "execute_confirm": "是否执行此命令?",
            "provider_not_available": "❌ LLM 服务不可用，请检查配置",
        },
        "zh-tw": {
            "welcome": "🚀 歡迎使用 TermAssist - 終端機智慧命令助手",
            "welcome_sub": "輸入自然語言描述生成命令，或輸入命令取得解釋",
            "input_prompt": "💬 請輸入",
            "generating": "🤔 正在思考...",
            "result": "📋 結果",
            "copy_success": "✅ 已複製到剪貼簿",
            "copy_fail": "❌ 複製失敗",
            "exit": "👋 再見",
            "mode_generate": "生成模式",
            "mode_explain": "解釋模式",
            "help": """
[bold]快速鍵:[/bold]
  [cyan]Ctrl+C[/cyan] - 退出程式
  [cyan]Ctrl+L[/cyan] - 清除畫面
  [cyan]/help[/cyan]  - 顯示說明
  [cyan]/config[/cyan] - 設定配置
  [cyan]/history[/cyan] - 查看歷史

[bold]使用方式:[/bold]
  1. 直接輸入自然語言描述，如："尋找目前目錄下所有大於100MB的檔案"
  2. 輸入命令取得解釋，如："grep -r 'pattern' ."
            """,
            "config_title": "⚙️  目前配置",
            "history_title": "📜 歷史記錄",
            "no_history": "暫無歷史記錄",
            "dangerous_warning": "⚠️  警告：此命令可能有風險，請謹慎執行！",
            "execute_confirm": "是否執行此命令?",
            "provider_not_available": "❌ LLM 服務無法使用，請檢查配置",
        },
        "en": {
            "welcome": "🚀 Welcome to TermAssist - Terminal AI Command Assistant",
            "welcome_sub": "Enter natural language to generate commands, or enter commands for explanation",
            "input_prompt": "💬 Input",
            "generating": "🤔 Thinking...",
            "result": "📋 Result",
            "copy_success": "✅ Copied to clipboard",
            "copy_fail": "❌ Copy failed",
            "exit": "👋 Goodbye",
            "mode_generate": "Generate Mode",
            "mode_explain": "Explain Mode",
            "help": """
[bold]Shortcuts:[/bold]
  [cyan]Ctrl+C[/cyan] - Exit program
  [cyan]Ctrl+L[/cyan] - Clear screen
  [cyan]/help[/cyan]  - Show help
  [cyan]/config[/cyan] - Configuration
  [cyan]/history[/cyan] - View history

[bold]Usage:[/bold]
  1. Enter natural language description, e.g.: "find all files larger than 100MB"
  2. Enter command for explanation, e.g.: "grep -r 'pattern' ."
            """,
            "config_title": "⚙️  Current Configuration",
            "history_title": "📜 History",
            "no_history": "No history yet",
            "dangerous_warning": "⚠️  Warning: This command may be dangerous, execute with caution!",
            "execute_confirm": "Execute this command?",
            "provider_not_available": "❌ LLM service not available, please check configuration",
        }
    }
    
    @classmethod
    def get(cls, lang: str, key: str) -> str:
        """Get UI string for specified language and key"""
        strings = cls.STRINGS.get(lang, cls.STRINGS["en"])
        return strings.get(key, key)
