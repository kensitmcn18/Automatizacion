# En config.py se va a realizar la configuracion los accesos globales que requiere el proyecto, aqui se cargan las parametrizaciones hechas en el .env
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = {
    "API_BASE_URL": os.getenv("MEWS_API_BASE_URL"),
    "CLIENT_TOKEN": os.getenv("MEWS_CLIENT_TOKEN"),
    "ACCESS_TOKEN": os.getenv("MEWS_ACCESS_TOKEN"),
    "START_DATE": "2025-05-06T01:00:00Z",
    "END_DATE": "2025-05-08T23:00:00Z",
    "SHEET_OUTPUT_PATH": "reservas_mews.xlsx"
}
