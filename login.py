from telethon.sync import TelegramClient

# INSERISCI LE TUE CREDENZIALI API DI TELEGRAM
API_ID = 25102963  
API_HASH = "1359591d4771a5b58b7b2447ad1dc33e"

# AVVIA L'AUTENTICAZIONE MANUALE
client = TelegramClient("manual_session", API_ID, API_HASH)

client.start()
print("✅ Autenticazione completata con successo!")

client.disconnect()
