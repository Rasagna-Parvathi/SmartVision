# SmartVision – AI Security System

SmartVision is an AI-based security system that uses **face recognition** to identify authorized users and detect intruders in real time.
The system monitors camera input, verifies faces using a trained dataset, and alerts the administrator if an unknown person is detected.

---

## Project Overview

SmartVision improves security by automating identity verification.
When a person appears in front of the camera, the system compares the detected face with stored images in the dataset.

* If the face matches → **Access Granted**
* If the face is unknown → **Intruder Alert**

The system can trigger an **alarm sound**, **save intruder images**, **send email notifications**, and **store access logs**.
A **web dashboard** is also provided to monitor all activities.

---

## Features

* Face Recognition using machine learning
* Real-time camera monitoring
* Authorized user identification
* Intruder detection
* Alarm notification system
* Email alert with captured intruder image
* Access logs with date and time
* Web dashboard to view system activity
* Intruder image gallery

---

## Technologies Used

* Python
* Flask
* OpenCV
* Face Recognition Library
* HTML
* CSS
* JavaScript

---

## Project Structure

```
SmartVision
│
├── backend
│   ├── app.py
│   ├── dataset
│   ├── models
│   ├── static
│   │   ├── intruders
│   │   ├── style.css
│   │   └── alarm.wav
│   ├── templates
│   │   ├── index.html
│   │   └── dashboard.html
│   └── access_log.csv
│
└── requirements.txt
```

---

## How the System Works

1. The camera captures video frames.
2. The system detects faces using OpenCV.
3. Detected faces are encoded using the Face Recognition library.
4. The encoding is compared with stored dataset images.
5. If a match is found → Access Granted.
6. If no match is found → Intruder detected.
7. The system triggers an alarm, saves the image, and logs the event.

---

## Installation

Clone the repository:

```
git clone https://github.com/Rasagna-Parvathi/SmartVision.git
```

Move to the project folder:

```
cd SmartVision/backend
```

Install required libraries:

```
pip install -r requirements.txt
```

Run the application:

```
python app.py
```

---

## Dashboard

The SmartVision dashboard provides a clear view of system activity:

* Total authorized accesses
* Total intruder alerts
* Access logs
* Intruder images captured by the system

---

## Future Improvements

* Live camera streaming in dashboard
* Mobile notification alerts
* Multi-user recognition
* Cloud database integration
* Real-time monitoring from remote devices

---

## Author

**Rasagna Parvathi**
BTech Computer Science and Engineering

---

## License

This project is created for educational and research purposes.
