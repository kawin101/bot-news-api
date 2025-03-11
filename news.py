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
    - ตรวจสอบว่าข่าวที่สุ่มได้ไม่ซ้ำกับของเก่า
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

            # 🔹 อ่านค่าปัจจุบันจาก news.tmp
            old_news = read_old_news()

            # 🔹 พยายามสุ่มข่าวใหม่จนกว่าจะไม่ซ้ำกับข่าวเก่า
            attempts = 10  # จำกัดจำนวนครั้งที่สุ่ม
            for _ in range(attempts):
                selected_article = random.choice(articles)["title"][:20]  # สุ่มข่าวและจำกัด 20 ตัวอักษร
                if selected_article != old_news:
                    return selected_article
            
            return selected_article  # ถ้าสุ่มครบ 10 ครั้งแล้วยังซ้ำ ให้ใช้ค่าสุดท้ายที่สุ่มได้

        return "No news available."
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")
        return None  # คืนค่า None เพื่อให้ไปใช้ข้อความสุ่มแทน

def generate_random_text(length=20):
    """
    สร้างข้อความสุ่มที่มีเฉพาะตัวอักษร A-Z ความยาว 20 ตัวอักษร
    """
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def read_old_news():
    """
    อ่านค่าข้อมูลเก่าจากไฟล์ `news.tmp`
    - ถ้าไฟล์ไม่มีอยู่หรือว่างเปล่า ให้คืนค่าเป็น None
    """
    if os.path.exists("news.tmp"):
        with open("news.tmp", "r", encoding="utf-8") as file:
            content = file.read().strip()
            return content if content else None
    return None

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
    - ตรวจสอบว่าข่าวที่สุ่มมาไม่ซ้ำกับของเก่า
    - แสดงข้อความยืนยันเมื่ออัปเดตเสร็จสิ้น
    """
    
    news = fetch_basketball_news()
    
    if news is None:  # ถ้า API ใช้งานไม่ได้ ให้ใช้ข้อความสุ่มแทน
        news = generate_random_text()

    update_tmp_file(news)  # ลบไฟล์เก่าและเขียนไฟล์ใหม่
    print("news.tmp updated successfully")  # แจ้งเตือนว่าการอัปเดตเสร็จสิ้น
