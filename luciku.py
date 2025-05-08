import requests
import time
import random
from faker import Faker
from datetime import datetime

# Token Bot Telegram
BOT_TOKEN = "7287175769:AAGTAa5w6cANRQI1QWinCDiS2bqTzXs4w9Q"
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

# Fungsi untuk generate nomor HP Indonesia
def generate_phone_number():
    return f"08{random.randint(1, 9)}{random.randint(100000000, 999999999)}"

# Fungsi untuk generate umur
def calculate_age(birth_date):
    today = datetime.now().date()
    age = (today - birth_date).days // 365  # Calculate age in years
    return age

# Fungsi untuk buat data dummy berdasarkan email
def generate_user_info(email):
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random.choice(['LAKI-LAKI', 'PEREMPUAN'])
    birth_date = fake.date_of_birth(minimum_age=17, maximum_age=60)
    birth_date_str = birth_date.strftime("%Y-%m-%d")
    age = calculate_age(birth_date)

    username_base = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}"

    # Simulate other user info
    nik = str(random.randint(1000000000000000, 9999999999999999))
    provider = random.choice(['TELKOMSEL', 'XL', 'INDOSAT', 'SMARTFREN'])
    address = fake.address().replace("\n", ", ")
    province = fake.state()
    city = fake.city()
    district = fake.city()
    postal_code = random.randint(10000, 99999)
    email = email or f"{first_name.lower()}.{last_name.lower()}@gmail.com"

    # Simulate registration date
    registration_date = fake.date_this_decade(before_today=True, after_today=False).strftime("%Y-%m-%d")

    return {
        "phone": generate_phone_number(),
        "provider": provider,
        "registration_date": registration_date,
        "nik": nik,
        "name": f"{first_name} {last_name}",
        "gender": gender,
        "birth_date": birth_date_str,
        "age": age,
        "province": province,
        "city": city,
        "district": district,
        "postal_code": postal_code,
        "email": email
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
                            f"📱 HASIL PENCARIAN\n\n"
                            f"📞 Nomor: {info['phone']}\n"
                            f"📱 Provider: {info['provider']}\n"
                            f"📅 Tgl Registrasi: {info['registration_date']}\n"
                            f"🆔 NIK: {info['nik']}\n"
                            f"👤 Nama: {info['name']}\n"
                            f"👫 Gender: {info['gender']}\n"
                            f"🎂 Tanggal Lahir: {info['birth_date']}\n"
                            f"🧓 Umur: {info['age']} tahun\n"
                            f"🏠 Provinsi: {info['province']}\n"
                            f"🏙️ Kabupaten/Kota: {info['city']}\n"
                            f"🏘️ Kecamatan: {info['district']}\n"
                            f"📮 Kode Pos: {info['postal_code']}\n"
                            f"✉️ Email: {info['email']}\n"
                        )
                        send_message(chat_id, response)

        time.sleep(1)

if __name__ == "__main__":
    main()
