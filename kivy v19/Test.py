import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("cosmiccode2025@gmail.com", "Password@2025")
# message to be sent
message = "Message_you_need_to_send"
# sending the mail
s.sendmail("cosmiccode2025@gmail.com", "cosmiccode2025@gmail.com", message)
# terminating the session
s.quit()