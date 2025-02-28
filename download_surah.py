import os
import requests

# Base folder for Yasser Al-Dosari
folder_path = "Quran_surahs/hazzaa"
os.makedirs(folder_path, exist_ok=True)

# Base URL for downloading (Example: Quranic audio sources like Quran.com API or others)
BASE_URL = "https://surahquran.com/English/hazzaa/"

# Surah list with correct file numbering
surahs = {i: f"{i:03}.mp3" for i in range(1, 115)}  # From Surah 1 (Fatiha) to Surah 114 (Nas)

# Download each Surah
for surah_num, filename in surahs.items():
    file_url = f"{BASE_URL}{filename}"
    file_path = os.path.join(folder_path, filename)

    try:
        print(f"Downloading {filename}...")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Raise error for bad responses (e.g., 404)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"✅ Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {filename}: {e}")

print("📥 All Surahs downloaded successfully!")

"""
QURAN_LIBRARY = {
    reciter: {
        "fatiha": f"Quran_surahs/{reciter}/001.mp3",   # Al-Fatiha
        "baqara": f"Quran_surahs/{reciter}/002.mp3",  # Al-Baqara
        "imran": f"Quran_surahs/{reciter}/003.mp3",   # Al-Imran
        "nisa": f"Quran_surahs/{reciter}/004.mp3",    # An-Nisa
        "maidah": f"Quran_surahs/{reciter}/005.mp3",  # Al-Ma'idah
        "anam": f"Quran_surahs/{reciter}/006.mp3",    # Al-An'am
        "araf": f"Quran_surahs/{reciter}/007.mp3",    # Al-A'raf
        "anfal": f"Quran_surahs/{reciter}/008.mp3",   # Al-Anfal
        "tawba": f"Quran_surahs/{reciter}/009.mp3",   # At-Tawba
        "yunus": f"Quran_surahs/{reciter}/010.mp3",   # Yunus
        "hud": f"Quran_surahs/{reciter}/011.mp3",     # Hud
        "yusuf": f"Quran_surahs/{reciter}/012.mp3",   # Yusuf
        "rad": f"Quran_surahs/{reciter}/013.mp3",     # Ar-Ra'd
        "ibrahim": f"Quran_surahs/{reciter}/014.mp3", # Ibrahim
        "hijr": f"Quran_surahs/{reciter}/015.mp3",    # Al-Hijr
        "nahl": f"Quran_surahs/{reciter}/016.mp3",    # An-Nahl
        "isra": f"Quran_surahs/{reciter}/017.mp3",    # Al-Isra
        "kahf": f"Quran_surahs/{reciter}/018.mp3",    # Al-Kahf
        "maryam": f"Quran_surahs/{reciter}/019.mp3",  # Maryam
        "taha": f"Quran_surahs/{reciter}/020.mp3",    # Ta-Ha
        "anbiya": f"Quran_surahs/{reciter}/021.mp3",  # Al-Anbiya
        "hajj": f"Quran_surahs/{reciter}/022.mp3",    # Al-Hajj
        "muminun": f"Quran_surahs/{reciter}/023.mp3", # Al-Mu'minun
        "nur": f"Quran_surahs/{reciter}/024.mp3",     # An-Nur
        "furqan": f"Quran_surahs/{reciter}/025.mp3",  # Al-Furqan
        "shuara": f"Quran_surahs/{reciter}/026.mp3",  # Ash-Shu'ara
        "naml": f"Quran_surahs/{reciter}/027.mp3",    # An-Naml
        "qasas": f"Quran_surahs/{reciter}/028.mp3",   # Al-Qasas
        "ankabut": f"Quran_surahs/{reciter}/029.mp3", # Al-Ankabut
        "rum": f"Quran_surahs/{reciter}/030.mp3",     # Ar-Rum
        "luqman": f"Quran_surahs/{reciter}/031.mp3",  # Luqman
        "sajda": f"Quran_surahs/{reciter}/032.mp3",   # As-Sajda
        "ahzab": f"Quran_surahs/{reciter}/033.mp3",   # Al-Ahzab
        "saba": f"Quran_surahs/{reciter}/034.mp3",    # Saba
        "fatir": f"Quran_surahs/{reciter}/035.mp3",   # Fatir
        "yaseen": f"Quran_surahs/{reciter}/036.mp3",  # Ya-Sin
        "saffat": f"Quran_surahs/{reciter}/037.mp3",  # As-Saffat
        "sad": f"Quran_surahs/{reciter}/038.mp3",     # Sad
        "zumar": f"Quran_surahs/{reciter}/039.mp3",   # Az-Zumar
        "ghafir": f"Quran_surahs/{reciter}/040.mp3",  # Ghafir
        "fussilat": f"Quran_surahs/{reciter}/041.mp3",# Fussilat
        "shura": f"Quran_surahs/{reciter}/042.mp3",   # Ash-Shura
        "zukhruf": f"Quran_surahs/{reciter}/043.mp3", # Az-Zukhruf
        "dukhan": f"Quran_surahs/{reciter}/044.mp3",  # Ad-Dukhan
        "jathiya": f"Quran_surahs/{reciter}/045.mp3", # Al-Jathiya
        "ahqaf": f"Quran_surahs/{reciter}/046.mp3",   # Al-Ahqaf
        "muhammad": f"Quran_surahs/{reciter}/047.mp3",# Muhammad
        "fath": f"Quran_surahs/{reciter}/048.mp3",    # Al-Fath
        "hujurat": f"Quran_surahs/{reciter}/049.mp3", # Al-Hujurat
        "qaf": f"Quran_surahs/{reciter}/050.mp3",     # Qaf
        "dhariyat": f"Quran_surahs/{reciter}/051.mp3",# Adh-Dhariyat
        "tur": f"Quran_surahs/{reciter}/052.mp3",     # At-Tur
        "najm": f"Quran_surahs/{reciter}/053.mp3",    # An-Najm
        "qamar": f"Quran_surahs/{reciter}/054.mp3",   # Al-Qamar
        "rahman": f"Quran_surahs/{reciter}/055.mp3",  # Ar-Rahman
        "waqia": f"Quran_surahs/{reciter}/056.mp3",   # Al-Waqia
        "hadid": f"Quran_surahs/{reciter}/057.mp3",   # Al-Hadid
        "mujadila": f"Quran_surahs/{reciter}/058.mp3",# Al-Mujadila
        "hashr": f"Quran_surahs/{reciter}/059.mp3",   # Al-Hashr
        "mumtahina": f"Quran_surahs/{reciter}/060.mp3",# Al-Mumtahina
        "saff": f"Quran_surahs/{reciter}/061.mp3",    # As-Saff
        "jumuah": f"Quran_surahs/{reciter}/062.mp3",  # Al-Jumuah
        "munafiqun": f"Quran_surahs/{reciter}/063.mp3",# Al-Munafiqun
        "taghabun": f"Quran_surahs/{reciter}/064.mp3",# At-Taghabun
        "talaq": f"Quran_surahs/{reciter}/065.mp3",   # At-Talaq
        "tahrim": f"Quran_surahs/{reciter}/066.mp3",  # At-Tahrim
        "mulk": f"Quran_surahs/{reciter}/067.mp3",    # Al-Mulk
        "qalam": f"Quran_surahs/{reciter}/068.mp3",   # Al-Qalam
        "haqqa": f"Quran_surahs/{reciter}/069.mp3",   # Al-Haqqa
        "maarij": f"Quran_surahs/{reciter}/070.mp3",  # Al-Maarij
        "nuh": f"Quran_surahs/{reciter}/071.mp3",     # Nuh
        "jinn": f"Quran_surahs/{reciter}/072.mp3",    # Al-Jinn
        "muzammil": f"Quran_surahs/{reciter}/073.mp3",# Al-Muzammil
        "mudathir": f"Quran_surahs/{reciter}/074.mp3",# Al-Mudathir
        "qiyama": f"Quran_surahs/{reciter}/075.mp3",  # Al-Qiyama
        "insan": f"Quran_surahs/{reciter}/076.mp3",   # Al-Insan
        "mursalat": f"Quran_surahs/{reciter}/077.mp3",# Al-Mursalat
        "naba": f"Quran_surahs/{reciter}/078.mp3",    # An-Naba
        "naziat": f"Quran_surahs/{reciter}/079.mp3",  # An-Naziat
        "abasa": f"Quran_surahs/{reciter}/080.mp3",   # Abasa
        "takwir": f"Quran_surahs/{reciter}/081.mp3",  # At-Takwir
        "infitar": f"Quran_surahs/{reciter}/082.mp3", # Al-Infitar
        "mutaffifin": f"Quran_surahs/{reciter}/083.mp3",# Al-Mutaffifin
        "inshiqaq": f"Quran_surahs/{reciter}/084.mp3",# Al-Inshiqaq
        "burooj": f"Quran_surahs/{reciter}/085.mp3",  # Al-Burooj
        "tariq": f"Quran_surahs/{reciter}/086.mp3",   # At-Tariq
        "ala": f"Quran_surahs/{reciter}/087.mp3",     # Al-Ala
        "ghashiya": f"Quran_surahs/{reciter}/088.mp3",# Al-Ghashiya
        "fajr": f"Quran_surahs/{reciter}/089.mp3",    # Al-Fajr
        "balad": f"Quran_surahs/{reciter}/090.mp3",   # Al-Balad
        "shams": f"Quran_surahs/{reciter}/091.mp3",   # Ash-Shams
        "layl": f"Quran_surahs/{reciter}/092.mp3",    # Al-Layl
        "duha": f"Quran_surahs/{reciter}/093.mp3",    # Ad-Duha
        "sharh": f"Quran_surahs/{reciter}/094.mp3",   # Al-Inshirah (Ash-Sharh)
        "tin": f"Quran_surahs/{reciter}/095.mp3",     # At-Tin
        "alaq": f"Quran_surahs/{reciter}/096.mp3",    # Al-Alaq
        "qadr": f"Quran_surahs/{reciter}/097.mp3",    # Al-Qadr
        "bayyina": f"Quran_surahs/{reciter}/098.mp3", # Al-Bayyina
        "zilzal": f"Quran_surahs/{reciter}/099.mp3",  # Az-Zalzala
        "adiyat": f"Quran_surahs/{reciter}/100.mp3",  # Al-Adiyat
        "qariah": f"Quran_surahs/{reciter}/101.mp3",  # Al-Qaria
        "takathur": f"Quran_surahs/{reciter}/102.mp3",# At-Takathur
        "asr": f"Quran_surahs/{reciter}/103.mp3",     # Al-Asr
        "humazah": f"Quran_surahs/{reciter}/104.mp3", # Al-Humazah
        "fil": f"Quran_surahs/{reciter}/105.mp3",     # Al-Fil
        "quraish": f"Quran_surahs/{reciter}/106.mp3", # Quraysh
        "maun": f"Quran_surahs/{reciter}/107.mp3",    # Al-Ma'un
        "kawthar": f"Quran_surahs/{reciter}/108.mp3", # Al-Kawthar
        "kafirun": f"Quran_surahs/{reciter}/109.mp3", # Al-Kafirun
        "nasr": f"Quran_surahs/{reciter}/110.mp3",    # An-Nasr
        "masad": f"Quran_surahs/{reciter}/111.mp3",   # Al-Masad
        "ikhlas": f"Quran_surahs/{reciter}/112.mp3",  # Al-Ikhlas
        "falaq": f"Quran_surahs/{reciter}/113.mp3",   # Al-Falaq
        "nas": f"Quran_surahs/{reciter}/114.mp3"      # An-Nas
    }
    for reciter in RECITERS.keys()
}
"""