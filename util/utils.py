# mews/utils.py
import requests
import time
from deep_translator import GoogleTranslator
from datetime import datetime, timedelta
import pytz
from typing import Optional

def safe_post(url, payload, headers):
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] Error calling {url}: {e}")
    return {}

def safe_post_with_retry(url, payload, headers, max_retries=5, rate_limit_delay=0.5):
    """Realiza una petición POST con reintentos y manejo de rate limiting"""
    wait_time = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", wait_time))
                print(f"⏳ Rate limit alcanzado. Esperando {retry_after} segundos...")
                time.sleep(retry_after)
                wait_time = min(wait_time * 2, 60)
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            break
    
    print(f"❌ Fallo después de {max_retries} intentos")
    return {}

def translate_country(country_name: str) -> str:
    """Traduce el nombre del país del inglés al español"""
    if not country_name:
        return ""
    try:
        return GoogleTranslator(source="en", target="es").translate(country_name)
    except Exception:
        return country_name

def parse_datetime(date_string: str) -> Optional[datetime]:
    """Parsea una fecha en múltiples formatos"""
    if not date_string:
        return None
    
    formatos = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S",
    ]
    
    for formato in formatos:
        try:
            return datetime.strptime(date_string.strip(), formato)
        except ValueError:
            continue
    
    return None

def calculate_nights(start_date_str: str, end_date_str: str) -> int:
    """Calcula el número de noches entre dos fechas"""
    try:
        start_date = parse_datetime(start_date_str)
        end_date = parse_datetime(end_date_str)
        
        if not start_date or not end_date:
            return 0
        
        start_date = start_date.date()
        end_date = end_date.date()
        
        nights = (end_date - start_date).days
        return max(nights, 0)
    except Exception as e:
        print(f"Error al calcular noches: {e}")
        return 0
def get_yesterday_range(timezone='America/Bogota'):
    """Obtiene el rango de ayer completo (00:00 - 23:59)"""
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    
    yesterday = now - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = yesterday.replace(hour=23, minute=59, second=59)
    
    return (
        start.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
        end.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    )

def get_date_range(days_ago=1, timezone='America/Bogota'):
    """
    Obtiene el rango de un día específico hace X días.
    
    Args:
        days_ago: Hace cuántos días (1 = ayer, 0 = hoy)
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    
    target_day = now - timedelta(days=days_ago)
    start = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = target_day.replace(hour=23, minute=59, second=59)
    
    return (
        start.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
        end.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    )