
import telebot
from telebot import types

# ضع التوكن الخاص بك هنا
TOKEN = "8520931817:AAG9EHInoA4cNmg9BL185TVughxC5DPt40Q"

bot = telebot.TeleBot(TOKEN)

# قاموس لحفظ العداد
user_counts = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_counts[user_id] = 0
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # سنستخدم كلمات بسيطة جداً للأزرار
    btn1 = types.KeyboardButton('سبحان الله')
    btn2 = types.KeyboardButton('الحمد لله')
    btn3 = types.KeyboardButton('الله أكبر')
    btn4 = types.KeyboardButton('أستغفر الله')
    btn5 = types.KeyboardButton('العداد 📊')
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(user_id, "✨ مرحباً بك في بوت التسبيح ✨\nاضغط على الأذكار بالأسفل:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_id = message.chat.id
    if user_id not in user_counts:
        user_counts[user_id] = 0

    # التحقق من النص المكتوب
    text = message.text
    
    if text == 'العداد 📊':
        bot.send_message(user_id, f"عدد أذكارك الحالي: {user_counts[user_id]}")
    
    elif text in ['سبحان الله', 'الحمد لله', 'الله أكبر', 'أستغفر الله']:
        user_counts[user_id] += 1
        bot.send_message(user_id, f"تقبل الله منك! (المجموع: {user_counts[user_id]})")
    
    else:
        bot.send_message(user_id, "من فضلك استخدم الأزرار الموجودة بالأسفل.")

print("البوت بدأ العمل.. جربه الآن في تلجرام!")
bot.infinity_polling()
