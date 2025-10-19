"""
services/report_generator.py - Servicio principal para generar reportes de reservaciones
"""
from typing import Dict, List, Any
from integrations.mews.client import MewsClient
from integrations.mews import endpoints
from data.cleaners import DataCleaner
from data.transformers import ReservationTransformer
from reports.google_sheet_writer import GoogleSheetWriter
import time

class ReportGenerator:
    """Genera reportes de reservaciones de Mews"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = MewsClient(
            api_base_url=config["API_BASE_URL"],
            client_token=config["CLIENT_TOKEN"],
            access_token=config["ACCESS_TOKEN"]
        )
        # Inicializar GoogleSheetWriter
        self.writer = GoogleSheetWriter(
            sheet_id=config["GOOGLE_SHEET_ID"],
            credentials_path=config["GOOGLE_CREDENTIALS_PATH"],
            sheet_name=config["GOOGLE_SHEET_NAME"]
        )
    
    def generate(self) -> bool:
        """Genera el reporte completo de reservaciones"""
        try:
            print("[INFO] Iniciando generación de reporte de reservaciones...")
            
            # 1. Obtener reservaciones
            print("[INFO] Obteniendo reservaciones...")
            reservations = self._get_reservations()
            if not reservations:
                print("[ERROR] No se encontraron reservaciones")
                return False
            
            # 2. Limpiar y extraer IDs
            print("[INFO] Limpiando datos...")
            cleaned_reservations = DataCleaner.clean_reservations(reservations)
            ids = DataCleaner.extract_ids(cleaned_reservations)
            
            # 3. Obtener datos relacionados
            print("[INFO] Obteniendo datos relacionados...")
            related_data = self._get_related_data(ids)
            
            # 4. Limpiar datos relacionados
            print("[INFO] Limpiando datos relacionados...")
            cleaned_related_data = self._clean_related_data(related_data)
            
            # 5. Transformar datos
            print("[INFO] Transformando datos...")
            transformer = self._create_transformer(cleaned_related_data)
            transformed_data = transformer.transform_reservations(cleaned_reservations)
            
            # 6. Generar reporte
            print("[INFO] Generando reporte...")
            success = self.writer.write_reservations(transformed_data)
            
            if success:
                print(f"[SUCCESS] Reporte generado exitosamente en Google Sheets: {self.writer.get_sheet_url()}")
                return True
            else:
                print("[ERROR] Error al generar reporte")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error en la generación del reporte: {e}")
            return False
    
    def _get_reservations(self) -> List[Dict[str, Any]]:
        """Obtiene las reservaciones de Mews"""
        return endpoints.get_reservations(
            client=self.client,
            start_utc=self.config["START_DATE"],
            end_utc=self.config["END_DATE"],
            limitation_count=self.config["LIMITATION_COUNT"]
        )
    
    def _get_related_data(self, ids: Dict[str, set]) -> Dict[str, Any]:
        """Obtiene todos los datos relacionados necesarios"""
        related_data = {}
        
        # Obtener nombres de grupos
        if ids["group_ids"]:
            print("  [INFO] Obteniendo nombres de grupos...")
            related_data["group_names"] = endpoints.get_group_names(
                client=self.client,
                group_ids=ids["group_ids"],
                start_utc=self.config["START_DATE"],
                end_utc=self.config["END_DATE"]
            )
        
        # Obtener información de clientes
        if ids["account_ids"]:
            print("  [INFO] Obteniendo información de clientes...")
            related_data["customer_info"] = endpoints.get_customer_names(
                client=self.client,
                account_ids=ids["account_ids"]
            )
        
        # Obtener nombres de tarifas
        print("  [INFO] Obteniendo nombres de tarifas...")
        related_data["rate_names"] = endpoints.get_rates_names(self.client)
        
        # Obtener precios de tarifas
        if ids["rate_ids"]:
            print("  [INFO] Obteniendo precios de tarifas...")
            related_data["rate_prices"] = endpoints.get_rates_pricing_batch(
                client=self.client,
                rate_ids=ids["rate_ids"],
                start_utc=self.config["START_DATE"],
                end_utc=self.config["END_DATE"],
                max_retries=self.config["MAX_RETRIES"]
            )
            time.sleep(self.config["RATE_LIMIT_DELAY"])
        
        # Obtener información de tarjeta de crédito
        print("  [INFO] Obteniendo información de tarjeta de crédito...")
        related_data["credit_card_info"] = endpoints.get_credit_card(
            client=self.client,
            start_utc=self.config["START_DATE"],
            end_utc=self.config["END_DATE"]
        )
        
        # Obtener productos por reservación
        if ids["reservation_ids"] and ids["service_ids"]:
            print("  [INFO] Obteniendo productos por reservación...")
            related_data["productos_por_reserva"] = endpoints.get_products_by_reservation(
                client=self.client,
                reservation_ids=list(ids["reservation_ids"]),
                service_ids=ids["service_ids"]
            )
        
        return related_data
    
    def _clean_related_data(self, related_data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia los datos relacionados"""
        cleaned_data = {}
        
        if "group_names" in related_data:
            cleaned_data["group_names"] = DataCleaner.clean_group_names(
                related_data["group_names"]
            )
        
        if "customer_info" in related_data:
            cleaned_data["customer_info"] = DataCleaner.clean_customer_data(
                related_data["customer_info"]
            )
        
        if "rate_names" in related_data and "rate_prices" in related_data:
            cleaned_names, cleaned_prices = DataCleaner.clean_rate_data(
                related_data["rate_names"],
                related_data["rate_prices"]
            )
            cleaned_data["rate_names"] = cleaned_names
            cleaned_data["rate_prices"] = cleaned_prices
        elif "rate_names" in related_data:
            cleaned_data["rate_names"] = DataCleaner.clean_group_names(
                related_data["rate_names"]
            )
            cleaned_data["rate_prices"] = {}
        
        if "credit_card_info" in related_data:
            cleaned_data["credit_card_info"] = related_data["credit_card_info"]
        
        if "productos_por_reserva" in related_data:
            cleaned_data["productos_por_reserva"] = related_data["productos_por_reserva"]
        else:
            cleaned_data["productos_por_reserva"] = {}
        
        return cleaned_data
    
    def _create_transformer(self, cleaned_data: Dict[str, Any]) -> ReservationTransformer:
        """Crea el transformador con los datos limpios"""
        return ReservationTransformer(
            group_names=cleaned_data.get("group_names", {}),
            customer_info=cleaned_data.get("customer_info", {}),
            rate_names=cleaned_data.get("rate_names", {}),
            rate_prices=cleaned_data.get("rate_prices", {}),
            productos_por_reserva=cleaned_data.get("productos_por_reserva", {}),
            credit_card_info=cleaned_data.get("credit_card_info", ("", "", "")),
            client=self.client
        )
