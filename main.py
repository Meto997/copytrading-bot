from telethon import TelegramClient, events
from googletrans import Translator
import telebot
from flask import Flask, request
import asyncio

# 🔹 Configurazioni principali
API_ID = 25102963  # <--- Il tuo API ID
API_HASH = "1359591d4771a5b58b7b2447ad1dc33e"  # <--- Il tuo API HASH
TOKEN = "7496414589:AAFod8rcFNq137cIQfTJMpmkuiO9Y-uv0YA"
WEBHOOK_URL = "https://75753060-0b9a-4c93-9acd-ffa1183736a0-00-1lxlgxg5mmcek.janeway.replit.dev/"
SOURCE_CHANNEL_ID = -1001199352806  # <-- Canale sorgente
DESTINATION_GROUP_ID = -1002404451506  # <-- Gruppo VIP

# 🔹 Inizializza il bot di Telebot
bot = telebot.TeleBot(TOKEN)
translator = Translator()

# 🔹 Configurazione del server Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Il bot è attivo e funzionante!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_update = request.get_json()
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return "", 200

# 🔹 Configura il Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL + TOKEN)

# 🔹 Funzione per rispondere ai messaggi degli utenti
@bot.message_handler(commands=['start', 'test'])
def send_welcome(message):
    bot.reply_to(message, "✅ Il bot è attivo e funzionante!")

# 🔹 Inizializza il client Telethon con asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient("user_session", API_ID, API_HASH)
client.start()


async def start_telethon():
    await client.start()
    print("🚀 Telethon avviato correttamente!")
    await client.run_until_disconnected()

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID))
async def forward_message(event):
    try:
        original_text = event.message.text
        if not original_text:
            return  # Se il messaggio è vuoto, ignoralo

        print(f"📩 Nuovo messaggio rilevato nel canale sorgente: {original_text}")
        translated_text = translator.translate(original_text, dest="it").text

        if translated_text and translated_text.strip():
            await client.send_message(DESTINATION_GROUP_ID, translated_text)
            print(f"✅ Messaggio tradotto e copiato:\n{translated_text}")
        else:
            print("⚠️ Traduzione fallita o testo vuoto!")
    except Exception as e:
        print(f"❌ Errore nell'inoltro: {e}")

# 🔹 Avvia il server Flask per mantenere il bot attivo
async def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def main():
    flask_task = asyncio.create_task(run_flask())
    telethon_task = asyncio.create_task(start_telethon())
    await asyncio.gather(flask_task, telethon_task)

if __name__ == "__main__":
    asyncio.run(main())
