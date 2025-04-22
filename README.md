# 💊 Smart BLE-Enabled Pill Box

A portable, BLE-powered smart pill box designed for professionals and travelers to ensure they never miss a dose—even on the go. Integrated with real-time vitals monitoring and Edge ML capabilities, this prototype acts as a personal health assistant with smart medication reminders.

## 🔧 Features

- **📱 BLE Sync with Flask App**  
  Sync alarm schedules and time seamlessly over Bluetooth Low Energy (BLE) using a custom Flask-based backend.

- **📊 Vital Signs Monitoring**  
  Integrated with the **MAX30102** sensor to track:
  - SpO2 (Oxygen Saturation)
  - Heart Rate
  - Skin Temperature

- **🧠 On-Device Edge ML**  
  Embedded ML models process vitals data locally on the **nRF52840** chip, eliminating the need for cloud processing.

- **⏰ Smart Alarm System**  
  - Vibration motor and buzzer to alert users
  - LED indicators for up to 5 pill compartments

- **📦 Compact & Travel-Friendly**  
  Fully enclosed in a lightweight 3D-printed PLA case for portability and daily use.

- **👩‍⚕️ Doctor Monitoring**  
  Automatically generates and shares health reports with doctors at every scheduled alarm time.

## 🖥️ Tech Stack

- **Microcontroller:** Seeed Studio nRF52840
- **Sensor:** MAX30102
- **Communication:** BLE
- **Backend:** Flask (Python)
- **ML Framework:** Custom TinyML
- **Frontend:** Basic HTML for interaction
- **Case:** 3D-printed PLA


## 🚀 Getting Started

1. Clone this repo:  
   `git clone https://github.com/dhnz-2006/smart-pill-box`

2. Connect nRF52840 and flash BLE code

3. Run the Flask backend:  
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
