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
    ดึงข้อมูลข่าวกีฬาบาสเกตบอลจาก NewsAPI
    - ใช้ `sortBy=publishedAt` เพื่อให้ได้ข่าวใหม่ล่าสุด
    - สุ่มเลือกข่าว 1 ข่าวจากรายการ แทนการเลือกข่าวแรกเสมอ
    - ถ้าดึงข่าวไม่ได้ คืนค่า None เพื่อใช้ข้อความสุ่มแทน
    """
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}
    params = {
        "category": "sports",
        "q": "basketball",
        "language": "en",
        "sortBy": "publishedAt"  # เรียงตามเวลาที่เผยแพร่
    }

    response = requests.get(API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data and "articles" in data and data["articles"]:
            articles = data["articles"]
            selected_article = random.choice(articles)  # 🔹 สุ่มเลือกข่าวจากรายการ
            return selected_article["title"][:20]  # จำกัดความยาว 20 ตัวอักษร
        return "No news available."
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")
        return None  # คืนค่า None เพื่อให้ไปใช้ข้อความสุ่มแทน

def generate_random_text(length=20):
    """
    สร้างข้อความสุ่มที่มีเฉพาะตัวอักษร A-Z ความยาว 20 ตัวอักษร
    """
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def update_tmp_file(content):
    """
    ลบไฟล์ `news.tmp` ก่อน แล้วสร้างไฟล์ใหม่พร้อมเขียนข้อมูล
    - ป้องกันปัญหาข้อมูลเก่าอยู่ในไฟล์
    """
    if os.path.exists("news.tmp"):
        os.remove("news.tmp")  # ลบไฟล์เก่าถ้ามีอยู่

    with open("news.tmp", "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == "__main__":
    """
    จุดเริ่มต้นของโปรแกรม
    - ดึงข่าวกีฬาบาสเกตบอลจาก NewsAPI
    - ถ้าดึงข่าวไม่ได้ ให้สร้างข้อความสุ่มแทน
    - ลบไฟล์ `news.tmp` แล้วสร้างใหม่เสมอ
    - แสดงข้อความยืนยันเมื่ออัปเดตเสร็จสิ้น
    """
    
    news = fetch_basketball_news()
    
    if news is None:  # ถ้า API ใช้งานไม่ได้ ให้ใช้ข้อความสุ่มแทน
        news = generate_random_text()

    update_tmp_file(news)  # ลบไฟล์เก่าและเขียนไฟล์ใหม่
    print("news.tmp updated successfully")  # แจ้งเตือนว่าการอัปเดตเสร็จสิ้น
