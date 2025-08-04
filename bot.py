from telegram import Update, KeyboardButton, ReplyKeyboardMarkup,BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters
)
import requests
from datetime import datetime , timedelta
import logging

BOT_TOKEN = "7856875903:AAFtu96gD81lnMjl_DD7sUPhqtYVzNTUGEo"
WEATHER_API_KEY = "28fd5816e6a25174d0f94d5d3ef910b3"


# --- Utils ---
def get_weather_by_city(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    return requests.get(url).json()

def get_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    return requests.get(url).json()
def format_weather(data):
    if data.get("cod") != 200:
        return "❌ City not found."
    name = data["name"]
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].capitalize()
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    feels = data["main"]["feels_like"]
    return f"<b><i>🌤️ Weather in {name}:\nTemp: {temp}°C feels like {feels}°C\nCondition: {desc}\nHumidity: {humidity}%\nWind: {wind} m/s</i></b>"

def format_forecast(data):
    if data.get("cod") != "200":
        return "❌ City not found."

    city = data["city"]["name"]
    msg = f"📅 5-Day Forecast for {city}:\n"
    for i in range(0, 40, 8):  # every 24 hours (8 intervals of 3h)
        d = data["list"][i]
        dt = d["dt_txt"] 
        i_t=datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
        i_t=i_t+timedelta(hours=5,minutes=30)
        dt=i_t.strftime("%d-%m-%Y %H:%M:%S")
        temp = d["main"]["temp"]
        feels = d["main"]["feels_like"]
        desc = d["weather"][0]["description"].capitalize()
        msg += f"\n🕒 {dt}\n🌡️ Temp: {temp}°C feels like {feels}°C\n☁️ {desc}\n"
    msg=f"<b><i>{msg}</i></b>"    
    return msg

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📍 Send Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("<b><i>Welcome! Use /weather [city] or /forecast [city]\nOr tap below to send location and get weather report:</i></b>",parse_mode="HTML", reply_markup=reply_markup)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please provide a city name. Example:\n`/weather London`", parse_mode='Markdown')
        return
    city = " ".join(context.args)
    data = get_weather_by_city(city)
    msg = format_weather(data)
    await update.message.reply_text(msg,parse_mode="HTML")

async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please provide a city name. Example:\n`/forecast London`", parse_mode='Markdown')
        return
    city = " ".join(context.args)
    data = get_forecast(city)
    msg = format_forecast(data)
    await update.message.reply_text(msg,parse_mode="HTML")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    data = get_weather_by_coords(lat, lon)
    msg = format_weather(data)
    await update.message.reply_text(msg,parse_mode="HTML")

async def inv(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<b>INVALID COMMAND , PLS GO >> /help</b>",parse_mode="HTML")   

async def help(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"<b><i> /start  >> to start the bot \n /weather >> to get weather report \n /forecast >> to get 5 days weather report \n send location to get weather report of ur place </i></b>",parse_mode="HTML")

async def message_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<i>for more info pls >> /help</i>",parse_mode="HTML")

async def commonds(app):
    COMMANDS=[
        BotCommand("start","to check wether bot is alive or not"),
        BotCommand("weather","to get weather report"),
        BotCommand("forecast","to get weather forecast upto 5 days"),
        BotCommand("help","to get a help"),
    ]
    await app.bot.set_my_commands(COMMANDS)
# --- Main ---
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("forecast", forecast))
app.add_handler(MessageHandler(filters.LOCATION, handle_location))
app.add_handler(CommandHandler("help",help))
app.add_handler(MessageHandler(filters.COMMAND,inv))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message_handler))

app.post_init = commonds

print("Bot running...")
app.run_polling()
