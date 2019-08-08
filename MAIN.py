#importing neccessary libraries
import requests
from bs4 import BeautifulSoup
import smtplib, ssl
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage  

#save sender and receiver email-id's in variable
sender_email = "YOUR_EMAIL_ID"
receiver_email = "RECEIVER_EMAIL_ID"

#sender's password here
password = input("Type your password and press enter:")

#making the request
url = requests.get('http://www.imd.gov.in/Welcome%20To%20IMD/Welcome.php')

#making a beautifulsoup object   
soup = BeautifulSoup(url.text, 'lxml')

def message_to_send(soup):
    #find <a> tags 
    article = soup.find('a', style='color:#000066;')
    title = article.text
    print(title)
    
    #find 'href' in <a> tag
    link = article['href']
    print(link)
    
    #go to the above scraped link and make request
    url_pdf = requests.get(link)
    soup_pdf = BeautifulSoup(url_pdf.text, 'lxml')

    def send_pdf(soup_pdf):
        #find the link of embedded pdf from embed tag 
        embedded_pdf = soup_pdf.find('embed', style='width:100%; height:601; border:none;')
        link_pdf = embedded_pdf['src']
        
        #strip '..' from link_pdf
        strip_link = link_pdf.strip('..')
        main_url = 'http://www.imd.gov.in'
        
        #adding to main_url
        whole_pdf = main_url + strip_link
        print(whole_pdf)
        
        #creating message 
        message = MIMEMultipart()
        message["Subject"] = "UPDATE: PRESS RELEASE FROM IMD"
        message["From"] = sender_email
        message["To"] = receiver_email

        #attach image
        fp = open('download.jpg', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)
        
        #send html in email body
        html ="""
                <html>
                <body>
                <center>
                <img src='cid:image1', alt="IMD" style="width:120px;height:150px;"><br><br>
                <font style="font-size:34px; color:#99FF0; font-weight:bold; font-family:courier; text-shadow: 2px 2px #FF6633;
                letter-spacing:2px;">INDIA METEOROLOGICAL DEPARTMENT</font><br>
                <font style="font-size:21px; color:#003399; font-weight:bold; font-family:'courier';">Ministry of Earth Sciences
                </font><br>
                <font style="font-size:18px; color:#330000; font-weight:bold; font-family:'courier'; ">Government of India
                </font>
                </center>
                </body>
                </html>
                """
        total = title + '\n' + link + '\n' + whole_pdf  
        
        #attach ADD 
        ADD=MIMEText(_text=f"\n\nHey reader, you got a new post.\n\n{total}")
        message.attach(ADD) 
        
        #attach part 
        part= MIMEText(html,"html")
        message.attach(part)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())            
            

    send_pdf(soup_pdf)                    

message_to_send(soup)

