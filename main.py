# En main.py se va a realizar la ejecución principal del proyecto
from services.report_generator import ReportGenerator
from config import CONFIG

def main():
    """Función principal del programa"""
    try:
        print("MEWS Reservation Report Generator")
        print("=" * 50)
        
        generator = ReportGenerator(CONFIG)
        success = generator.generate()
        
        if success:
            print("\n[SUCCESS] Proceso completado exitosamente!")
        else:
            print("\n[ERROR] El proceso no se completó correctamente")
            return 1
            
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
