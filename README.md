🌦️ Tele Weather Bot

A Telegram bot that delivers real-time weather updates and 5-day forecasts for any city. Built with Python and powered by the OpenWeatherMap API.

📦 Features

Get current weather for any city

5-day weather forecast

Simple Telegram commands

Fast and lightweight

Easy to deploy and customize

🛠️ Setup

1. Clone the repository

git clone https://github.com/yoganandansr99/tele_weather_bot.git
cd tele_weather_bot

2. Install dependencies

pip install -r requirements.txt

3. Configure your bot

Create a .env file or update bot.py with:

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

You can get your weather API key from OpenWeatherMap.

4. Run the bot

python bot.py

💬 Commands

/start – Welcome message

/weather <city> – Get current weather for the specified city

/forecast <city> – Get 5-day weather forecast

/help – Show help message

📁 Files

bot.py – Main bot logic

requirements.txt – Python dependencies

.gitignore – Ignore rules

🚀 Future Enhancements

Location-based weather using Telegram geolocation

Weather alerts and notifications

Custom forecast intervals

📄 License

Open-source and free to use. Contributions welcome!
