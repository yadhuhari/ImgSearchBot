import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Replace with your actual bot token
BOT_TOKEN = "7327597712:AAHLJycT8fIncE_458c9MlxowKKrk5K62aU"

bot = telebot.TeleBot(BOT_TOKEN)

def search_images(query, num_results=10):
    """Searches Google Images for images matching the given query.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of results to retrieve. Defaults to 10.

    Returns:
        list: A list of image URLs.
    """

    search_url = f"https://www.google.com/search?q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwi59YqX0ML7AhWRgZUCHf8gA_oQ_AUoAnoECAEQBA&biw=1920&bih=937&dpr=1"

    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        image_results = soup.find_all('img', {'class': 'rg_i Q4LuWd'})

        image_urls = [urljoin(search_url, img['src']) for img in image_results[:num_results]]

        return image_urls

    except Exception as e:
        print(f"Error searching for images: {e}")
        return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        chat_id=message.chat.id,
        photo=random.choice(PICS)
        caption="Welcome to Image Search Bot! ```Send me a search query and I'll find images for you.```"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    image_urls = search_images(query)

    if image_urls:
        for url in image_urls:
            bot.send_photo(chat_id=message.chat.id, photo=url)
    else:
        bot.send_message(chat_id=message.chat.id, text="No images found for that query.")

bot.polling()
