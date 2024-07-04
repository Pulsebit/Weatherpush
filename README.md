***Weather Email Notification***

- 🌤This Python script fetches the current weather forecast for a specified city and sends it via email using SMTP. It utilizes the requests, schedule, time, and smtplib libraries for HTTP requests, scheduling, time management, and email handling respectively.
- The script will fetch the current weather information for the specified city, format it into an email, and send it to the recipient's email address specified in the code.

***

- Install dependencies:
```sh
pip install -r requirements.txt
```
***Notes***
- Update script with your configuration details:
 - Replace your_email@example.com and your_email_password with your email credentials.
 - Modify SMTP server details in send_email() function (e.g., smtp.example.com and port 587 for 163 Mail).
 - Update city_code in the job() function to your desired city's code (e.g., 101010100 for Beijing).
 - Change recipient email in the send_email() function (recipient_email@example.com).


**Usage**
- Run the script using Python:
```sh
python weather_email.py
```
