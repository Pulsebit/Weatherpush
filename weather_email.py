import os
import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

WEATHER_API_URL = "http://t.weather.sojson.com/api/weather/city/{}"
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
FROM_EMAIL = os.getenv('FROM_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')
SUBJECT_DEFAULT = "Today's weather forecast"

def get_weather(city):
    """
    Fetches weather information for a given city code.
    
    :param city: City code as string
    :return: Weather information as string or error message
    """
    response = requests.get(WEATHER_API_URL.format(city))
    data = response.json()
    
    if data['status'] == 200:
        forecast = data['data']['forecast'][0]
        return (
            f"{data['cityInfo']['city']} {forecast['ymd']} {forecast['week']}\n"
            f"Weather: {forecast['type']}\n"
            f"Temperature: {forecast['high']} {forecast['low']}"
        )
    else:
        return "Weather query failed with status: {}".format(data.get('msg', 'Unknown error'))

def send_email(subject, body):
    """
    Sends an email with the provided subject and body.
    
    :param subject: Email subject
    :param body: Email body content
    """
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

def job():
    """
   Timed task: Obtain weather information and send emails
    """
    city_code = os.getenv('CITY_CODE', '101010100')
    weather_info = get_weather(city_code)
    send_email(SUBJECT_DEFAULT, weather_info)

if __name__ == "__main__":
    schedule.every().day.at("08:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)