# En main.py se va a realizar la ejecución principal del proyecto
from services.report_generator import ReportGenerator
from config import CONFIG

if __name__ == "__main__":
    generator = ReportGenerator(CONFIG)
    generator.generate()
