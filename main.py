import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 获取天气信息
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
        
        return f"{city_name} {date} {week}\n天气：{weather}\n温度：{temperature}"
    else:
        return "天气查询失败"

# 发送邮件
def send_email(subject, body, to_email):
    from_email = 'your_email@example.com'  # 发件人邮箱
    password = 'your_email_password'       # 发件人邮箱密码

    # 设置邮件内容
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 连接SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # SMTP服务器地址和端口，这里以163邮箱为例
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")

# 定时任务
def job():
    city_code = '101010100'  # 北京的城市代码
    weather_info = get_weather(city_code)
    subject = "今日天气预报"
    send_email(subject, weather_info, 'recipient_email@example.com')  # 收件人邮箱

