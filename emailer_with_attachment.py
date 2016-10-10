import smtplib
import mimetypes
import getpass
from os import listdir
from os.path import isfile,join,getsize
from email import encoders
from email.mime.text import MIMEText
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio


def getAttachmentsSize():
    total = 0

    for i in listdir('attachments'):
        if isfile(join("attachments",i)):
            total += getsize(join("attachments",i))

    return total / (10**6)

def getPayload(path):
    path = join("attachments" , path)
    ctype , encoding = mimetypes.guess_type(path)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype , subtype = ctype.split("/" , 1)

    if maintype == 'text':
        fp = open(path)
        msg = MIMEText(fp.read() , _subtype=subtype)
        fp.close()

    elif maintype == 'image':
        fp = open(path , 'rb')
        msg = MIMEImage(fp.read())
        fp.close()

    elif maintype == 'audio':
        fp = open(path , 'rb')
        msg = MIMEAudio(fp.read())
        fp.close()

    else:
        fp = open(path , 'rb')
        msg = MIMEBase(maintype , subtype)
        msg.set_payload(fp.read())
        fp.close()

        encoders.encode_base64(msg)
    

    msg.add_header('Content-Disposition' , 'attachment' , filename=path)

    return msg

def sendMail(username , password , to , composed_mail):
    s = smtplib.SMTP('smtp.gmail.com' , 587)
    s.ehlo()
    s.starttls()

    s.login(username , password)
    s.sendmail(username , to , composed_mail)
    s.quit()


def main():
    subject = raw_input('Enter subject of email:')
    body = raw_input("Enter body of message:")
    to = raw_input('Enter email of recipient:')
    sender = raw_input('Enter sender email:')

    
    container = MIMEMultipart()
    container['Subject'] = subject
    container['To'] = to
    container['From'] = sender
    
    size = getAttachmentsSize()

    if size > 20:
        print "Attachment folder too big.Remove some content"

    files = [f for f in listdir("attachments") if isfile(join("attachments", f))]

    for path in files:
        msg = getPayload(path)
        msg.add_header('Content-Disposition' , 'attachment' , filename=path)
        container.attach(msg)
        
    container.attach(MIMEText(body))

    composed_mail = container.as_string()

    username = raw_input('Enter your gmail address:')
    password = getpass.getpass('Enter the passwrd for your account:')

    try:
        sendMail(username , password , container['To'] , composed_mail)
    except:
        print "An error occurred"

main()
