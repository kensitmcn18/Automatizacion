"""
example_usage.py - Ejemplo de uso de la nueva arquitectura refactorizada
"""
from services.report_generator import ReportGenerator
from config import CONFIG

def example_basic_usage():
    """Ejemplo básico de uso del generador de reportes"""
    print("📋 Ejemplo básico de uso:")
    
    # Crear el generador de reportes
    generator = ReportGenerator(CONFIG)
    
    # Generar el reporte
    success = generator.generate()
    
    if success:
        print("✅ Reporte generado correctamente")
    else:
        print("❌ Error al generar reporte")

def example_custom_config():
    """Ejemplo con configuración personalizada"""
    print("\n🔧 Ejemplo con configuración personalizada:")
    
    # Configuración personalizada
    custom_config = CONFIG.copy()
    custom_config.update({
        "START_DATE": "2025-01-01T00:00:00Z",
        "END_DATE": "2025-01-31T23:59:59Z",
        "SHEET_OUTPUT_PATH": "reservas_enero_2025.xlsx",
        "LIMITATION_COUNT": 50
    })
    
    # Crear generador con configuración personalizada
    generator = ReportGenerator(custom_config)
    
    # Generar reporte
    success = generator.generate()
    
    if success:
        print("✅ Reporte personalizado generado correctamente")
    else:
        print("❌ Error al generar reporte personalizado")

if __name__ == "__main__":
    print("🏨 Ejemplos de uso - MEWS Reservation Report Generator")
    print("=" * 60)
    
    # Ejemplo básico
    example_basic_usage()
    
    # Ejemplo con configuración personalizada
    example_custom_config()
    
    print("\n📚 Para más información, consulta la documentación en el README.md")
