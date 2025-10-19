"""
data/cleaners.py - Limpiadores de datos para validar y limpiar datos de Mews
"""
from typing import Dict, List, Any, Set
from datetime import datetime

class DataCleaner:
    """Limpia y valida los datos de Mews antes de la transformación"""
    
    @staticmethod
    def clean_reservations(reservations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limpia y valida las reservaciones"""
        cleaned_reservations = []
        
        for reservation in reservations:
            if DataCleaner._is_valid_reservation(reservation):
                cleaned_reservation = DataCleaner._clean_reservation(reservation)
                cleaned_reservations.append(cleaned_reservation)
        
        return cleaned_reservations
    
    @staticmethod
    def extract_ids(reservations: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Extrae todos los IDs necesarios de las reservaciones"""
        reservation_ids = set()
        service_ids = set()
        group_ids = set()
        account_ids = set()
        rate_ids = set()
        
        for reservation in reservations:
            if reservation.get("Id"):
                reservation_ids.add(reservation["Id"])
            
            if reservation.get("ServiceId"):
                service_ids.add(reservation["ServiceId"])
            
            if reservation.get("GroupId"):
                group_ids.add(reservation["GroupId"])
            
            if reservation.get("AccountId"):
                account_ids.add(reservation["AccountId"])
            
            if reservation.get("RateId"):
                rate_ids.add(reservation["RateId"])
        
        return {
            "reservation_ids": reservation_ids,
            "service_ids": service_ids,
            "group_ids": group_ids,
            "account_ids": account_ids,
            "rate_ids": rate_ids
        }
    
    @staticmethod
    def clean_customer_data(customer_info: Dict[str, Dict]) -> Dict[str, Dict]:
        """Limpia los datos de clientes"""
        cleaned_customers = {}
        
        for customer_id, customer_data in customer_info.items():
            cleaned_customer = {
                "Nombre": DataCleaner._clean_string(customer_data.get("Nombre", "")),
                "Apellido": DataCleaner._clean_string(customer_data.get("Apellido", "")),
                "Correo": DataCleaner._clean_email(customer_data.get("Correo", "")),
                "Telefono": DataCleaner._clean_string(customer_data.get("Telefono", "")),
                "Direccion": DataCleaner._clean_string(customer_data.get("Direccion", "")),
                "Nacionalidad": DataCleaner._clean_string(customer_data.get("Nacionalidad", "")),
                "Enviar correos electronicos de Marketing": DataCleaner._clean_boolean(
                    customer_data.get("Enviar correos electronicos de Marketing", "")
                )
            }
            cleaned_customers[customer_id] = cleaned_customer
        
        return cleaned_customers
    
    @staticmethod
    def clean_group_names(group_names: Dict[str, str]) -> Dict[str, str]:
        """Limpia los nombres de grupos"""
        return {
            group_id: DataCleaner._clean_string(name)
            for group_id, name in group_names.items()
        }
    
    @staticmethod
    def clean_rate_data(rate_names: Dict[str, str], rate_prices: Dict[str, str]) -> tuple:
        """Limpia los datos de tarifas"""
        cleaned_names = {
            rate_id: DataCleaner._clean_string(name)
            for rate_id, name in rate_names.items()
        }
        
        cleaned_prices = {}
        for rate_id, price in rate_prices.items():
            cleaned_price = DataCleaner._clean_price(price)
            if cleaned_price:
                cleaned_prices[rate_id] = cleaned_price
        
        return cleaned_names, cleaned_prices
    
    @staticmethod
    def _is_valid_reservation(reservation: Dict[str, Any]) -> bool:
        """Valida si una reservación es válida"""
        required_fields = ["Id", "Number"]
        return all(reservation.get(field) for field in required_fields)
    
    @staticmethod
    def _clean_reservation(reservation: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia una reservación individual"""
        return {
            key: DataCleaner._clean_value(value)
            for key, value in reservation.items()
        }
    
    @staticmethod
    def _clean_value(value: Any) -> Any:
        """Limpia un valor individual"""
        if isinstance(value, str):
            return DataCleaner._clean_string(value)
        elif isinstance(value, (int, float)):
            return value if value >= 0 else 0
        elif isinstance(value, list):
            return [DataCleaner._clean_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: DataCleaner._clean_value(v) for k, v in value.items()}
        else:
            return value
    
    @staticmethod
    def _clean_string(value: str) -> str:
        """Limpia una cadena de texto"""
        if not value:
            return ""
        
        cleaned = str(value).strip()
        return cleaned if cleaned else ""
    
    @staticmethod
    def _clean_email(email: str) -> str:
        """Limpia y valida un email"""
        if not email:
            return ""
        
        cleaned = email.strip().lower()
        if "@" in cleaned and "." in cleaned:
            return cleaned
        else:
            return ""
    
    @staticmethod
    def _clean_boolean(value: str) -> str:
        """Limpia un valor booleano"""
        if not value:
            return "No"
        
        cleaned = str(value).strip().lower()
        if cleaned in ["yes", "true", "1", "si", "sí"]:
            return "Yes"
        else:
            return "No"
    
    @staticmethod
    def _clean_price(price: str) -> str:
        """Limpia un precio"""
        if not price:
            return ""
        
        cleaned = str(price).strip()
        if cleaned and cleaned != "":
            return cleaned
        else:
            return ""
