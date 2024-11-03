# My_toking_bot
import telebot
from openai import OpenAI

import requests

# Инициализация клиента API OpenAI с API ключом

client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Список для хранения истории разговора
conversation_history = []

# Инициализация Telegram бота
# Ключи вставляю для бота tg01bot weather @TG01wetherbot:
bot = telebot.TeleBot("7904269589:AAF_Cbn-HswNllR6O8J7obwgbWh59KxR5cI")


# Функция для получения погоды
def get_weather(city):
    api_key = '18296f86db52c8ed138347556f734ec2'  # Замените на ваш API ключ OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Температура в {city}: {temperature}°C, {description}."
    else:
        return "Город не найден."


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Получение текстового сообщения от пользователя
    user_input = message.text

    # Добавление ввода пользователя в историю разговора
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Отправка запроса в нейронную сеть
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=conversation_history
        )

        # Извлечение и вывод ответа нейронной сети
        ai_response_content = chat_completion.choices[0].message.content
        bot.reply_to(message, "AI: " + ai_response_content)

        # Добавление ответа нейронной сети в историю разговора
        conversation_history.append({"role": "assistant", "content": ai_response_content})

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: " + str(e))

 # Проверка, является ли ввод пользователя командой для получения погоды
    if user_input.startswith("/weather "):
        city = user_input.split("/weather ")[1]  # Извлекаем название города
        weather_info = get_weather(city)
        bot.reply_to(message, weather_info)
    else:
        # Добавление ввода пользователя в историю разговора
        conversation_history.append({"role": "user", "content": user_input})

        try:
            # Отправка запроса в нейронную сеть
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=conversation_history
            )

            # Извлечение и вывод ответа нейронной сети
            ai_response_content = chat_completion.choices[0].message.content
            bot.reply_to(message, "AI: " + ai_response_content)

            # Добавление ответа нейронной сети в историю разговора
            conversation_history.append({"role": "assistant", "content": ai_response_content})

        except Exception as e:
            bot.reply_to(message, "Произошла ошибка: " + str(e))


bot.polling()


