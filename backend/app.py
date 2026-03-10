from flask import Flask, render_template, request
import os
import cv2
import face_recognition
import datetime
import numpy as np
import smtplib
from email.message import EmailMessage
import threading
import winsound
import csv

app = Flask(__name__)

# =========================
# EMAIL CONFIGURATION
# =========================

EMAIL_ADDRESS = "parvathirasagnarasagnabittu@gmail.com"
EMAIL_PASSWORD = "hertnewcsjkcchnf"
ADMIN_EMAIL = "parvathirasagnarasagnabittu@gmail.com"

# =========================
# PATH SETUP
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, "dataset", "rasagna")
upload_folder = os.path.join(BASE_DIR, "uploads")
intruder_folder = os.path.join(BASE_DIR, "static", "intruders")
alarm_sound = os.path.join(BASE_DIR, "static", "alarm.wav")
log_file = os.path.join(BASE_DIR, "access_log.csv")

os.makedirs(upload_folder, exist_ok=True)
os.makedirs(intruder_folder, exist_ok=True)

# =========================
# LOAD FACE DATASET
# =========================

known_face_encodings = []
known_face_names = []

print("Loading dataset...")

for image_name in os.listdir(dataset_path):

    image_path = os.path.join(dataset_path, image_name)

    image = face_recognition.load_image_file(image_path)

    encodings = face_recognition.face_encodings(image)

    if encodings:
        known_face_encodings.append(encodings[0])
        known_face_names.append("Rasagna")

print("Face dataset loaded successfully")

# =========================
# ALARM CONTROL
# =========================

alarm_running = False

def alarm_thread():
    while alarm_running:
        winsound.PlaySound(alarm_sound, winsound.SND_FILENAME)

def play_alarm():

    global alarm_running

    if not alarm_running:
        alarm_running = True
        threading.Thread(target=alarm_thread).start()

def stop_alarm():

    global alarm_running

    alarm_running = False
    winsound.PlaySound(None, winsound.SND_PURGE)

# =========================
# EMAIL ALERT
# =========================

def send_email_alert(image_path):

    try:

        msg = EmailMessage()
        msg["Subject"] = "Intruder Alert - SmartVision"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = ADMIN_EMAIL

        msg.set_content("Intruder detected by SmartVision system.")

        with open(image_path, "rb") as f:
            file_data = f.read()

        msg.add_attachment(
            file_data,
            maintype="image",
            subtype="jpeg",
            filename="intruder.jpg"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email sent")

    except Exception as e:
        print("EMAIL ERROR:", e)

# =========================
# FACE IDENTIFICATION
# =========================

def identify_face(frame):

    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)

    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)

    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    names=[]
    confidences=[]

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        name="Unknown"
        confidence=0

        if len(face_distances)>0:

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:

                name = known_face_names[best_match_index]

                confidence = round((1-face_distances[best_match_index])*100,2)

        names.append(name)
        confidences.append(confidence)

    face_locations=[(t*4,r*4,b*4,l*4) for (t,r,b,l) in face_locations]

    return face_locations,names,confidences

def generate_frames():

    cap = cv2.VideoCapture(0)

    while True:

        success, frame = cap.read()

        if not success:
            break

        else:

            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# =========================
# WEBSITE IMAGE DETECTION
# =========================

@app.route("/", methods=["GET","POST"])

def home():

    name=None
    confidence=None
    status=None

    if request.method=="POST":

        file=request.files["image"]

        if file:

            filepath=os.path.join(upload_folder,file.filename)

            file.save(filepath)

            image=face_recognition.load_image_file(filepath)

            encodings=face_recognition.face_encodings(image)

            if encodings:

                face_encoding=encodings[0]

                face_distances=face_recognition.face_distance(
                    known_face_encodings,
                    face_encoding
                )

                best_match_index=np.argmin(face_distances)

                if face_distances[best_match_index] < 0.65:

                    name=known_face_names[best_match_index]

                    confidence=round((1-face_distances[best_match_index])*100,2)

                    status="Access Granted"

                else:

                    name="Unknown"
                    confidence=0
                    status="Access Denied"

                with open(log_file,"a") as f:

                    now=datetime.datetime.now()

                    f.write(f"{name},{confidence},{status},{now}\n")

    return render_template("index.html",name=name,confidence=confidence,status=status)

# =========================
# VIDEO STREAM ROUTE
# =========================

@app.route('/video')
def video():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")

def dashboard():

    logs=[]

    authorized=0
    intruder=0

    if os.path.exists(log_file):

        with open(log_file,"r") as f:

            reader=csv.reader(f)

            for row in reader:

                logs.append(row)

                if "Granted" in row[2]:
                    authorized+=1
                elif "Intruder" in row[2]:
                    intruder+=1

    intruder_images=os.listdir(intruder_folder)

    return render_template(
        "dashboard.html",
        logs=logs,
        authorized=authorized,
        intruder=intruder,
        intruder_images=intruder_images
    )

# =========================
# CAMERA SECURITY SYSTEM
# =========================

def start_camera():

    cap=cv2.VideoCapture(0)

    cap.set(3,640)
    cap.set(4,480)

    intruder_captured=False

    while True:

        ret,frame=cap.read()

        if not ret:
            break

        face_locations,names,confidences=identify_face(frame)

        for (top,right,bottom,left),name,confidence in zip(face_locations,names,confidences):

            if name!="Unknown":

                color=(0,255,0)

                label=f"{name} ({confidence}%)"

                stop_alarm()

                intruder_captured=False

            else:

                color=(0,0,255)

                label="INTRUDER"

                play_alarm()

                if not intruder_captured:

                    timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                    image_path=os.path.join(
                        intruder_folder,
                        f"intruder_{timestamp}.jpg"
                    )

                    cv2.imwrite(image_path,frame)

                    with open(log_file,"a") as f:

                        now=datetime.datetime.now()

                        f.write(f"Unknown,0,Intruder,{now}\n")

                    send_email_alert(image_path)

                    intruder_captured=True

            cv2.rectangle(frame,(left,top),(right,bottom),color,2)

            cv2.putText(frame,label,(left,top-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

        cv2.imshow("SmartVision AI Security",frame)

        if cv2.waitKey(1)==ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# =========================
# MAIN
# =========================

if __name__=="__main__":

    print("1 - Run Website")
    print("2 - Run Security Camera")

    choice=input("Enter option: ")

    if choice=="1":

        app.run(debug=True,use_reloader=False)

    elif choice=="2":

        start_camera()