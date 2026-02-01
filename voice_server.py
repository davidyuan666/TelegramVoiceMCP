#!/usr/bin/env python3
"""
Telegram Voice MCP Server
提供 Telegram 语音消息发送能力的 MCP 服务器
"""
import asyncio
import logging
import os
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from telegram import Bot
from telegram.error import TelegramError
from voice_generator import VoiceGenerator

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 MCP 服务器
app = Server("telegram-voice")

# Telegram bot 实例
bot: Bot | None = None
voice_gen: VoiceGenerator | None = None


def get_bot() -> Bot:
    """获取或创建 Telegram bot 实例"""
    global bot
    if bot is None:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        bot = Bot(token=token)
    return bot


def get_voice_generator() -> VoiceGenerator:
    """获取或创建语音生成器实例"""
    global voice_gen
    if voice_gen is None:
        voice_gen = VoiceGenerator()
    return voice_gen


async def send_voice_message(arguments: dict) -> list[TextContent]:
    """发送语音消息到 Telegram"""
    chat_id = arguments.get("chat_id")
    text = arguments.get("text")
    lang = arguments.get("lang", "zh-CN")

    if not chat_id or not text:
        return [TextContent(type="text", text="Error: chat_id and text are required")]

    try:
        # 生成语音文件
        generator = get_voice_generator()
        voice_file = generator.text_to_speech(text, lang=lang)

        # 发送语音消息
        telegram_bot = get_bot()
        with open(voice_file, 'rb') as audio:
            message = await telegram_bot.send_voice(chat_id=chat_id, voice=audio)

        result = f"Voice message sent successfully!\nChat ID: {message.chat_id}\nMessage ID: {message.message_id}"
        return [TextContent(type="text", text=result)]
    except TelegramError as e:
        return [TextContent(type="text", text=f"Telegram error: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的 Telegram 语音工具"""
    return [
        Tool(
            name="send_voice_message",
            description="Send a voice message to Telegram using text-to-speech",
            inputSchema={
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "string",
                        "description": "Telegram chat ID"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to convert to speech"
                    },
                    "lang": {
                        "type": "string",
                        "description": "Language code (zh-CN for Chinese, en for English)",
                        "default": "zh-CN"
                    }
                },
                "required": ["chat_id", "text"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    try:
        if name == "send_voice_message":
            return await send_voice_message(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """运行 MCP 服务器"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())



