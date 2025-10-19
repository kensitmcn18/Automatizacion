"""
test_google_sheets.py - Script de prueba para Google Sheets
"""
import os
import sys
from config import CONFIG
from services.report_generator import ReportGenerator

def test_google_sheets_integration():
    """Prueba la integración con Google Sheets"""
    print("🧪 Iniciando prueba de integración con Google Sheets...")
    
    # Verificar configuraciones
    print("\n📋 Verificando configuraciones...")
    
    required_configs = [
        "GOOGLE_SHEET_ID",
        "GOOGLE_CREDENTIALS_PATH", 
        "GOOGLE_SHEET_NAME"
    ]
    
    missing_configs = []
    for config_key in required_configs:
        if not CONFIG.get(config_key):
            missing_configs.append(config_key)
    
    if missing_configs:
        print(f"❌ Configuraciones faltantes: {', '.join(missing_configs)}")
        print("   Por favor, configura estas variables en tu archivo .env")
        return False
    
    # Verificar archivo de credenciales
    credentials_path = CONFIG["GOOGLE_CREDENTIALS_PATH"]
    if not os.path.exists(credentials_path):
        print(f"❌ Archivo de credenciales no encontrado: {credentials_path}")
        print("   Por favor, crea el archivo credentials.json con las credenciales de Google")
        return False
    
    print("✅ Configuraciones verificadas correctamente")
    
    # Probar inicialización del ReportGenerator
    print("\n🔧 Probando inicialización del ReportGenerator...")
    try:
        generator = ReportGenerator(CONFIG)
        print("✅ ReportGenerator inicializado correctamente")
        
        # Verificar tipo de writer
        if hasattr(generator.writer, 'get_sheet_url'):
            print("✅ GoogleSheetWriter configurado correctamente")
            print(f"   URL de la hoja: {generator.writer.get_sheet_url()}")
        else:
            print("⚠️ SheetWriter configurado (modo Excel)")
            
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar ReportGenerator: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🚀 Prueba de Integración Google Sheets")
    print("=" * 50)
    
    success = test_google_sheets_integration()
    
    if success:
        print("\n✅ ¡Prueba completada exitosamente!")
        print("\n📝 Próximos pasos:")
        print("1. Configura las variables en tu archivo .env")
        print("2. Crea el archivo credentials.json con las credenciales")
        print("3. Comparte tu Google Sheet con el email del service account")
        print("4. Ejecuta el reporte con: python main.py")
    else:
        print("\n❌ Prueba fallida. Revisa las configuraciones.")
        sys.exit(1)

if __name__ == "__main__":
    main()
