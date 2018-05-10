# from django.core.mail import send_mail
#
# def _mail_for_request(id_, member, directorate_mails, subject="ITU Robotics Door Clearance Request"):
#     if member is Member or True:
#         msg = member.name + " is requesting for clearance to open the door. ITU-ID: " + member.id + "\n Request ID: " + id_
#         send_mail(subject, msg, 'senceryazici@gmail.com', directorate_mails, fail_silently=False)
#         return True
#     else:
#         return False

from database.json_database.database_struct import Member
import smtplib

logged = False
server = None

SYSTEM_MAIL = "senceryazici@gmail.com"
SYSTEM_PASSWORD = "kiymhplfbjxlowge"

def login():
    global server, logged
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        # NOTE: Application password needed to perform this. Google - gmail - app password
        server.login(SYSTEM_MAIL, SYSTEM_PASSWORD)
        logged = True
        return True
    except:
        logged = False
        return False

def mail_for_request(id_, member, directorate_mails, subject="ITU Robotics Door Clearance Request"):
    global logged, server
    if not logged:
        if not login():
            return False
    msg_str = member.name + " is requesting for clearance to open the door. <ITU-ID:" + member.id + ",Request ID:" + id_ + ">"
    msg = "\r\n".join([
    "From: " + SYSTEM_MAIL,
    "To: " + ",".join(directorate_mails),
    "Subject: " + subject + "<" + id_ + ">",
    "",
    msg_str
    ])
    server.sendmail("senceryazici@gmail.com", directorate_mails, msg)
    return True



import smtplib
import time
import imaplib
import email

def _find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def _info(msg):
    print "[ INFO ] " + msg

def read_email_from_gmail(directorate_mails, pending_request_id):
    ORG_EMAIL   = "@gmail.com"
    FROM_EMAIL  = SYSTEM_MAIL
    FROM_PWD    = SYSTEM_PASSWORD
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT   = 993
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        # type, data = mail.search(None, '(ALL)')
        mail_ids = data[0]

        id_list = mail_ids.split()
        if not len(id_list) > 0:
            _info("NO NEW MAIL FOUND")
            return None, None
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    _info("---- NEW MAIL ------")
                    _info("FROM: " + email_from + "SUBJECT: " + email_subject)

                    for direc in directorate_mails:
                        if not email_from.strip() == direc.strip():
                            continue
                    _info("MAIL FROM KNOWN ADDRESS")

                    # Decode
                    body = None
                    if msg.is_multipart():
                        # continue
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))

                            # skip any text/plain (txt) attachments
                            if ctype == 'text/plain' and 'attachment' not in cdispo:
                                body = part.get_payload(decode=True)  # decode
                                break
                    else:
                        body = msg.get_payload(decode=True)
                    # Decode

                    request_result = False
                    req_id = email_subject.upper().replace("RE: ", "")
                    req_status = body
                    if "<" in req_id and ">" in req_id:
                        req_id = _find_between(req_id, "<", ">")

                    if "\n" in req_status:
                        req_status = req_status.split("\n")[0]
                    _info(">> ID:" + req_id + " STATUS: " + req_status)

                    # if the request id is in the pending id list
                    if (req_id in pending_request_id):
                        if "OK" in req_status.upper():
                            request_result = True

                        return req_id, request_result
                        # NOTE: RETURN RESULT TO THE server
                    else:
                        _info("NO MATCH WITH THE PENDING REQUESTS")
                        continue
    except Exception, e:
        print str(e)
