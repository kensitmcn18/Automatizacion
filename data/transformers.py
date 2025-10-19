"""
data/transformers.py - Transformadores de datos para convertir datos de Mews al formato de reporte
"""
from typing import Dict, List, Any, Optional
from util.utils import calculate_nights
from integrations.mews import endpoints

class ReservationTransformer:
    """Transforma los datos de reservaciones de Mews al formato del reporte"""
    
    def __init__(self, group_names: Dict[str, str], customer_info: Dict[str, Dict], 
                 rate_names: Dict[str, str], rate_prices: Dict[str, str],
                 productos_por_reserva: Dict[str, str], credit_card_info: tuple,
                 client: Optional[Any] = None):
        self.group_names = group_names
        self.customer_info = customer_info
        self.rate_names = rate_names
        self.rate_prices = rate_prices
        self.productos_por_reserva = productos_por_reserva
        self.tipo_tarjeta, self.numero_tarjeta, self.expiracion_tarjeta = credit_card_info
        self.client = client
    
    def transform_reservation(self, reservation: Dict[str, Any]) -> Dict[str, Any]:
        """Transforma una reservación individual al formato del reporte"""
        account_id = reservation.get("AccountId")
        customer_data = self.customer_info.get(account_id, {})
        
        # Calcular noches y camas
        noches = calculate_nights(
            reservation.get("ScheduledStartUtc", ""),
            reservation.get("ScheduledEndUtc", "")
        )
        
        personas = sum(person["Count"] for person in reservation.get("PersonCounts", []) if "Count" in person)
        camas = noches * personas if noches > 0 and personas > 0 else 0
        
        # Calcular importe total
        rate_id = reservation.get("RateId")
        precio_str = self.rate_prices.get(rate_id, "")
        importe_total = self._calculate_total_amount(precio_str, noches)
        
        return {
            "Numero": reservation.get("Number", ""),
            "Grupo": self.group_names.get(reservation.get("GroupId"), ""),
            "Apellido": customer_data.get("Apellido", ""),
            "Nombre": customer_data.get("Nombre", ""),
            "Correo": customer_data.get("Correo", ""),
            "Teléfono": customer_data.get("Telefono", ""),
            "Direccion": customer_data.get("Direccion", ""),
            "Nacionalidad": customer_data.get("Nacionalidad", ""),
            "RecibeCorreosMarketing": customer_data.get("Enviar correos electronicos de Marketing", ""),
            "Estado": reservation.get("State", ""), 
            "Fecha de creación": reservation.get("CreatedUtc", ""),
            "Fecha de actualización": reservation.get("UpdatedUtc", ""),
            "Fecha llegada": reservation.get("ScheduledStartUtc", ""),
            "Fecha salida": reservation.get("ScheduledEndUtc", ""),
            "Recuento noches": noches if noches > 0 else "",
            "Cantidad de Personas": personas,
            "Recuento camas": camas if camas > 0 else "",
            "Tipo habitación": self._get_room_name(reservation),
            "Numero habitación": self._get_room_number(reservation),
            "tarifa": self.rate_names.get(reservation.get("RateId"), ""),
            "Productos": self.productos_por_reserva.get(reservation.get("Id"), ""),
            "Precio": precio_str,
            "Importe total": importe_total,
            "Tipo tarjeta": self.tipo_tarjeta,
            "Numero de tarjeta": self.numero_tarjeta,
            "Fecha vencimiento": self.expiracion_tarjeta,
            "motivo de la reserva": reservation.get("Purpose", "")
        }
    
    def transform_reservations(self, reservations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transforma una lista de reservaciones"""
        return [self.transform_reservation(reservation) for reservation in reservations]
    
    def _get_room_name(self, reservation: Dict[str, Any]) -> str:
        """Obtiene el nombre del tipo de habitación"""
        if not self.client:
            return ""
        
        service_id = reservation.get("ServiceId")
        resource_category_id = reservation.get("RequestedResourceCategoryId")
        
        if not service_id or not resource_category_id:
            return ""
        
        try:
            return endpoints.get_room_name(self.client, service_id, resource_category_id)
        except Exception as e:
            print(f"Error al obtener nombre de habitación: {e}")
            return ""
    
    def _get_room_number(self, reservation: Dict[str, Any]) -> str:
        """Obtiene el número de habitación"""
        if not self.client:
            return ""
        
        assigned_resource_id = reservation.get("AssignedResourceId")
        
        if not assigned_resource_id:
            return ""
        
        try:
            return endpoints.get_room_number(self.client, assigned_resource_id)
        except Exception as e:
            print(f"Error al obtener número de habitación: {e}")
            return ""
    
    def _calculate_total_amount(self, precio_str: str, noches: int) -> str:
        """Calcula el importe total basado en el precio y número de noches"""
        try:
            if not precio_str or not isinstance(noches, int) or noches <= 0:
                return ""
            
            if " " not in precio_str:
                return ""
                
            simbolo, valor_str = precio_str.split(" ", 1)
            valor = float(valor_str.replace(',', ''))
            return f"{simbolo} {round(valor * noches, 2)}"
        except Exception as e:
            print(f"Error al calcular importe total: {e}")
            return ""
