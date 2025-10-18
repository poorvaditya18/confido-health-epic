import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    EPIC_CLIENT_ID = os.getenv("EPIC_CLIENT_ID")
    EPIC_PRIVATE_KEY_PATH = os.getenv("EPIC_PRIVATE_KEY_PATH")
    EPIC_TOKEN_URL = os.getenv("EPIC_TOKEN_URL")
    EPIC_SCOPES = os.getenv("EPIC_SCOPES", "system/Patient.read system/Appointment.read system/Practitioner.read system/Patient.search system/Appointment.search system/Location.read System/Location.search system/Practitioner.search system/Patient/*.read system/Appointment/*.read system/Group.read").split()
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")