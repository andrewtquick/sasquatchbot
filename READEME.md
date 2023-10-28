# Sasquatch Bot

Discord bot for twitch.tv/schadsquatch

---

# Installation

1. Install [python 3.11.5](https://www.python.org/downloads/release/python-3115/) or newer
2. Create a virtual environment
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment
   ```
   Windows:
   .venv/Scripts/Activate.ps1
   ```
   ```
   Mac/Linux
   .venv/Scripts/activate
   ```
4. Create a `.env` file with the following variables
   ```
   CLIENT_ID=
   TOKEN=
   FIREBASE_DATABASE_URL=
   FIREBASE_TYPE=
   FIREBASE_PROJECT_ID=
   FIREBASE_PRIVATE_KEY_ID=
   FIREBASE_PRIVATE_KEY=
   FIREBASE_CLIENT_EMAIL=
   FIREBASE_CLIENT_ID=
   FIREBASE_AUTH_URI=
   FIREBASE_TOKEN_URI=
   FIREBASE_AUTH_PROVIDER_X509_CERT_URL=
   FIREBASE_CLIENT_X509_CERT_URL=
   FIREBASE_UNIVERSE_DOMAIN=
   ```
5. Install required python packages
   ```
   pip install -r requirements.txt
   ```
6. Run the application
   ```
   python main.py
   ```

---

# Project Specifics

This project utilizes Firebase, which is a NoSQL collection style database. Should you feel more comfortable with something different, ensure that you remove the unnecessary environment variables from the `.env` file and adapt to your database of choosing.
