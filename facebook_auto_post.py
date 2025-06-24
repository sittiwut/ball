import requests
import schedule
import time
import facebook
import os
import logging
from datetime import datetime

# ตั้งค่า Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# การตั้งค่า API จาก Environment Variables
JUSTWATCH_API_URL = "https://api.justwatch.com/content/titles/en_US/popular"
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
MORNING_POST_TIME = os.getenv("MORNING_POST_TIME", "02:00")  # 09:00 TH = 02:00 UTC
EVENING_POST_TIME = os.getenv("EVENING_POST_TIME", "11:00")  # 18:00 TH = 11:00 UTC

# ฟังก์ชันส่งแจ้งเตือนผ่าน LINE Notify
def send_line_notify(message):
    if not LINE_NOTIFY_TOKEN:
        logger.warning("LINE_NOTIFY_TOKEN ไม่ได้ตั้งค่า ข้ามการแจ้งเตือน")
        return
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
        data = {"message": message}
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        logger.info("ส่งการแจ้งเตือน LINE สำเร็จ")
    except requests.RequestException as e:
        logger.error(f"เกิดข้อผิดพลาดในการส่ง LINE Notify: {str(e)}")

# ฟังก์ชันดึงข้อมูลจาก JustWatch
def fetch_justwatch_popular():
    try:
        response = requests.post(JUSTWATCH_API_URL, json={
            "page_size": 5,
            "page": 1,
            "query": "",
            "content_types": ["movie", "show"]
        }, timeout=10)
        response.raise_for_status()
        data = response.json()
        titles = data.get("items", [])
        if not titles:
            error_msg = "ไม่มีข้อมูลจาก JustWatch"
            logger.warning(error_msg)
            send_line_notify(error_msg)
            return error_msg
        
        post_message = "🎬 ภาพยนตร์และซีรีส์ยอดนิยมจาก JustWatch วันนี้!\n\n"
        for item in titles[:3]:
            title = item.get("title", "N/A")
            content_type = item.get("object_type", "N/A").capitalize()
            post_message += f"- {title} ({content_type})\n"
        logger.info("ดึงข้อมูลจาก JustWatch สำเร็จ")
        return post_message
    except requests.RequestException as e:
        error_msg = f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก JustWatch: {str(e)}"
        logger.error(error_msg)
        send_line_notify(error_msg)
        return error_msg

# ฟังก์ชันโพสต์ลง Facebook
def post_to_facebook(message):
    if not all([FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN]):
        error_msg = "FACEBOOK_PAGE_ID หรือ FACEBOOK_ACCESS_TOKEN ไม่ได้ตั้งค่า"
        logger.error(error_msg)
        send_line_notify(error_msg)
        return
    try:
        graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
        graph.put_object(
            parent_object=FACEBOOK_PAGE_ID,
            connection_name="feed",
            message=message
        )
        logger.info(f"โพสต์สำเร็จเมื่อ {datetime.now()}")
        send_line_notify(f"โพสต์สำเร็จ: {message[:50]}...")
    except facebook.GraphAPIError as e:
        error_msg = f"เกิดข้อผิดพลาดในการโพสต์ลง Facebook: {str(e)}"
        logger.error(error_msg)
        send_line_notify(error_msg)

# ฟังก์ชันหลักสำหรับการโพสต์
def job():
    logger.info("เริ่มงานโพสต์อัตโนมัติ")
    message = fetch_justwatch_popular()
    if not message.startswith("เกิดข้อผิดพลาด"):
        post_to_facebook(message)
    else:
        logger.warning("ข้ามการโพสต์เนื่องจากไม่มีข้อมูลที่ถูกต้อง")

# ตั้งเวลาการโพสต์
schedule.every().day.at(MORNING_POST_TIME).do(job)
schedule.every().day.at(EVENING_POST_TIME).do(job)

# รันลูปเพื่อตรวจสอบงานตามตาราง
if __name__ == "__main__":
    logger.info("เริ่มต้นระบบโพสต์อัตโนมัติ...")
    send_line_notify("เริ่มต้นระบบโพสต์อัตโนมัติ")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดใน main loop: {str(e)}")
            send_line_notify(f"เกิดข้อผิดพลาดในระบบ: {str(e)}")
            time.sleep(60)