import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get weather information
def get_weather(city):
    url = f'http://t.weather.sojson.com/api/weather/city/{city}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 200:
        city_name = data['cityInfo']['city']
        date = data['data']['forecast'][0]['ymd']
        week = data['data']['forecast'][0]['week']
        weather = data['data']['forecast'][0]['type']
        temperature = data['data']['forecast'][0]['high'] + ' ' + data['data']['forecast'][0]['low']
        
        return f"{city_name} {date} {week}\nweather：{weather}\ntemperature：{temperature}"
    else:
        return "The weather query failed"

# Send  email
def send_email(subject, body, to_email):
    from_email = 'your_email@example.com'  # Modify the recipient's email address
    password = 'your_email_password'       # Modify the recipient's email password

    # Set the content of the message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send emails
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Modify the SMTP server address and port
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("The message was sent successfully")
    except Exception as e:
        print(f"The message failed to send: {str(e)}")

# Timing task
def job():
    city_code = '101010100'  # Modify the city code
    weather_info = get_weather(city_code)
    subject = "Today's weather forecast"
    send_email(subject, weather_info, 'recipient_email@example.com')  # Modify the recipient's email address

