import os
import requests

# โหลดค่า ENV จาก GitHub Secrets
USER_EMAIL = os.getenv("USER_EMAIL")
USER_USERNAME = os.getenv("USER_USERNAME")
USER_REPO = os.getenv("USER_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# News API Key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
API_URL = f"https://newsapi.org/v2/top-headlines?category=sports&q=basketball&language=en&apiKey={NEWS_API_KEY}"

def fetch_basketball_news():
    """ดึงข้อมูลข่าวกีฬาบาสเกตบอลจาก NewsAPI"""
    response = requests.get(API_URL)
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

def push_to_github():
    """Push ไฟล์ news.tmp ที่อัปเดตกลับไปที่ GitHub"""
    os.system(f"git config --global user.name '{USER_USERNAME}'")
    os.system(f"git config --global user.email '{USER_EMAIL}'")
    os.system("git add news.tmp")
    os.system("git commit -m 'Update Basketball News' || exit 0")
    os.system(f"git push https://x-access-token:{GITHUB_TOKEN}@github.com/{USER_REPO}.git || exit 0")

if __name__ == "__main__":
    data = fetch_basketball_news()
    if data:
        formatted_content = format_news_data(data)
        update_tmp_file(formatted_content)
        push_to_github()
        print("news.tmp updated successfully")
