import os
import requests
import random
import string

# 🔹 โหลด API Key จาก GitHub Secrets (ค่าเก็บไว้ใน Environment Variable ของ GitHub Actions)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# 🔹 ใช้ `top-headlines` endpoint ของ NewsAPI เพื่อดึงข่าวฟรี
API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_basketball_news():
    """
    ดึงข้อมูลข่าวกีฬาบาสเกตบอลจาก NewsAPI
    - ใช้ `Authorization` header เพื่อยืนยันตัวตนผ่าน API Key
    - ใช้ query parameters:
      - category = "sports"  → กรองเฉพาะข่าวหมวดกีฬา
      - q = "basketball"     → ค้นหาข่าวที่เกี่ยวข้องกับบาสเกตบอล
      - language = "en"      → กรองเฉพาะข่าวภาษาอังกฤษ
    - จำกัดความยาวหัวข้อข่าวไว้ที่ 20 ตัวอักษร
    - หาก API ใช้งานไม่ได้หรือไม่มีข่าว จะ return `None`
    """
    
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}  # ส่ง API Key ผ่าน Header
    params = {
        "category": "sports",
        "q": "basketball",
        "language": "en"
    }

    response = requests.get(API_URL, headers=headers, params=params)  # ส่ง request ไปยัง API
    
    if response.status_code == 200:  # ตรวจสอบว่าคำขอสำเร็จหรือไม่ (HTTP 200 OK)
        data = response.json()  # แปลง response JSON เป็น dictionary
        if data and "articles" in data and data["articles"]:  # ตรวจสอบว่ามีข่าวอยู่จริงหรือไม่
            return data["articles"][0]["title"][:20]  # ดึงหัวข้อข่าวแรกสุด และจำกัดที่ 20 ตัวอักษร
        return "No news available."  # ถ้าไม่มีข่าวให้แสดงข้อความนี้แทน
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")  # แสดงข้อความ Error
        return None  # คืนค่า None เพื่อให้ไปใช้ข้อความสุ่มแทน

def generate_random_text(length=20):
    """
    สร้างข้อความสุ่มที่มีเฉพาะตัวอักษร A-Z ความยาว 20 ตัวอักษร
    - ใช้ `random.choices()` สุ่มตัวอักษรจาก `string.ascii_uppercase`
    - คืนค่าข้อความที่สร้างขึ้น
    """
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def update_tmp_file(content):
    """
    เขียนข้อความที่ได้รับไปยังไฟล์ `news.tmp`
    - เปิดไฟล์ `news.tmp` ในโหมดเขียน (`w`)
    - ใช้ encoding `utf-8` เพื่อรองรับตัวอักษรพิเศษ
    - เขียนข้อมูลลงในไฟล์
    """
    with open("news.tmp", "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == "__main__":
    """
    จุดเริ่มต้นของโปรแกรม
    - เรียกใช้ `fetch_basketball_news()` เพื่อดึงข่าว
    - ถ้าดึงข่าวไม่ได้ (`news is None`) ให้ใช้ `generate_random_text()` แทน
    - อัปเดตไฟล์ `news.tmp` ด้วยข้อความที่ได้
    - แสดงข้อความว่า `news.tmp updated successfully` เพื่อยืนยันว่าไฟล์ถูกอัปเดต
    """
    
    news = fetch_basketball_news()
    
    if news is None:  # ถ้า API ใช้งานไม่ได้ ให้ใช้ข้อความสุ่มแทน
        news = generate_random_text()

    update_tmp_file(news)  # บันทึกข่าวหรือข้อความสุ่มลงไฟล์ `news.tmp`
    print("news.tmp updated successfully")  # แจ้งเตือนว่าการอัปเดตเสร็จสิ้น
