import os
import yt_dlp
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔒 Bot Token from ENV
BOT_TOKEN = os.getenv("BOT_TOKEN", "7897474464:AAFWfrC39t0dIG9_wdzJgvmUiBUHBIc3NXQ")

# 🎵 Function: Download audio
def download_audio(query: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3'
    }
    os.makedirs("downloads", exist_ok=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        filename = ydl.prepare_filename(info)
        return filename, info.get("title", "Unknown Title")

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎶 Welcome to Music Bot!\nUse /song <name or YouTube URL> to download music.")

# ✅ /song
async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /song <name or YouTube URL>")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"⏳ Downloading: {query} ...")

    try:
        filepath, title = download_audio(query)
        with open(filepath, "rb") as f:
            await update.message.reply_audio(
                audio=InputFile(f),
                title=title,
                caption=f"🎵 {title}"
            )
        os.remove(filepath)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# 🚀 Start Bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", song))
    print("✅ Music Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
