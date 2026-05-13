<div align="center">

# 🚀 TermAssist

**终端智能命令助手 | Terminal AI Command Assistant | 終端機智慧命令助手**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**TermAssist** 是一款轻量级、智能化的终端命令助手，帮助开发者通过自然语言描述快速生成准确的 Shell 命令，同时也能解释复杂的命令含义。

#### 灵感来源

受 GitHub Trending 上热门的 AI 终端工具（如 VritraAI、Goose、Gemini CLI）启发，但专注于**纯本地运行**和**轻量级设计**，无需复杂的云端依赖。

#### 核心差异化亮点

- 🏠 **纯本地运行** - 支持 Ollama 本地模型，无需联网
- ⚡ **轻量快速** - 单一可执行文件，毫秒级响应
- 🔌 **多 LLM 支持** - 兼容 Ollama、OpenAI、Anthropic
- 🌐 **多语言界面** - 简体中文、繁体中文、English
- 📝 **双向功能** - 自然语言→命令，命令→解释
- 📊 **历史记录** - SQLite 持久化存储，支持搜索

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🤖 **AI 驱动** | 支持多种 LLM 提供商，智能生成命令 |
| 🎯 **自然语言** | 用中文/英文描述需求，自动转换命令 |
| 📖 **命令解释** | 输入复杂命令，获取详细解释 |
| 🎨 **美观 TUI** | 基于 Rich 的现代化终端界面 |
| 🔒 **安全第一** | 危险命令检测，执行前确认 |
| 📋 **剪贴板集成** | 一键复制生成的命令 |
| 🕐 **历史管理** | 自动保存查询历史，支持搜索 |
| ⚙️ **灵活配置** | YAML 配置文件，易于自定义 |

### 🚀 快速开始

#### 环境要求

- Python 3.8+
- 以下 LLM 服务之一：
  - [Ollama](https://ollama.com/) (本地，推荐)
  - OpenAI API Key
  - Anthropic API Key

#### 安装步骤

```bash
# 方式1：从源码安装
git clone https://github.com/gitstq/TermAssist.git
cd TermAssist
pip install -r requirements.txt
pip install -e .

# 方式2：使用安装脚本
chmod +x install.sh
./install.sh
```

#### 配置 LLM

编辑配置文件 `~/.config/termassist/config.yaml`：

**使用 Ollama (推荐，免费本地运行):**
```yaml
llm:
  provider: ollama
  model: llama3.2
  api_base: http://localhost:11434
```

**使用 OpenAI:**
```yaml
llm:
  provider: openai
  model: gpt-4
  api_key: your-api-key-here
```

**使用 Anthropic:**
```yaml
llm:
  provider: anthropic
  model: claude-3-sonnet
  api_key: your-api-key-here
```

#### 启动使用

```bash
# 交互模式
termassist
# 或短别名
tai

# 一次性查询
termassist "查找当前目录下所有大于100MB的文件"

# 解释命令
termassist -e "grep -r 'pattern' ."
```

### 📖 详细使用指南

#### 交互模式命令

| 命令 | 功能 |
|------|------|
| `/help` | 显示帮助信息 |
| `/config` | 查看当前配置 |
| `/history` | 查看历史记录 |
| `/stats` | 查看使用统计 |
| `/clear` | 清屏 |
| `/exit` | 退出程序 |

#### 使用示例

**生成命令:**
```
💬 请输入: 查找最近7天内修改过的所有Python文件
```

**解释命令:**
```
💬 请输入: find . -name "*.py" -mtime -7 -exec grep -l "TODO" {} \;
```

### 💡 设计思路与迭代规划

#### 技术选型原因

- **Python**: 跨平台、生态丰富、开发效率高
- **Rich**: 现代化终端 UI，支持语法高亮和表格
- **SQLite**: 轻量级持久化，无需额外服务
- **Click**: 成熟的 CLI 框架

#### 后续迭代计划

- [ ] 支持更多 LLM 提供商（Gemini、本地模型等）
- [ ] 命令执行结果智能分析
- [ ] 自定义提示词模板
- [ ] 插件系统支持
- [ ] 命令收藏夹功能
- [ ] 团队协作共享

### 📦 打包与部署

```bash
# 构建 Python 包
python -m build

# 构建独立可执行文件
python build.py --exe

# 完整构建流程
python build.py --all
```

### 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 繁體中文

### 🎉 項目介紹

**TermAssist** 是一款輕量級、智慧化的終端機命令助手，幫助開發者透過自然語言描述快速生成準確的 Shell 命令，同時也能解釋複雜的命令含義。

#### 核心差異化亮點

- 🏠 **純本地運行** - 支援 Ollama 本地模型，無需連網
- ⚡ **輕量快速** - 單一可執行檔案，毫秒級響應
- 🔌 **多 LLM 支援** - 相容 Ollama、OpenAI、Anthropic
- 🌐 **多語言介面** - 簡體中文、繁體中文、English
- 📝 **雙向功能** - 自然語言→命令，命令→解釋
- 📊 **歷史記錄** - SQLite 持久化儲存，支援搜尋

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🤖 **AI 驅動** | 支援多種 LLM 提供商，智慧生成命令 |
| 🎯 **自然語言** | 用中文/英文描述需求，自動轉換命令 |
| 📖 **命令解釋** | 輸入複雜命令，獲取詳細解釋 |
| 🎨 **美觀 TUI** | 基於 Rich 的現代化終端介面 |
| 🔒 **安全第一** | 危險命令檢測，執行前確認 |
| 📋 **剪貼簿整合** | 一鍵複製生成的命令 |
| 🕐 **歷史管理** | 自動儲存查詢歷史，支援搜尋 |
| ⚙️ **靈活配置** | YAML 配置檔案，易於自定義 |

### 🚀 快速開始

#### 環境要求

- Python 3.8+
- 以下 LLM 服務之一：
  - [Ollama](https://ollama.com/) (本地，推薦)
  - OpenAI API Key
  - Anthropic API Key

#### 安裝步驟

```bash
git clone https://github.com/gitstq/TermAssist.git
cd TermAssist
pip install -r requirements.txt
pip install -e .
```

#### 啟動使用

```bash
# 互動模式
termassist
# 或短別名
tai

# 一次性查詢
termassist "尋找目前目錄下所有大於100MB的檔案"

# 解釋命令
termassist -e "grep -r 'pattern' ."
```

### 📄 開源協議

本專案採用 [MIT](LICENSE) 協議開源。

---

## English

### 🎉 Introduction

**TermAssist** is a lightweight, intelligent terminal command assistant that helps developers quickly generate accurate Shell commands from natural language descriptions, while also explaining complex command meanings.

#### Key Differentiators

- 🏠 **Local-First** - Supports Ollama local models, no internet required
- ⚡ **Lightning Fast** - Single executable, millisecond response
- 🔌 **Multi-LLM Support** - Compatible with Ollama, OpenAI, Anthropic
- 🌐 **Multi-Language UI** - Simplified Chinese, Traditional Chinese, English
- 📝 **Bidirectional** - Natural language → command, command → explanation
- 📊 **History Management** - SQLite persistence with search support

### ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered** | Multiple LLM providers, intelligent command generation |
| 🎯 **Natural Language** | Describe needs in English/Chinese, auto-convert to commands |
| 📖 **Command Explain** | Input complex commands, get detailed explanations |
| 🎨 **Beautiful TUI** | Modern terminal UI based on Rich |
| 🔒 **Safety First** | Dangerous command detection, confirmation before execution |
| 📋 **Clipboard Integration** | One-click copy generated commands |
| 🕐 **History** | Auto-save query history with search |
| ⚙️ **Flexible Config** | YAML configuration, easy to customize |

### 🚀 Quick Start

#### Requirements

- Python 3.8+
- One of the following LLM services:
  - [Ollama](https://ollama.com/) (local, recommended)
  - OpenAI API Key
  - Anthropic API Key

#### Installation

```bash
git clone https://github.com/gitstq/TermAssist.git
cd TermAssist
pip install -r requirements.txt
pip install -e .
```

#### Usage

```bash
# Interactive mode
termassist
# or short alias
tai

# One-shot query
termassist "find all files larger than 100MB"

# Explain command
termassist -e "grep -r 'pattern' ."
```

### 📄 License

This project is open source under the [MIT](LICENSE) License.

---

<div align="center">

Made with ❤️ by TermAssist Team

</div>
