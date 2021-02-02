import socket
import threading
import time
from gpiozero import MotionSensor
import picamera
import smtplib
import io
from PIL import Image
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders

#connection configuration
client_address = ('192.168.1.8', 10000) #IP of the Server
pir = MotionSensor(18) #Pin 18 on Raspberry Pi for the PIR Sensor
camera = picamera.PiCamera()

#motion sensor configuration
print('PIR Module Setup')
print('Press CTRL+C to EXIT')
time.sleep(2)
print('Ready')
k=0


def SendMail(footage):
    msg = MIMEMultipart()
    sender_email_address = 'Add the email of the sender'
    receiver_email_address = 'Add the email of the receiver'
    Subject = 'Subject: Motion Detected \n\n'
    content = 'Dear User, \n Motion Detected in your home. \n\n'
    footer = 'Stay calm and check the video bellow'
    passcode = 'Add the password of the sender email'
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(footage, 'rb').read())
    email.encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(footage))
    msg.attach(part)
    
    text = MIMEText(Subject + content + footer)
    msg.attach(text)
    
    mail = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) #Add the data of the email provider
    mail.ehlo()
    mail.login(sender_email_address, passcode)
    mail.sendmail(sender_email_address,
               receiver_email_address,
               msg.as_string())
    mail.quit()




def client():
    global k
    video = k
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       
        while True:
            pir.wait_for_motion()
            
            #when motion detected enable connection with the server
            threading.Timer(80, client).start()
            client_socket = socket.socket()
            client_socket.connect(client_address)
            connection = client_socket.makefile('wb')
            print('Connection Established')
            print('Motion Detected')
            
            camera.resolution = (640,480)
            camera.rotation = 180
            camera.framerate = 35
    
            camera.start_preview
            time.sleep(2)
           
            camera.start_recording(connection, format = 'h264')
            camera.start_recording('Intruder%02d.h264' % k, splitter_port = 2, resize=(320,240)) #splits the feed and simultaneously saves the video on Raspberry Pi
            camera.wait_recording(20)
            camera.wait_recording(splitter_port = 2)
            camera.stop_recording(splitter_port = 2)
            camera.stop_recording()
            
            #convert h264 to mp4
            os.system('MP4Box -add ' + 'Intruder%02d.h264' % k + ' ' + 'Intruder%02d.mp4' % k)
            os.system('rm ' +'Intruder%02d.h264' % k)
            footage = 'Intruder%02d.mp4' % k
            #send email
            SendMail(footage)
            
            connection.close()
            client_socket.close()
            time.sleep(2)
            k+=1
            print('Connection closed')
                
            while 1:
                pass


if __name__ == '__main__':
    while 1:
        client()
