"""
test_refactored_code.py - Prueba básica de la arquitectura refactorizada
"""
import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todos los módulos se pueden importar correctamente"""
    try:
        print("🧪 Probando importaciones...")
        
        # Probar importaciones principales
        from config import CONFIG
        print("✅ config.py importado correctamente")
        
        from services.report_generator import ReportGenerator
        print("✅ ReportGenerator importado correctamente")
        
        from integrations.mews.client import MewsClient
        print("✅ MewsClient importado correctamente")
        
        from integrations.mews import endpoints
        print("✅ endpoints importado correctamente")
        
        from data.cleaners import DataCleaner
        print("✅ DataCleaner importado correctamente")
        
        from data.transformers import ReservationTransformer
        print("✅ ReservationTransformer importado correctamente")
        
        from reports.sheet_writer import SheetWriter
        print("✅ SheetWriter importado correctamente")
        
        from util.utils import safe_post, translate_country, calculate_nights
        print("✅ utils importado correctamente")
        
        print("\n🎉 Todas las importaciones funcionan correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_configuration():
    """Prueba que la configuración se carga correctamente"""
    try:
        print("\n🔧 Probando configuración...")
        
        from config import CONFIG
        
        required_keys = [
            "API_BASE_URL", "CLIENT_TOKEN", "ACCESS_TOKEN", 
            "START_DATE", "END_DATE", "SHEET_OUTPUT_PATH"
        ]
        
        for key in required_keys:
            if key not in CONFIG:
                print(f"❌ Falta clave de configuración: {key}")
                return False
        
        print("✅ Configuración cargada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_client_creation():
    """Prueba la creación del cliente Mews"""
    try:
        print("\n🌐 Probando creación de cliente...")
        
        from config import CONFIG
        from integrations.mews.client import MewsClient
        
        client = MewsClient(
            api_base_url=CONFIG["API_BASE_URL"],
            client_token=CONFIG["CLIENT_TOKEN"],
            access_token=CONFIG["ACCESS_TOKEN"]
        )
        
        print("✅ Cliente Mews creado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando cliente: {e}")
        return False

def test_report_generator_creation():
    """Prueba la creación del generador de reportes"""
    try:
        print("\n📊 Probando creación de generador de reportes...")
        
        from config import CONFIG
        from services.report_generator import ReportGenerator
        
        generator = ReportGenerator(CONFIG)
        
        print("✅ Generador de reportes creado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando generador: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Iniciando pruebas de la arquitectura refactorizada")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_configuration,
        test_client_creation,
        test_report_generator_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La refactorización está lista.")
        return 0
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    exit(main())
