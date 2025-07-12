"""
mews_enpoints es el responsable de la lógica específica de cada recurso
Este archivo contiene funciones que representan acciones concretas con los datos de Mews, como obtener el nombre de los clientes, los paises etc 
Dejo el ejemplo de como queda la configuración del get_group_names
1. Hay que pasar todos los endpoints usados a esta clase como:
get_customer_names(...)
get_rates_names(...)
get_products_by_reservation(...)
get_credit_card(...)
get_room_name(...)
"""
from collections import defaultdict
from mews.utils import translate_country

def get_group_names(client, group_ids, start_utc, end_utc):
    if not group_ids:
        return {}

    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token,
        "UpdatedUtc": {"StartUtc": start_utc, "EndUtc": end_utc},
        "GroupIds": list(group_ids),
        "Limitation": {"Count": 30}
    }
    data = client.post("reservationGroups/getAll", payload)
    return {group["Id"]: group["Name"] for group in data.get("ReservationGroups", [])}