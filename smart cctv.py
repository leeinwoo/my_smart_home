import cv2
import time
import smtplib
import motion
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import telegram

smtp_server = "smtp.gmail.com"
port = 587
portssl = 465
userid = "id"
passwd = "pw"
token = '239499283:AAHYbHg410S0ccm_-w7nmLT2Tz1zp_RaBps'

def sendMail(image):
    to=[userid]
    imageByte=cv2.imencode(".jpeg",image)[1].tostring()
    msg=MIMEMultipart()
    imageMime=MIMEImage(imageByte)
    msg.attach(imageMime)
    msg['From']='Me'
    msg['To']=to[0]
    msg['Subject']="Invader is Coming!!"

    server=smtplib.SMTP(smtp_server, port)
    server.ehlo_or_helo_if_needed()
    ret,m=server.starttls()
    server.ehlo_or_helo_if_needed()
    ret,m=server.login(userid, passwd)
    if (ret!=235):
        print("login fail")
        return
    server.sendmail('me',to,msg.as_string())
    server.quit()

def sendTelegram(image):
    bot = telegram.Bot(token=token)
    last_update_id = None
    try:
        last_update_id = bot.getUpdates()[-1].update_id
    except IndexError:
        last_update_id = None
    for update in bot.getUpdates(offset=last_update_id, timeout=10):
        chat_id = update.message.chat_id
        path = image.encode('utf-8')
        img = open(path, 'r')
        bot.sendPhoto(chat_id=chat_id, photo=img)
        bot.sendMessage(chat_id=chat_id, text='Invader is Coming!!')
    
if __name__ == '__main__':
    print("start")
    thresh=16
    cam=cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    if(cam.isOpened()==False):
        print("cam isnt opened")
        exit()
    i=[None,None,None]
    flag=False
    for n in range(3):
        i[n]=motion.getGrayCamImg(cam)
    checkFlag=0
    while True:
        diff=motion.diffImage(i)
        thrimg=cv2.threshold(diff,thresh,1,cv2.THRESH_BINARY)[1]
        count=cv2.countNonZero(thrimg)
        print("count:",count)
        #if invader is checked.
        if count>500:
            checkFlag+=1
        if checkFlag>=10 and flag==False:
            img = 'detect.jpg'
            cv2.imwrite(img,i[2])
            sendMail(i[2])
            sendTelegram(img)
            flag=True
            print("invader is coming!!!")
            break
        elif count==0 and flag==True:
            flag=False
            checkFlag=0
        print("checkFlag:",checkFlag)
        # process next image
        motion.updateCameraImage(cam, i)
        key = cv2.waitKey(10)
        if key == 27:
            break
