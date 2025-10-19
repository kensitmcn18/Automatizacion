# En config.py se va a realizar la configuracion los accesos globales que requiere el proyecto, aqui se cargan las parametrizaciones hechas en el .env
from dotenv import load_dotenv
import os
from util.utils import get_yesterday_range

load_dotenv()

# Obtener la ruta absoluta del directorio del proyecto
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Calcular fechas dinámicas usando la función robusta que maneja zona horaria
START_DATE, END_DATE = get_yesterday_range(timezone='Europe/Madrid')

CONFIG = {
    "API_BASE_URL": os.getenv("MEWS_API_BASE_URL", "https://api.mews-demo.com/api/connector/v1"),
    "CLIENT_TOKEN": os.getenv("MEWS_CLIENT_TOKEN", "E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D"),
    "ACCESS_TOKEN": os.getenv("MEWS_ACCESS_TOKEN", "C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D"),
    "START_DATE": START_DATE,
    "END_DATE": END_DATE,
    "HEADERS": {"Content-Type": "application/json"},
    "LIMITATION_COUNT": 30,
    "MAX_RETRIES": 5,
    "RATE_LIMIT_DELAY": 0.5,
    # Google Sheets Configuration
    "GOOGLE_SHEET_ID": os.getenv("GOOGLE_SHEET_ID"),
    "GOOGLE_CREDENTIALS_PATH": os.getenv("GOOGLE_CREDENTIALS_PATH", os.path.join(PROJECT_DIR, "credentials.json")),
    "GOOGLE_SHEET_NAME": os.getenv("GOOGLE_SHEET_NAME", "Reservas Mews")
}
