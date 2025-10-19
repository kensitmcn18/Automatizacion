"""
mews_endpoints es el responsable de la lógica específica de cada recurso
Este archivo contiene funciones que representan acciones concretas con los datos de Mews, como obtener el nombre de los clientes, los paises etc 
"""
from collections import defaultdict
from typing import Dict, Set, List
from util.utils import safe_post, safe_post_with_retry, translate_country

def get_reservations(client, start_utc: str, end_utc: str, limitation_count: int = 30) -> List[Dict]:
    """Obtiene todas las reservaciones de Mews"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token,
        "States": [
            "Inquired", "Confirmed", "Optional", "Started", "Processed", "Requested"
        ],
        "UpdatedUtc": {"StartUtc": start_utc, "EndUtc": end_utc},
        "Limitation": {"Count": limitation_count}
    }
    
    data = client.post("reservations/getAll/2023-06-06", payload)
    return data.get("Reservations", [])

def get_group_names(client, group_ids: Set[str], start_utc: str, end_utc: str) -> Dict[str, str]:
    """Obtiene los nombres de los grupos de reservación"""
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

def get_countries(client) -> Dict[str, str]:
    """Obtiene la lista de países y los traduce al español"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token
    }
    
    data = client.post("countries/getAll", payload)
    countries_data = data.get("Countries", [])
    return {country["Code"]: translate_country(country["EnglishName"]) for country in countries_data}

def get_customer_names(client, account_ids: Set[str]) -> Dict[str, Dict]:
    """Obtiene la información de los clientes"""
    if not account_ids:
        return {}
    
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token,
        "CustomerIds": list(account_ids),
        "Extent": {
            "Customers": True,
            "Addresses": True
        },
        "Limitation": {"Count": 30}
    }

    data = client.post("customers/getAll", payload)
    customers_data = data.get("Customers", [])
    countries_data = get_countries(client)

    customer_info = {}
    for customer in customers_data:
        customer_id = customer.get("Id", "")
        nationality_code = customer.get("NationalityCode", "")
        country_name = countries_data.get(nationality_code, "")
        
        address = customer.get("Address") or {}
        address_parts = [
            address.get("Line1"), 
            address.get("Line2"), 
            address.get("City"), 
            address.get("PostalCode"), 
            countries_data.get(address.get("CountryCode"), address.get("CountryCode"))
        ]
        formatted_address = ", ".join(filter(None, address_parts))
        
        send_marketing_emails = "No"
        if "Options" in customer and "SendMarketingEmails" in customer["Options"]:
            send_marketing_emails = "Yes"
       
        customer_info[customer_id] = {
            "Nombre": customer.get("FirstName", ""),
            "Apellido": customer.get("LastName", ""),
            "Correo": customer.get("Email", ""),
            "Telefono": customer.get("Phone", ""),
            "Direccion": formatted_address,
            "Nacionalidad": country_name,
            "Enviar correos electronicos de Marketing": send_marketing_emails
        }
    
    return customer_info

def get_rates_names(client) -> Dict[str, str]:
    """Obtiene los nombres de las tarifas"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token
    }
    
    data = client.post("rates/getAll", payload)
    rates_data = data.get("Rates", [])
    return {rate["Id"]: rate["Name"] for rate in rates_data if "Id" in rate and "Name" in rate}

def get_rates_pricing_batch(client, rate_ids: Set[str], start_utc: str, end_utc: str, max_retries: int = 5) -> Dict[str, str]:
    """Obtiene los precios de las tarifas con reintentos"""
    if not rate_ids:
        return {}
    
    rate_prices = {}
    currency_map = {"GBP": "£", "USD": "$", "EUR": "€"}
    
    for rate_id in rate_ids:
        if not rate_id:
            continue
            
        payload = {
            "ClientToken": client.client_token,
            "AccessToken": client.access_token, 
            "RateId": rate_id,
            "StartUtc": start_utc,
            "EndUtc": end_utc    
        }
        
        # Usar safe_post_with_retry para manejar rate limiting
        url = f"{client.api_base_url}/rates/getPricing"
        data = safe_post_with_retry(url, payload, client.headers, max_retries)
        
        for item in data.get("BaseAmountPrices", []):
            currency = item.get('Currency', '')
            gross_value = item.get('GrossValue', 0)
            symbol = currency_map.get(currency, currency)
            # Usar el rate_id del bucle, no el del item
            rate_prices[rate_id] = f"{symbol} {gross_value}"
    
    return rate_prices

def get_credit_card(client, start_utc: str, end_utc: str) -> tuple:
    """Obtiene información de tarjeta de crédito"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token,
        "UpdatedUtc": {"StartUtc": start_utc, "EndUtc": end_utc}
    }
    
    data = client.post("creditCards/getAll", payload)
    
    if data and "CreditCards" in data and data["CreditCards"]:
        for card in data["CreditCards"]:
            if card.get("ObfuscatedNumber"):
                return (
                    card.get("Type", ""), 
                    card.get("ObfuscatedNumber", ""), 
                    card.get("Expiration", "")
                )
    
    return "", "", ""

def get_room_name(client, service_id: str, resource_category_id: str) -> str:
    """Obtiene el nombre del tipo de habitación"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token, 
        "ResourceCategoryIds": [resource_category_id],
        "ServiceIds": [service_id]
    }
    
    data = client.post("resourceCategories/getAll", payload)
    
    if data and "ResourceCategories" in data and len(data["ResourceCategories"]) > 0:
        names = data["ResourceCategories"][0].get("Names", {})
        return names.get("en-US", "Tipo no encontrado")

    return "Datos no encontrados"

def get_room_number(client, assigned_resource_id: str) -> str:
    """Obtiene el número de habitación"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token,
        "ResourceIds": [assigned_resource_id]
    }
    
    data = client.post("resources/getAll", payload)
    
    if data and "Resources" in data and len(data["Resources"]) > 0:
        return data["Resources"][0].get("Name", "Número no encontrado")
    
    return "Datos no encontrados"

def get_products_by_reservation(client, reservation_ids: List[str], service_ids: Set[str]) -> Dict[str, str]:
    """Obtiene los productos por reservación"""
    payload = {
        "ClientToken": client.client_token,
        "AccessToken": client.access_token,
        "ServiceOrderIds": reservation_ids,
        "ServiceIds": list(service_ids),
        "Limitation": {"Count": 40}   
    }
    
    data = client.post("orderItems/getAll", payload)
    order_items = data.get("OrderItems", [])
    productos_por_reserva = defaultdict(list)
    
    for item in order_items:
        res_id = item.get("ServiceOrderId")
        product_type = item.get("Type", "").strip()
        
        if product_type == "ProductOrder":
            nombre_producto = item.get("BillingName", "").strip()
            cantidad = item.get("UnitCount", 1)
            valor = f"{cantidad} x {nombre_producto}"
            
            if res_id and valor:
                productos_por_reserva[res_id].append(valor)

    return {
        res_id: ", ".join(sorted(set(productos)))
        for res_id, productos in productos_por_reserva.items()
    }