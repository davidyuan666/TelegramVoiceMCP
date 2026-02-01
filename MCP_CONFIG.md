# MCP 配置指南

本文档说明如何在 Claude Code CLI 中配置 Telegram Voice MCP 服务器。

## 项目说明

本项目是一个 MCP 服务器，为 Claude Code CLI 提供 Telegram 语音消息发送能力。

### 功能

- `send_voice_message`: 将文本转换为语音并发送到 Telegram

### 使用场景

在 Claude Code CLI 中通过自然语言指令发送语音消息到 Telegram。

## 配置步骤

### 第一步：设置环境变量

创建 `.env` 文件：

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

**获取 Bot Token**:
1. 在 Telegram 中找到 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 复制获得的 Token

### 第二步：安装依赖

```bash
cd TelegramVoiceMCP
pip install -r requirements.txt
```

### 第三步：配置 Claude Code CLI

编辑配置文件 `C:\Users\wuxig\.claude.json`，添加以下配置：

```json
{
  "mcpServers": {
    "telegram-voice": {
      "type": "stdio",
      "command": "python",
      "args": [
        "C:/workspace/claudecodelabspace/TelegramVoiceMCP/voice_server.py"
      ],
      "env": {
        "TELEGRAM_BOT_TOKEN": "your_bot_token_here"
      }
    }
  }
}
```

**注意**:
- 将路径替换为你的实际路径
- 将 `your_bot_token_here` 替换为你的实际 Bot Token
- Windows 路径使用正斜杠 `/` 或双反斜杠 `\\`

### 第四步：重启 Claude Code CLI

配置完成后，重启 Claude Code CLI 使配置生效。

## 使用方法

启动 Claude Code CLI 后，可以使用自然语言指令：

**发送中文语音消息**:
```
Send a voice message "你好，这是一条测试语音消息" to Telegram chat ID 751182377
```

**发送英文语音消息**:
```
Send an English voice message "Hello, this is a test" to chat 751182377
```

## 测试

运行测试脚本验证语音生成：

```bash
cd TelegramVoiceMCP
python voice_generator.py
```

这将生成两个测试语音文件：
- 中文测试语音
- 英文测试语音

## 故障排查

### 问题：MCP Server 无法启动

**检查**:
1. 确认 Python 版本 >= 3.10
2. 确认已安装所有依赖：`pip install -r requirements.txt`
3. 确认环境变量 `TELEGRAM_BOT_TOKEN` 已设置
4. 查看 Claude Code CLI 日志

### 问题：无法生成语音

**检查**:
1. 确认 gTTS 库已正确安装
2. 确认网络连接正常（gTTS 需要访问 Google 服务）
3. 检查 voice_cache 目录权限

### 问题：无法发送语音消息

**检查**:
1. Bot Token 是否正确
2. Chat ID 是否正确
3. 机器人是否有发送消息的权限
4. 语音文件是否成功生成

## 技术细节

### 语音生成

- 使用 gTTS (Google Text-to-Speech) 引擎
- 支持语言：中文 (zh-CN)、英文 (en) 等
- 生成格式：MP3
- 缓存目录：`voice_cache/`

### 文件命名

语音文件使用文本内容的 MD5 哈希命名，避免重复生成相同内容的语音。

格式：`voice_{md5_hash}.mp3`

### MCP 工具参数

```json
{
  "chat_id": "string (required)",
  "text": "string (required)",
  "lang": "string (optional, default: zh-CN)"
}
```

## 安全建议

1. **不要将 Bot Token 提交到 Git 仓库**
   - 使用 `.env` 文件存储 Token
   - 确保 `.env` 在 `.gitignore` 中

2. **定期更换 Bot Token**
   - 如果 Token 泄露，立即通过 @BotFather 重新生成

3. **限制机器人权限**
   - 只授予必要的权限
   - 考虑使用白名单限制可以使用机器人的用户

## 相关文档

- [README.md](README.md) - 项目概述
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [python-telegram-bot 文档](https://docs.python-telegram-bot.org/)
- [gTTS 文档](https://gtts.readthedocs.io/)
