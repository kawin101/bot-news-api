import os
import requests
import random
import string

# 🔹 โหลด API Key จาก GitHub Secrets
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# 🔹 ใช้ `top-headlines` และเรียงตามเวลาที่เผยแพร่ (`publishedAt`)
API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_basketball_news():
    """
    ดึงข้อมูลข่าวจาก NewsAPI และเลือกข่าวที่ไม่ซ้ำกับข่าวเก่า
    - อ่านข่าวเก่าจาก `news.tmp`
    - คัดกรองข่าวใหม่ที่ไม่ซ้ำ
    - ถ้าทุกข่าวซ้ำ → ใช้ข้อความสุ่มแทน
    """
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}
    params = {"category": "sports", "q": "basketball", "language": "en", "sortBy": "publishedAt"}
    
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])

        if articles:
            old_news = read_old_news()

            # 🔹 คัดกรองข่าวใหม่ที่ไม่ซ้ำกับของเก่า
            unique_articles = [a["title"][:20] for a in articles if a["title"][:20] != old_news]

            if unique_articles:
                return random.choice(unique_articles)  # 🔹 สุ่มจากข่าวที่ไม่ซ้ำ

    return generate_random_text()  # 🔹 ถ้าข่าวทั้งหมดซ้ำ หรือ API มีปัญหา → ใช้ข้อความสุ่มแทน

def generate_random_text(length=20):
    """สร้างข้อความสุ่ม A-Z ความยาว 20 ตัวอักษร"""
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def read_old_news():
    """อ่านค่าข้อมูลเก่าจากไฟล์ `news.tmp`"""
    if os.path.exists("news.tmp"):
        with open("news.tmp", "r", encoding="utf-8") as file:
            return file.read().strip()
    return None

def update_tmp_file(content):
    """เขียนทับไฟล์ `news.tmp` ด้วยข้อมูลใหม่"""
    with open("news.tmp", "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == "__main__":
    news = fetch_basketball_news()
    update_tmp_file(news)
    print("news.tmp updated successfully")
