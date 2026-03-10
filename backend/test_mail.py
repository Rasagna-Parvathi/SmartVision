import smtplib

EMAIL_ADDRESS = "parvathirasagnarasagnabittu@gmail.com"
EMAIL_PASSWORD = "hertnewcsjkcchnf"  # no spaces

try:
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print("Login successful")
    smtp.quit()
except Exception as e:
    print("ERROR:", e)