#!/usr/bin/env python3
"""
Text-to-Speech Voice Generator
支持中英文文本转语音
"""
import os
from pathlib import Path
from gtts import gTTS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceGenerator:
    """语音生成器"""

    def __init__(self, output_dir: str = "voice_cache"):
        """
        初始化语音生成器

        Args:
            output_dir: 语音文件输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def text_to_speech(self, text: str, lang: str = "zh-CN", filename: str = None) -> str:
        """
        将文本转换为语音文件

        Args:
            text: 要转换的文本
            lang: 语言代码 (zh-CN=中文, en=英文)
            filename: 输出文件名（可选）

        Returns:
            str: 生成的语音文件路径
        """
        try:
            # 自动检测语言
            if not filename:
                import hashlib
                text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                filename = f"voice_{text_hash}.mp3"

            output_path = self.output_dir / filename

            # 生成语音
            logger.info(f"Generating speech for text: {text[:50]}...")
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(str(output_path))

            logger.info(f"Voice file saved: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            raise


if __name__ == "__main__":
    # 测试
    generator = VoiceGenerator()

    # 测试中文
    voice_file = generator.text_to_speech("你好，这是一条测试语音消息。")
    print(f"Generated: {voice_file}")

    # 测试英文
    voice_file_en = generator.text_to_speech("Hello, this is a test voice message.", lang="en")
    print(f"Generated: {voice_file_en}")
