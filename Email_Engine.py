import base64
from IPython.display import display, HTML
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import imaplib
import os
import threading
import base64
from IPython.display import display, HTML
import getpass
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)


# coding=utf-8
# Author: Nima Farnoodian   nima.farnoodian@student.uclouvain.be

# tested on python 3.6.4
def ImageExist(email):
    cnx = connection.MySQLConnection(user=user_name, password=Password,
                                 host=host,
                                 database=database)
    cursor=cnx.cursor()
    query="SELECT emailCard FROM user WHERE email ="
    cursor.execute(query+"'"+email+"'")
    user=[]

    for i in cursor:
        user.append(i)
    print(user)
    if len(user)>0:
        approval=user[0][0]
        exist=True
    else:
        exist=False
        
    if type(approval)==type(None) or approval=='':
        con=True
    else:
        con=False
        
    cursor.close()
    return (exist,con)

def find_user_ID(email):
    cnx = connection.MySQLConnection(user=user_name, password=Password,
                                 host=host,
                                 database=database)
    cursor=cnx.cursor()
    query="SELECT auth_id FROM user WHERE email ="
    cursor.execute(query+"'"+email+"'")
    user=[]

    for i in cursor:
        user.append(i)
    if len(user)>0:
        
        auth_id=user[0][0]
    cursor.close()
    
    return auth_id

def update_HTML_Address(HTMLaddress,email):
    HTMLaddress=HTMLaddress.strip()
    cnx = connection.MySQLConnection(user=user_name, password=Password,
                                     host=host,
                                     database=database)
    updateQuery = "UPDATE user SET emailCard = '"+ HTMLaddress+"' WHERE email = '"+email +"'"
    cursor=cnx.cursor()
    cursor.execute(updateQuery)
    cnx.commit()
    cnx.rollback()
    cursor.close()

def find_user(email):
    cnx = connection.MySQLConnection(user=user_name, password=Password,
                                 host=host,
                                 database=database)
    cursor=cnx.cursor()
    query="SELECT firstName, lastName,approbation FROM user WHERE email ="
    cursor.execute(query+"'"+email+"'")
    user=[]

    for i in cursor:
        user.append(i)
    if len(user)>0:
        
        fname=user[0][0]
        lname=user[0][1]
        approval=user[0][2]
        exist=True
    else:
        fname=''
        lname=''
        approval=''
        exist=False
    cursor.close()
    return (fname,lname,approval,exist)

def update_status(email):
    email=email.strip()
    cnx = connection.MySQLConnection(user=user_name, password=Password,
                                     host=host,
                                     database=database)
    updateQuery = "UPDATE user SET approbation = 'WaitingForValidation' WHERE email = '"+email +"'"

    cursor=cnx.cursor()
    cursor.execute(updateQuery)
    cnx.commit()
    cnx.rollback()
    cursor.close()

def read_images_from_pdf(pdf):
# Extract jpg's from pdf's. Quick and dirty.

    startmark = b"\xff\xd8"
    startfix = 0
    endmark = b"\xff\xd9"
    endfix = 2
    i = 0
    imagelist=[]
    njpg = 0
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream + 20)
        if istart < 0:
            i = istream + 20
            continue
        iend = pdf.find(b"endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend - 20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        print("JPG %d from %d to %d" % (njpg, istart, iend))
        jpg = pdf[istart:iend]
        '''
        with open(receiver+'/'+filename+"-jpg%d.jpg" % njpg, "wb") as jpgfile:
            jpgfile.write(jpg)
        '''
        jpg=base64.b64encode(jpg).decode('utf-8')
        imagelist.append(jpg)
    
        njpg += 1
        i = iend
        
    return imagelist

def send_email_simple(receiver,subject,bodyscript):
    # Author: Nima Farnoodian
    body = 'Subject: '+subject+ ' .\n\nDear ' + name_extract(receiver)+', \n\n' + bodyscript + '\nSincerely,\nApp4you Administrator'
    try:
        try:
            smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        except Exception as e:
            print(e)
            smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
        print('An automatice reply sent to ' + receiver)
    except:
        print('An error appears while sending an automatic reply to ' + receiver)
    #type(smtpObj) 
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('youremail@outlook.com', "your password") 
    smtpObj.sendmail('youremail@outlook.com', receiver, body) # Or recipient@outlook

    smtpObj.quit()
    pass

    


def send_email_html(receiver,subject,bodyscript='',html=''):
  

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'youremail@outlook.com'
    msg['To'] = receiver

    # Create the body of the message (a plain-text and an HTML version).
    #text = "test"

    # Record the MIME types of both parts - text/plain and text/html.
    if html=='':
        html=bodyscript
    else:
        html='<p><strong>'+bodyscript+'</strong></p>'+html
    part1 = MIMEText(bodyscript, 'plain')
    part2 = MIMEText(html, 'html')
    

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    try:
        try:
            smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        except Exception as e:
            print(e)
            smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
        print('An automatice reply sent to ' + receiver)
    except:
        print('An error appears while sending an automatic reply to ' + receiver)
    #type(smtpObj) 
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('youremail@outlook.com', "your password") 
    smtpObj.sendmail('youremail@outlook.com', receiver, msg.as_string()) # Or recipient@outlook

    smtpObj.quit()
    pass

def name_extract(full_email):
    return full_email.split('<')[0].strip()


def html_embedding(images,sender_mail,sender_name,sender_id,send_date,image_number,sender_message):
    head=(''  '<html>'
            '<img src="https://docparser.com/blog/wp-content/uploads/2016/08/Email-Attachment-Parsing-e1479117260293.png" alt="Logo" border="0" class="img__block" style="display: block; max-width: 100%; margin: 0 auto;" />'
              '<head> <title>{sender_name}</title> </head>'
              '<body>'
              '<hr>'
                '<center><strong>App4You</strong></center>'
                '<center><strong>The following images sent by {sender_name}.</strong></center>'
                '<p>App4You ID: {ID}</p>'
                '<p>User email: {sender}</p>'
                '<p>Date and Time: {date}</p>'
                '<p>The number of images: {imgno}'
                '<p>The sender message: {message}'
                 '<p></p>'

          '')
    template = (''
        '<img src=data:image/jpeg;base64,{blob}>' # Use the ".png" magic url so that the latest, most-up-to-date image is included
        '{caption}'                              # Optional caption to include below the graph
        '<hr>'  
                # horizontal line
    '')

    end=(''
         '</body>'
         '</html>'
    '')
    email_body = ''
    for image in images:
        _ = template
        _ = _.format(blob=image,sender=sender_mail, caption='')
        email_body += _
    head=head.format(sender_name=sender_name,sender=sender_mail,ID=sender_id,date=send_date,imgno=image_number,message=sender_message)
    display(HTML(head+email_body+end))
    with open(sender_id+".html", "w") as file:
        file.write(head+email_body+end)
    return head+email_body+end

def email_reader(time):
    mail_conbtents=[]
    EMAIL = 'youremail@outlook.com'
    PASSWORD = "yourpassword"
    SERVER = 'outlook.office365.com'
    e = threading.Event()
    while not e.wait(time):

        #with imaplib.IMAP4(SERVER) as mail:
            #mail.noop()
        mail=imaplib.IMAP4_SSL(SERVER)
        # connect to the server and go to its inbox
        mail.login(EMAIL, PASSWORD)
        # we choose the inbox but you can select others
                #mail.select('inbox')
        mail.select('inbox')
        # we'll search using the ALL criteria to retrieve
        # every message inside the inbox
        # it will return with its status and a list of ids
        status, data = mail.search(None, 'UnSeen')
        # the list returned is a list of bytes separated
        # by white spaces on this format: [b'1 2 3', b'4 5 6']
        # so, to separate it first we create an empty list
        mail_ids = []
        # then we go through the list splitting its blocks
        # of bytes and appending to the mail_ids list
        for block in data:
            # the split function called without parameter
            # transforms the text or bytes into a list using
            # as separator the white spaces:
            # b'1 2 3'.split() => [b'1', b'2', b'3']
            mail_ids += block.split()

        # now for every id we'll fetch the email
        # to extract its content
        #emailExtracted={}
        counter=0
        for i in mail_ids:
            opStat=False
            try:
                img=[]
                emailmsg=''
                # the fetch function fetch the email given its id
                # and format that you want the message to be

                status, data = mail.fetch(i, '(BODY.PEEK[])')
                #status, data = mail.fetch(i, '(RFC822)')
                if counter==10:
                    break
                counter+=1
                # the content data at the '(RFC822)' format comes on
                # a list with a tuple with header, content, and the closing
                # byte b')'
                for response_part in data:
                    # so if its a tuple...
                    if isinstance(response_part, tuple):
                        # we go for the content at its second element
                        # skipping the header at the first and the closing
                        # at the third
                        message = email.message_from_bytes(response_part[1])

                        # with the content we can extract the info about
                        # who sent the message and its subject

                        mail_from = message['from']
                        mail_subject = message['subject']
                        mail_date=message['date']
                        '''
                        print('-------------------')
                        print(message)
                        print('-------------------')
                        
                        '''
                        clean_mail=mail_from.split('<')[1].split('>')[0]
                        QueryRes=find_user(clean_mail)
                        fname=QueryRes[0]
                        lname=QueryRes[1]
                        exist=QueryRes[3]
                        UserStat=QueryRes[2]

                        res_get=ImageExist(clean_mail)
                        exist=res_get[0]
                        continues=res_get[1]
                        # then for the text we have a little more work to do
                        # because it can be in plain text or multipart
                        # if its not plain text we need to separate the message
                        # from its annexes to get the text
                        if exist==False:
                            mail.store(i, '+FLAGS', '\SEEN')
                        if continues==False: 
                            if UserStat=='WaitingForValidation':
                                subject= 'Your validation is being examined.' 
                                bodyscript='Your validation is being examined. You do not need to re-send your ID-Card. Once we finish our examination, we will let you know the result via an email.'
                                send_email_simple(mail_from,subject,bodyscript)
                                mail.store(i, '+FLAGS', '\SEEN')
                        if continues==True and exist==True:
                            if message.is_multipart():
                                
                                mail_content = ''
                                #print('this is a content type: ' )
                                #print(message.get_content_type())
                                # on multipart we have the text message and
                                # another things like annex, and html version
                                # of the message, in that case we loop through
                                # the email payload
                                for part in message.get_payload():
                                    # if the content type is text/plain
                                    # we extract it
                                    #print('Each Content')
                                    #print(part.get_content_type())
                                    if part.get_content_type() in  ['image/jpeg','image/png','application/pdf']: 
                                        mail_content += part.get_payload()
                                        content_disposition = str(part.get("Content-Disposition"))
                                        #print('Pay load')
                                        #print(part.get_payload())

                                        # the following code is used to save the attachments 
                                        if "attachment" in content_disposition:
                                            # download attachment
                                            #filename = part.get_filename()
                                            if part.get_content_type() in  ['image/jpeg','image/png']:
                                                picfetched=base64.b64encode(part.get_payload(decode=True)).decode('utf-8')
                                                img.append(picfetched)
                                            if part.get_content_type()=='application/pdf':
                                                img+=read_images_from_pdf(part.get_payload(decode=True))
                                    if part.get_content_type() == 'text/plain':
                                        emailmsg= part.get_payload()
                                        print(emailmsg)        
                            else:
                                # if the message isn't multipart, just extract it
                                mail_content = message.get_payload()
                            mail_conbtents.append([mail_subject,mail_content])
                            # and then let's show its result

                            #emailExtracted[mail_from]
                            print(f'From: {mail_from}')
                            print(f'Date: {mail_date}')
                            print(f'Subject: {mail_subject}')
                            print('Message')
                            print(emailmsg)
                            #print(img)
                            imgnum=len(img)
                            
                            opStat=True 
            except:
                print('An unknown error appeared. The message is still marked Unread/Unseen.')
                
            if opStat==True:
                subject= 'Your email has been successfully recieved' 
                #bodyscript='<p> Dear '+name_extract(mail_from)+',</p>'+'<p>We declare that we have received your email that includes ' + str(imgnum)+ ' image(s). After checking, we will notify you of either your validation or rejection via an email.</p><p>Sincerely,<p>App4you administration.</p></p>'
                bodyscript='<p> Dear '+fname+' ' +lname+',</p>'+'<p>We declare that we have received your email that includes ' + str(imgnum)+ ' image(s). After checking, we will notify you of either your validation or rejection via an email.</p><p>Sincerely,<p>App4you administration.</p></p>'
                
                try:
                    if imgnum>0:
                        uid=find_user_ID(mail_from.split('<')[1].split('>')[0])
                        html=html_embedding(img,mail_from.split('<')[1].split('>')[0],mail_from.strip(),uid,mail_date,str(imgnum), emailmsg)
                        #send_email_html(mail_from,subject,bodyscript=bodyscript,html=html)
                        send_email_html(mail_from,subject,bodyscript=bodyscript,html='')
                        #update_status(mail_from.split('<')[1].split('>')[0])
                        address=os.getcwd()
                        address=address.replace('\\','/')
                        address+='/'
                        HTMLaddress=address+uid+'.html'
                        update_HTML_Address(HTMLaddress,mail_from.split('<')[1].split('>')[0])
                    else:
                        subject= 'Your email has been recieved, but without any ID Card/Image' 
                        bodyscript='We declare that we have received your email but it does not contain any ID Card. Notice that your email must include at least an image (in the formats of .jpg or .png) or a PDF file, which represent your identity.'
                        send_email_simple(mail_from,subject,bodyscript)
                        
                    mail.store(i, '+FLAGS', '\SEEN')  # Mark as read
                    #imap_server.store(message_number, '-FLAGS', '\SEEN') #Mark as unread
                except:
                    pass


#username=input('Enter Your email:')
#password = getpass.getpass('Please enter your password:')
#print(password)
'''
user_name=user of database connection
Password=pasword of database connection
host=if local, set'127.0.0.1', otherwise host IP
database= Your database name
'''
print('Database Connection:')
user_name=input('Enter Your user name:')
Password = getpass.getpass('Please enter your password:')
host=input('Enter Your host:')
database=input('Enter Your Database name:')
try:
    cnx = connection.MySQLConnection(user=user_name, password=Password,
                                 host=host,
                                 database=database)
    print('Database Connection is valid.')
    print('The engine is currently listening.')
    email_reader(10)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()


