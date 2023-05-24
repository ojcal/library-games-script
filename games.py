import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os.path

# SMTP server settings
smtp_server = "mail.mail.org"
smtp_port = 587

# Email credentials
smtp_username = "**********"
smtp_password = "**********"

# create a message object
msg = MIMEMultipart()
msg['Subject'] = 'Uusia pelejä kirjastossa!'
msg['From'] = 'Python automaatio *********'
msg['To'] = '***********'

# URL of the webpage to track
url = "http://bit.ly/*******"

# Check if the file exists, if not, create it
if not os.path.isfile('kirjaston_pelit.txt'):
    with open('kirjaston_pelit.txt', 'w') as f:
        f.write("")

try:
    # Make a request to the webpage
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the first 10 search titles and links
    search_titles = soup.select('h2.search-title')[:10]
    search_links = soup.select('a.title')[:10]

    # Combine the titles and links into a list of strings
    search_results = [f"{i+1}. {title.get_text().replace('Näytä tarkat tiedot','').replace('PlayStation 5.', 'PS5').replace('PlayStation 4.', 'PS4').replace(' :', ':').strip()}: https://*********.fi{link.get('href')[:link.get('href').find('?sid=')]}\n" for i,
                      (title, link) in enumerate(zip(search_titles, search_links))]

    # Join the search results into a single string
    search_results_text = "\n".join(search_results)

    # Read the previous email body from the file
    with open('kirjaston_pelit.txt', 'r') as f:
        previous_body = f.read()

    # Check if the new email body is different from the previous one
    if search_results_text.strip() != previous_body.strip():

        # attach the message body
        body = f"Kirjastoon on tullut uusia pelejä: \n\n{search_results_text}"
        msg.attach(MIMEText(body, 'plain'))

        # connect to the SMTP server and start TLS
        smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
        smtp_conn.starttls()

        # authenticate with the SMTP server
        smtp_conn.login(smtp_username, smtp_password)

        # send the message
        smtp_conn.sendmail(msg['From'], msg['To'], msg.as_string())

        # Write the new email body to the file
        with open('kirjaston_pelit.txt', 'w') as f:
            f.write(search_results_text)

        # close the connection
        smtp_conn.quit()

except requests.exceptions.RequestException as e:
    # Create or append to the error.txt file
    with open('error.txt', 'a') as f:
        # Write the error message to the file
        f.write(str(e) + '\n')
