"""
test_simple.py - Prueba simple de importaciones
"""
import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Prueba las importaciones básicas"""
    try:
        print("🧪 Probando importaciones básicas...")
        
        # Probar configuración
        from config import CONFIG
        print("✅ config.py importado correctamente")
        
        # Probar cliente Mews
        from integrations.mews.client import MewsClient
        print("✅ MewsClient importado correctamente")
        
        # Probar utilidades
        from util.utils import safe_post
        print("✅ safe_post importado correctamente")
        
        print("🎉 Todas las importaciones básicas funcionan!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Prueba simple de importaciones")
    print("=" * 40)
    
    if test_basic_imports():
        print("\n✅ ¡Prueba exitosa! El error de importación está solucionado.")
    else:
        print("\n❌ Aún hay problemas de importación.")
