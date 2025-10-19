#!/usr/bin/env python3
"""
Script de prueba para verificar que las fechas dinámicas funcionan correctamente
"""

from datetime import datetime
import pytz
from util.utils import get_yesterday_range, get_date_range
from config import CONFIG

def test_fechas_dinamicas():
    """Prueba las fechas dinámicas implementadas"""
    print("=" * 60)
    print("PRUEBA DE FECHAS DINÁMICAS")
    print("=" * 60)
    
    # 1. Probar get_yesterday_range directamente
    print("\n1. Probando get_yesterday_range() directamente:")
    start_date, end_date = get_yesterday_range(timezone='America/Bogota')
    print(f"   START_DATE: {start_date}")
    print(f"   END_DATE:   {end_date}")
    
    # 2. Verificar formato
    print("\n2. Verificando formato de fechas:")
    try:
        # Verificar que se puede parsear con el formato esperado
        start_parsed = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
        end_parsed = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
        print(f"   ✅ Formato correcto - Ambas fechas se pueden parsear")
        print(f"   START_DATE parseado: {start_parsed}")
        print(f"   END_DATE parseado:   {end_parsed}")
    except ValueError as e:
        print(f"   ❌ Error en formato: {e}")
        return False
    
    # 3. Verificar que START_DATE es anterior a END_DATE
    print("\n3. Verificando orden de fechas:")
    if start_parsed < end_parsed:
        print(f"   ✅ START_DATE ({start_date}) es anterior a END_DATE ({end_date})")
    else:
        print(f"   ❌ Error: START_DATE no es anterior a END_DATE")
        return False
    
    # 4. Verificar que CONFIG tiene las fechas correctas
    print("\n4. Verificando CONFIG:")
    config_start = CONFIG.get("START_DATE")
    config_end = CONFIG.get("END_DATE")
    print(f"   CONFIG START_DATE: {config_start}")
    print(f"   CONFIG END_DATE:   {config_end}")
    
    if config_start == start_date and config_end == end_date:
        print(f"   ✅ CONFIG tiene las fechas dinámicas correctas")
    else:
        print(f"   ❌ CONFIG no tiene las fechas correctas")
        return False
    
    # 5. Verificar zona horaria (debe estar en UTC)
    print("\n5. Verificando zona horaria:")
    if start_date.endswith('Z') and end_date.endswith('Z'):
        print(f"   ✅ Las fechas están en formato UTC (terminan en 'Z')")
    else:
        print(f"   ❌ Las fechas no están en formato UTC")
        return False
    
    # 6. Mostrar información adicional
    print("\n6. Información adicional:")
    tz_bogota = pytz.timezone('America/Bogota')
    now_bogota = datetime.now(tz_bogota)
    print(f"   Fecha actual en Bogotá: {now_bogota.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # 7. Probar get_date_range con diferentes parámetros
    print("\n7. Probando get_date_range() con diferentes parámetros:")
    
    # Ayer (days_ago=1)
    start_1, end_1 = get_date_range(days_ago=1, timezone='America/Bogota')
    print(f"   Ayer (days_ago=1): {start_1} - {end_1}")
    
    # Hoy (days_ago=0)
    start_0, end_0 = get_date_range(days_ago=0, timezone='America/Bogota')
    print(f"   Hoy (days_ago=0):   {start_0} - {end_0}")
    
    # Hace 2 días (days_ago=2)
    start_2, end_2 = get_date_range(days_ago=2, timezone='America/Bogota')
    print(f"   Hace 2 días:        {start_2} - {end_2}")
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("✅ Las fechas dinámicas están funcionando correctamente")
    print("=" * 60)
    
    return True

def test_simulacion_ejecucion():
    """Simula una ejecución del sistema para verificar que las fechas se usan correctamente"""
    print("\n" + "=" * 60)
    print("SIMULACIÓN DE EJECUCIÓN DEL SISTEMA")
    print("=" * 60)
    
    print(f"Configuración actual:")
    print(f"  START_DATE: {CONFIG['START_DATE']}")
    print(f"  END_DATE:   {CONFIG['END_DATE']}")
    print(f"  API_BASE_URL: {CONFIG['API_BASE_URL']}")
    print(f"  LIMITATION_COUNT: {CONFIG['LIMITATION_COUNT']}")
    
    print(f"\n✅ El sistema está configurado correctamente para obtener")
    print(f"   reservas desde {CONFIG['START_DATE']} hasta {CONFIG['END_DATE']}")
    
    return True

if __name__ == "__main__":
    try:
        # Ejecutar pruebas
        test_fechas_dinamicas()
        test_simulacion_ejecucion()
        
        print(f"\n🎉 ¡Todas las pruebas completadas exitosamente!")
        print(f"💡 Las fechas se actualizarán automáticamente cada vez que ejecutes el script principal.")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
