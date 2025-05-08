# ini adalah untuk mengiformasikan data penguna
# jadi harap berjalan dengan lancar ya :)

import requests
import time
import random
from faker import Faker

# Token Bot Telegram
BOT_TOKEN = "123456789:ABCDEF_your_real_token_here"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
fake = Faker('id_ID')

# Fungsi untuk ambil update terbaru
def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(f"{URL}/getUpdates", params=params)
    return response.json()

# Fungsi untuk kirim pesan
def send_message(chat_id, text):
    params = {'chat_id': chat_id, 'text': text}
    requests.post(f"{URL}/sendMessage", params=params)

# Fungsi untuk buat data dummy berdasarkan email
def generate_user_info(email):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username_base = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}"

    return {
        "name": f"{first_name} {last_name}",
        "phone": fake.phone_number(),
        "email": email,
        "nik": str(random.randint(1000000000000000, 9999999999999999)),
        "birth_date": fake.date_of_birth(minimum_age=17, maximum_age=60).strftime("%Y-%m-%d"),
        "address": fake.address().replace("\n", ", "),
        "facebook": f"{first_name} {last_name}",
        "instagram": f"@{username_base}"
    }

# Fungsi utama untuk polling
def main():
    print("Bot berjalan...")
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")

                    if text == "/start":
                        send_message(chat_id, "Selamat datang! Kirim email siapa saja, dan saya coba lacak 😉.")
                    else:
                        info = generate_user_info(text)
                        response = (
                            f"Nama: {info['name']}\n"
                            f"Nomor HP: {info['phone']}\n"
                            f"Email: {info['email']}\n"
                            f"NIK: {info['nik']}\n"
                            f"Tanggal Lahir: {info['birth_date']}\n"
                            f"Alamat: {info['address']}\n"
                            f"Facebook: {info['facebook']}\n"
                            f"Instagram: {info['instagram']}"
                        )
                        send_message(chat_id, response)

        time.sleep(1)

if __name__ == "__main__":
    main()
