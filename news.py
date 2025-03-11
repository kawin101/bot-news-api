import os
import requests

# โหลด API Key จาก GitHub Secrets
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ใช้ `top-headlines` เพื่อดึงข่าวฟรี
API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_basketball_news():
    """ดึงข้อมูลข่าวกีฬาบาสเกตบอลจาก NewsAPI"""
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}  # ✅ ส่ง API Key ใน Header
    params = {
        "category": "sports",
        "q": "basketball",
        "language": "en"
    }

    response = requests.get(API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")
        return None

def format_news_data(data):
    """เลือกข่าว 1 ข่าวและจำกัดข้อความที่ 20 ตัวอักษร"""
    if not data or "articles" not in data or not data["articles"]:
        return "No news available."

    article = data["articles"][0]  # ใช้ข่าวแรก
    title = article["title"][:20]  # จำกัดข้อความที่ 20 ตัวอักษร
    return title

def update_tmp_file(content):
    """อัปเดตไฟล์ .tmp ด้วยข้อมูลข่าว"""
    with open("news.tmp", "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == "__main__":
    data = fetch_basketball_news()
    if data:
        formatted_content = format_news_data(data)
        update_tmp_file(formatted_content)
        print("news.tmp updated successfully")
