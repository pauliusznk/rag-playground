from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from openai import OpenAI
import os
import ffmpeg


class TelegramBot:
    def __init__(self, assistant):
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.assistant = assistant

    async def handle_text(self, update, context):
        question = update.message.text
        await self.reply_with_answer(update, question)

    async def handle_voice(self, update, context):
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")
        base_name = f"voice-{timestamp}"
        temp_dir = "../temp"
        ogg_path = os.path.join(temp_dir, f"{base_name}.ogg")
        wav_path = os.path.join(temp_dir, f"{base_name}.wav")

        # Create temp directory if it doesn't exist
        os.makedirs(temp_dir, exist_ok=True)

        await file.download_to_drive(ogg_path)

        try:
            ffmpeg.input(ogg_path).output(wav_path).run(quiet=True, overwrite_output=True)
        except Exception as e:
            print("FFmpeg error:", e)
            await update.message.reply_text("Failed to process audio.")
            return
        
        client = OpenAI()
        with open(wav_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=audio_file)

        question = transcript.text
        print(f"Transcription: {question}")
        await self.reply_with_answer(update, question)

        os.remove(ogg_path)
        os.remove(wav_path)
        
    async def reply_with_answer(self, update, question):
        answer = self.assistant.generate(question)
        await update.message.reply_text(answer)

    def run(self):
        app = ApplicationBuilder().token(self.telegram_token).build()
        app.add_handler(MessageHandler(filters.TEXT, self.handle_text))
        app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        print("Bot is running")
        app.run_polling()
