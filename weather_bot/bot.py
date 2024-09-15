import os
import logging
import requests
import telebot
from telebot import types
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
bot_token = os.getenv("bot_token")
weather_token = os.getenv("wapi_token")

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_token)

def get_weather(city, api_token):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_token,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather = {
            'city': data['name'],
            'temp': data['main']['temp'],
            'pressure': data['main']['pressure'],
            'icon': data['weather'][0]['icon'],  # Иконка погоды
            'description': data['weather'][0]['description']  # Описание погоды
        }
        return weather
    else:
        raise Exception(f"Ошибка: {data.get('message', 'Не удалось получить данные о погоде')}")

#командa /start
@bot.message_handler(commands=['start'])
def start(message):
	logger.info(f"Received /start command from user: {message.from_user.id}")
	bot.send_message(message.chat.id, "Привет! Я бот, который показывает погоду. Напиши мне название города и я найду погоду в нем.")


# Обработчик для запроса погоды по городу
@bot.message_handler(content_types=['text'])
def get_city_weather(message):
    city = message.text.strip()
    logger.info(f"Received weather request for city: {city} from user: {message.from_user.id}")
    try:
        weather = get_weather(city, weather_token)
        response = (f"Город: {weather['city']}\n"
                    f"Температура: {weather['temp']}°C\n"
                    f"Давление: {weather['pressure']} hPa\n"
                    f"Погода: {weather['description']}\n"
                    f"Иконка: http://openweathermap.org/img/wn/{weather['icon']}@2x.png")
    except Exception as e:
        response = f"Не удалось получить данные о погоде для города {city}. Проверьте правильность названия и попробуйте снова."
        logger.error(f"Error fetching weather for {city}: {e}")
    
    bot.send_message(message.chat.id, response)

#командa/location
@bot.message_handler(commands=['location'])
def send_location(message):
    bot.send_location(message.chat.id, latitude=53.9, longitude=27.5667)  # Пример координат для Минска, Беларусь
    logger.info(f"Sent location to user: {message.from_user.id}")

# Обработчик команды /cities для отображения кнопок с городами
@bot.message_handler(commands=['cities'])
def send_cities_keyboard(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Минск')
    itembtn2 = types.KeyboardButton('Москва')
    itembtn3 = types.KeyboardButton('Лондон')
    itembtn4 = types.KeyboardButton('Нью-Йорк')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=markup)
    logger.info(f"Displayed city keyboard to user: {message.from_user.id}")

# Запуск бота
if __name__ == '__main__':
    logger.info("Bot started")
    bot.infinity_polling()
