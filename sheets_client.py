import requests
from deep_translator import GoogleTranslator
import pandas as pd
from collections import defaultdict
from datetime import datetime

CLIENTOKEN = "E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D"
ACCESSTOKEN = "C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D"
HEADERS = {"Content-Type": "application/json"}
START_DATE = "2025-05-06T01:00:00Z"
END_DATE = "2025-05-08T23:00:00Z"

def get_mews_reservations():
    url_reservations = "https://api.mews-demo.com/api/connector/v1/reservations/getAll/2023-06-06"
    
    
    payload_reservations = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "States": [
            "Inquired",
            "Confirmed",
            "Optional",
            "Started",
            "Processed",
            "Requested"
        ],
        "UpdatedUtc": {"StartUtc": START_DATE, 
                        "EndUtc": END_DATE},
        "Limitation": {"Count": 30}
    }
    
    response = requests.post(url_reservations, json=payload_reservations, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        reservations = data.get("Reservations", [])

        if reservations:
            
            reservation_ids = [reserva["Id"] for reserva in reservations]
            service_ids = {reserva.get("ServiceId") for reserva in reservations if reserva.get("ServiceId")}
            group_ids = {reserva.get("GroupId") for reserva in reservations if reserva.get("GroupId")}
            account_ids = {reserva.get("AccountId") for reserva in reservations if reserva.get("AccountId")}
            counts = [person["Count"] for reservation in data.get("Reservations", []) for person in reservation.get("PersonCounts", [])]
            productos_por_reserva = get_products_by_reservation(reservation_ids, service_ids)
            
                
            
                            
            group_names = get_group_names(group_ids)
            customer_info = get_customer_names(account_ids)
            payments_info_by_reservation  = get_payments(reservation_ids)
            rate_name = get_rates_names()
            
        
            reservas_filtradas = []    
            for reserva in reservations:
                service_id = reserva.get("ServiceId")
                reservation_ids = [reserva["Id"]for reserva in reservations]
                reservation_id = reserva["Id"]
                               
                if not reserva.get("CreditCardId"):
                    tipo_tarjeta, numero_tarjeta, expiracion_tarjeta = "", "", ""
                else:
                    tipo_tarjeta, numero_tarjeta, expiracion_tarjeta = get_credit_card()
                
                fecha_llegada_str = reserva.get("ScheduledStartUtc")
                fecha_salida_str = reserva.get("ScheduledEndUtc")
            try:
                   
                    fecha_llegada = datetime.strptime(fecha_llegada_str, "%Y-%m-%dT%H:%M:%SZ").date()
                    fecha_salida = datetime.strptime(fecha_salida_str,"%Y-%m-%dT%H:%M:%SZ").date()
                    recuento_noches = (fecha_salida - fecha_llegada).days
                    
            except Exception as e: 
                print(f"Error al calcular noches para reserva {reserva.get('Number')}: {e}")
                recuento_noches = "N/A"
            
            
           
            reservas_filtradas = [
                {
                    "Numero": reserva.get("Number", "N/A"),
                    "Grupo": group_names.get(reserva.get("GroupId"), "N/A"),
                    "Apellido": customer_info.get(reserva.get("AccountId"), {}).get("Apellido", "N/A"),
                    "Nombre": customer_info.get(reserva.get("AccountId"), {}).get("Nombre", "N/A"),
                    "Correo": customer_info.get(reserva.get("AccountId"), {}).get("Correo", "N/A"),
                    "Teléfono": customer_info.get(reserva.get("AccountId"), {}).get("Telefono", "N/A"),
                    "Direccion": customer_info.get(reserva.get("AccountId"), {}).get("Direccion", "N/A"),
                    "Nacionalidad": customer_info.get(reserva.get("AccountId"), {}).get("Nacionalidad", "N/A"),
                    "RecibeCorreosMarketing": customer_info.get(reserva.get("AccountId"), {}).get("Enviar correos electronicos de Marketing", "N/A"),
                    "Estado": reserva.get("State", "N/A"), 
                    "Fecha de creación": reserva.get("CreatedUtc", "N/A"),
                    "Fecha de actualización": reserva.get("UpdatedUtc", "N/A"),
                    "Fecha llegada": reserva.get("ScheduledStartUtc", "N/A"),
                    "Fecha salida": reserva.get("ScheduledEndUtc", "N/A"),
                    "Recuento noches": recuento_noches,
                    "Personas": sum(person["Count"] for person in reserva.get("PersonCounts", []) if "Count" in person),
                    "Tipo habitación": get_room_name(reserva.get("ServiceId"), reserva.get("RequestedResourceCategoryId")),
                    "Número habitación": get_room_number(reserva.get("AssignedResourceId")),
                    "tarifa": rate_name.get(reserva.get("RateId")),
                    "Precio": get_rates_pricing(reserva.get("RateId")),
                    "Producto": productos_por_reserva.get(reserva.get("Id"),"N/A"),
                    "Tipo tarjeta": tipo_tarjeta,
                    "Numero de tarjeta": numero_tarjeta,
                    "Fecha vencimiento": expiracion_tarjeta,
                    "Pago": format_payment(payments_info_by_reservation.get(reserva.get("Id"))),
                    "motivo de la reserva": reserva.get("Purpose", "N/A")
                    }
                    
            for reserva in reservations
            ]
            print(f"Fecha llegada raw: '{fecha_llegada_str}' (tipo: {type(fecha_llegada_str)})")
            print(f"Fecha salida raw: '{fecha_salida_str}' (tipo: {type(fecha_salida_str)})")
                
            
            df = pd.DataFrame(reservas_filtradas)
            df.to_excel("reservas_mews.xlsx", index=False)  
            print("Archivo 'reservas_mews.xlsx' guardado exitosamente.")
        else:
            print("No se encontraron reservas en la respuesta.")
            
    else:
        print(f"Error {response.status_code}: {response.text}")

def get_group_names(group_ids):
    if not group_ids:
        return {}
    
    url_groups = "https://api.mews-demo.com/api/connector/v1/reservationGroups/getAll"
    
    
    payload_groups = {
       "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "UpdatedUtc": {"StartUtc": START_DATE, 
                        "EndUtc": END_DATE},
        "GroupIds": list(group_ids),
        "Limitation": {"Count": 30}
    }
    
    response = requests.post(url_groups, json=payload_groups, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        return {group["Id"]: group["Name"] for group in data.get("ReservationGroups", [])}
    else:
        print(f"Error {response.status_code} al obtener nombres de grupos: {response.text}")
        return {}
def translate_country(country_name):
    
    if not country_name:
        return "N/A"
    try:
        return GoogleTranslator(source="en", target="es").translate(country_name)
    except Exception:
        return country_name 

def get_countries():
    url_countries = "https://api.mews-demo.com/api/connector/v1/countries/getAll"
    
    payload_countries = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN}
    response = requests.post(url_countries, json=payload_countries, headers=HEADERS)
    
    if response.status_code == 200:
        countries_data = response.json().get("Countries", [])
        country_dict = {country["Code"]: translate_country(country["EnglishName"]) for country in countries_data}
        
        return country_dict
    return {}

def get_customer_names(account_ids):
    if not account_ids:
        return {}
    
    url_customers = "https://api.mews-demo.com/api/connector/v1/customers/getAll"

    payload_customers = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "CustomerIds": list(account_ids),
        "Extent": {
                "Customers": True,
                "Addresses": True},
        "Limitation": {"Count": 30}, 
        
    }

    response = requests.post(url_customers, json=payload_customers, headers=HEADERS)

    if response.status_code == 200:
        customers_data = response.json().get("Customers", [])
        countries_data = get_countries()

        customer_info = {}
        for customer in customers_data:
            customer_id = customer.get("Id", "N/A")
            nationality_code = customer.get("NationalityCode", "N/A")
            country_name = countries_data.get(nationality_code)
    
            
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
                "Nombre": customer.get("FirstName", "N/A"),
                "Apellido": customer.get("LastName", "N/A"),
                "Correo": customer.get("Email","N/A"),
                "Telefono": customer.get("Phone","N/A"),
                "Direccion": formatted_address,
                "Nacionalidad": country_name,
                "Enviar correos electronicos de Marketing": send_marketing_emails
                
            }
        return customer_info
    else:
        print(f"Error {response.status_code} al obtener clientes: {response.text}")
        return {}

def get_rates_names():
    url_rates_names = "https://api.mews-demo.com/api/connector/v1/rates/getAll"

    payload_rates_names = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN
    }
    response = requests.post(url_rates_names, json=payload_rates_names, headers=HEADERS)

    if response.status_code == 200:
        rates_data = response.json().get("Rates", [])
        return {rate["Id"]: rate["Name"] for rate in rates_data if "Id" in rate and "Name" in rate}
    else:
        print(f"Error al obtener nombres de tarifas: {response.status_code} - {response.text}")
        return {}

def get_rates_pricing(rate_id):
    if not rate_id:
        return None
    
    url_rates = "https://api.mews-demo.com/api/connector/v1/rates/getpricing"
    
    payload_rates = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN, 
        "RateId": rate_id,
        "StartUtc": START_DATE,
        "EndUtc": END_DATE    
    }
    response = requests.post(url_rates, json=payload_rates, headers=HEADERS)
    
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print(f"Error al convertir respuesta de {rate_id} a JSON.")
            return None
        
        if "BaseAmountPrices" in data and data["BaseAmountPrices"]:
            price_info = data["BaseAmountPrices"][0]
            currency_map = {"GBP": "£", "USD": "$"}
            currency_symbol = currency_map.get(price_info.get("Currency"), price_info.get("Currency", "N/A"))
            gross_value = price_info.get("GrossValue", 0)
            
            return f"{currency_symbol} {gross_value}"
    
    print(f"Error {response.status_code} al obtener precios de {rate_id}: {response.text}")
    return None

def get_all_rates_prices(rate_ids):
    
    all_prices = []
    
    for rate_id in rate_ids:
        if isinstance(rate_id, str):  
            price = get_rates_pricing(rate_id)
            if price:
                all_prices.append(price)
            
        else:
            print(f"⚠️ RateId inválido: {rate_id} (debe ser string)")
    
    return all_prices

rate_ids = [
    "89e8b0c9-3526-4773-8040-b235009cb80b",
    "b8c1b67f-704e-4112-8e68-b15b0094d112",
    "ac0e8ce6-5078-4a55-be60-b19600a4314d",
    "146714c4-ebb1-4c36-9b59-b13f00ac1d39" 
]
               
prices = get_all_rates_prices(rate_ids)

def get_credit_card(Credit_card): 
    url_card = "https://api.mews-demo.com/api/connector/v1/creditCards/getAll"
    payload_card = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "UpdatedUtc": {"StartUtc": START_DATE, 
                        "EndUtc": END_DATE}
    }
    
    response = requests.post(url_card, json=payload_card, headers=HEADERS)
    if response.status_code == 200: 
        card_data = response.json()
        if not card_data or "CreditCards" not in card_data or not card_data["CreditCards"]:
            return "", "", ""  

        for card in card_data["CreditCards"]:
            if card.get("ObfuscatedNumber"):  
                return card.get("Type", ""), card.get("ObfuscatedNumber", ""), card.get("Expiration", "")

    return "", "", ""

def get_payments(reservation_ids): 
    url_payment = "https://api.mews-demo.com/api/connector/v1/payments/getAll"
    payload_payment = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "UpdatedUtc": {"StartUtc": START_DATE, 
                        "EndUtc": END_DATE},
        "Limitation": {"Count": 30}         
    }
    response = requests.post(url_payment, json=payload_payment, headers=HEADERS)
    
    payments_by_reservation ={}

    if response.status_code == 200:
        data = response.json()
        for payment in data.get("Payments",):
            reservation_id = payment.get("ReservationId")
            amount_info = payment.get("Amount", {})
            payment_data = {
                "Currency": amount_info.get("Currency"),
                "GrossValue": amount_info.get("GrossValue")
        }
            if reservation_id in reservation_ids:
                if reservation_id not in payments_by_reservation:
                    payments_by_reservation[reservation_id]  = []
                payments_by_reservation[reservation_id].append(payment_data)
    else:
        print(f"Error al obtener pagos: {response.status_code} - {response.text}")

    return payments_by_reservation

def format_payment(payments):
    if payments and isinstance(payments, list):
        formatted_payments = []
        for payment in payments:
            currency = payment.get("Currency")
            gross_value = payment.get("GrossValue")
            if currency and gross_value is not None:
                formatted_payments.append(f"{abs(gross_value)} {currency}")
        return ", ".join(formatted_payments) if formatted_payments else "N/A"
    return "N/A"
        
    
def get_room_name(service_id, resource_category_id):
    url = "https://api.mews-demo.com/api/connector/v1/resourceCategories/getAll"
    
    
    payload = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN, 
        "ResourceCategoryIds": [resource_category_id],
        "ServiceIds": [service_id]
    }
    
    response = requests.post(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        if data and "ResourceCategories" in data and len(data["ResourceCategories"]) > 0:
            names = data["ResourceCategories"][0].get("Names", {})
            return names.get("en-US", "Tipo no encontrado")
        return "Datos no encontrados"
    else:
        return "Información no encontrada"

def get_room_number(assigned_resource_id):
    url_resources = "https://api.mews-demo.com/api/connector/v1/resources/getAll"
  
    
    payload = {
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "ResourceIds": [assigned_resource_id]
    }
    
    response = requests.post(url_resources, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        if data and "Resources" in data and len(data["Resources"]) > 0:
            return data["Resources"][0].get("Name", "Número no encontrado")
        return "Datos no encontrados"
    else:
        return "Información no encontrada"
    
def get_products_by_reservation(reservation_ids, service_ids):
    url_items = "https://api.mews-demo.com/api/connector/v1/orderItems/getAll"
    payload ={
        "ClientToken": CLIENTOKEN,
        "AccessToken": ACCESSTOKEN,
        "ServiceOrderIds": list(reservation_ids),
        "ServiceIds": list(service_ids),
        "Limitation": {"Count": 40}   
    }
    
    response = requests.post(url_items, json=payload, headers=HEADERS)
    
    
    if response.status_code == 200:
        order_items =  response.json().get("OrderItems", [])
        productos_por_reserva = defaultdict(list)
        valor = ""
        for item in order_items:
            res_id = item.get("ServiceOrderId")
            productType = item.get("Type", "").strip()
            if productType == "ProductOrder":
                nombre_producto = item.get("BillingName", "").strip()
                cantidad = item.get("UnitCount",1)
                valor = str(cantidad) + " x " + nombre_producto
            if res_id and valor != "":
                productos_por_reserva[res_id].append(valor)

        return {
            res_id: ", ".join(sorted(set(productos)))
            for res_id, productos in productos_por_reserva.items()
        }
    else:
        print(f"Error al obtener OrderItems: {response.status_code} - {response.text}")
        return {}
        
    
# def get_product(service_ids):
#     url_products= "https://api.mews-demo.com/api/connector/v1/products/getAll"
#     payload = {
#         "ClientToken": CLIENTOKEN,
#         "AccessToken": ACCESSTOKEN,
#         "ServiceIds": list(service_ids),
#         "UpdatedUtc": {"StartUtc": START_DATE, 
#                         "EndUtc": END_DATE},
#         "Limitation": {"Count": 40}
#     }
#     response = requests.post(url_products, json=payload, headers=HEADERS)
    
#     if response.status_code == 200:
#         products_data = response.json().get("Products", [])
        
        
#         product_names = []
#         for producto in products_data:
#             if producto.get("IsActive"):
#                 name_dict = producto.get("Names", {})
#                 name = name_dict.get("en-US") or list(name_dict.values())[0]  
#                 if name:
#                     product_names.append(name)

        
#         return ", ".join(sorted(set(product_names)))
    
#     else:
#         print(f"Error al obtener productos: {response.status_code} - {response.text}")
#         return "No disponible"

if __name__ == "__main__":
    get_mews_reservations()
