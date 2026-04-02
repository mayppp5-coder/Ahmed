import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ---------------------- التوكن ----------------------
BOT_TOKEN = "8646400281:AAFQAejRPcDfpGnBreUFziNzix0m7D8DKuA"
users_file = "users.txt"

# ---------------------- إعدادات التحميل ----------------------
def get_ydl_opts(is_audio=False, platform="youtube"):
    cookies_file = None
    if platform == "instagram" and os.path.exists("cookies_instagram.txt"):
        cookies_file = "cookies_instagram.txt"
    elif platform == "youtube" and os.path.exists("cookies_youtube.txt"):
        cookies_file = "cookies_youtube.txt"

    if is_audio:
        return {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}],
            'cookiefile': cookies_file,
            'user_agent': 'Mozilla/5.0'
        }
    else:
        return {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'video.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cookiefile': cookies_file,
            'user_agent': 'Mozilla/5.0'
        }

# ---------------------- تحميل الفيديو / الصوت ----------------------
def download(url, is_audio=False):
    # تحديد المنصة تلقائيًا
    if "instagram.com" in url:
        platform = "instagram"
    elif "youtube.com" in url or "youtu.be" in url:
        platform = "youtube"
    else:
        platform = "other"  # تيك توك / فيسبوك / غير مدعوم

    ydl_opts = get_ydl_opts(is_audio, platform)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

# ---------------------- إدارة المستخدمين ----------------------
def save_user(user_id):
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            users = f.read().splitlines()
    else:
        users = []
    if str(user_id) not in users:
        users.append(str(user_id))
        with open(users_file, "w") as f:
            f.write("\n".join(users))

def get_user_count():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return len(f.read().splitlines())
    return 0

# ---------------------- /start ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.message.from_user.id)
    text = (
        "🛡️ هـلا بـيـك يـا  فـي بـوت  فـزعـة  🛡️\n\n"
        "أنا فزعتك لتحميل أي فيديو يخطر ببالك من:\n"
        "تيك توك 🎶 | إنستقرام 📸 | يوتيوب 🎥 | فيسبوك 💙\n\n"
        "🚀 طريقة الاستخدام:\n"
        "أرسل الرابط هنا.. واترك الباقي على فزعة!"
    )
    keyboard = [
        [InlineKeyboardButton("🔴 تحميل فيديو", callback_data='video')],
        [InlineKeyboardButton("🔵 تحميل صوت", callback_data='audio')]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------------- التعامل مع الأزرار ----------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "audio":
        context.user_data['audio'] = True
        await query.edit_message_text("🔵 أرسل الرابط لتحويله إلى صوت")
    else:
        context.user_data['audio'] = False
        await query.edit_message_text("🔴 أرسل الرابط لتحميل الفيديو")

# ---------------------- استقبال الرابط ----------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    is_audio = context.user_data.get("audio", False)
    msg = await update.message.reply_text(
        "⏳ جاري الفزعة.. يتم الآن تجهيز ملفك\nيرجى الانتظار قليلاً حسب حجم الملف.."
    )
    try:
        file = download(url, is_audio)
        if is_audio:
            await update.message.reply_audio(audio=open(file, "rb"))
        else:
            await update.message.reply_video(video=open(file, "rb"))
        os.remove(file)
    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("❌ فشل التحميل أو الرابط غير مدعوم")
    await msg.delete()

# ---------------------- /stats ----------------------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = get_user_count()
    await update.message.reply_text(f"👥 عدد مستخدمي بوت فزعة: {count}")

# ---------------------- تشغيل البوت ----------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ بوت فزعة يعمل الآن...")
app.run_polling()
