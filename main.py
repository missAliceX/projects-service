from configparser import ConfigParser
from src.service import Service
import os


svc = Service(ConfigParser(os.environ)["DEFAULT"])
svc.start()
