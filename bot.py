from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import io

TOKEN = "8409092907:AAFuzckMkZur6ZNeB5tcN63q8Be6hfLI4jY"

def create_sticker(text):
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((60, 180, 452, 350), radius=40, fill=(255, 255, 255, 230))

    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text(((512 - w) / 2, 240), text, fill="black", font=font)

    bio = io.BytesIO()
    bio.name = "sticker.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim teks, aku ubah jadi sticker 😎")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    sticker = create_sticker(text)
    await update.message.reply_sticker(sticker)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot jalan...")
app.run_polling(drop_pending_updates=True)