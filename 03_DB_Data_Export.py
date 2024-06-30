import mysql.connector  # using mysql connector 
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os 
import numpy as np
import pandas as pd

myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiva@123",
    database="demo"
)
myCursor = myDB.cursor()


print("All employee data:")
myCursor.execute("select * from employees")
rows = myCursor.fetchall()


column_names = [i[0] for i in myCursor.description]


print(tabulate(rows, headers=column_names, tablefmt="pretty"))

if myDB.is_connected():
    db_info = myDB.get_server_info()
    print("Connected to MySQL Server version ", db_info)

    myCursor.execute("SELECT DATABASE();")
    record = myCursor.fetchone()
    print("You're connected to database: ", record)

    myCursor.close()
    myDB.close()
else:
    print("You're not connected to MySQL Server")


data_list = [list(row) for row in rows]

numpy_array = np.array(data_list)

df = pd.DataFrame(numpy_array, columns=column_names)

df.to_excel("emp_data.xlsx", index = False)


FROM = 'laxminarayanapattanayak@gmail.com'
TO = "laxminarayana3101@gmail.com"
SUBJECT = "Demo python mail with attachments"
TEXT = "This message was sent by Laxmi Narayana for test purpose with multiple attachments."


message = MIMEMultipart()
message['From'] = FROM
message['To'] = TO
message['Subject'] = SUBJECT


message.attach(MIMEText(TEXT, 'plain'))

file_path = os.path.abspath('emp_data.xlsx')    
filename = os.path.basename(file_path)
print(filename)


def attach_file(message, filename):
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        message.attach(part)


attach_file(message, filename)


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

USERNAME = 'laxminarayanapattanayak@gmail.com'
PASSWORD = '_____' # A 16 alphabetic character based password generated by google account

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(FROM, TO, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()