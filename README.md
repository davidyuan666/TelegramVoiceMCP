# Telegram Voice MCP

通过 MCP (Model Context Protocol) 为 Claude Code CLI 提供 Telegram 语音消息发送能力。

## 功能特性

- 文本转语音 (TTS) - 支持中文和英文
- 通过 Telegram Bot API 发送语音消息
- 自动语音文件缓存
- 完整的 MCP 服务器实现

## 技术栈

- **python-telegram-bot**: Telegram Bot API 封装
- **gTTS**: Google Text-to-Speech 引擎
- **MCP**: Model Context Protocol 服务器框架

## 快速开始

### 1. 安装依赖

```bash
cd TelegramVoiceMCP
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. 配置 Claude Code CLI

参考 [MCP_CONFIG.md](MCP_CONFIG.md) 配置 MCP 服务器。

### 4. 测试

```bash
python voice_generator.py
```

## 项目结构

```
TelegramVoiceMCP/
├── voice_server.py      # MCP 服务器主程序
├── voice_generator.py   # TTS 语音生成器
├── requirements.txt     # Python 依赖
├── .env.example        # 环境变量模板
├── .gitignore          # Git 忽略文件
├── README.md           # 项目说明
└── MCP_CONFIG.md       # MCP 配置指南
```

## MCP 工具

### send_voice_message

发送语音消息到 Telegram。

**参数**:
- `chat_id` (string, required): Telegram 聊天 ID
- `text` (string, required): 要转换为语音的文本
- `lang` (string, optional): 语言代码，默认 "zh-CN"
  - `zh-CN`: 中文
  - `en`: 英文

**示例**:
```
Send a voice message "你好，这是测试语音" to Telegram chat 123456789
```

## 语音生成

使用 Google Text-to-Speech (gTTS) 引擎：
- 支持多语言
- 自动缓存生成的语音文件
- 使用 MD5 哈希避免重复生成

## 安全建议

1. 不要将 `.env` 文件提交到 Git
2. 定期更换 Bot Token
3. 限制机器人权限

## 相关项目

- [TelegramSenderMCP](../TelegramSenderMCP) - 发送文本消息
- [TelegramReceiverMCP](../TelegramReceiverMCP) - 接收消息

## License

MIT
