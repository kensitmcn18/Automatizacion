# Guía de Migración - Refactorización de sheets_client.py

## Resumen de Cambios

Se ha refactorizado completamente el archivo `sheets_client.py` siguiendo una arquitectura modular y mantenible. Los cambios principales incluyen:

### 🏗️ Nueva Arquitectura

```
Automatizacion/
├── config.py                    # ✅ Configuración centralizada
├── main.py                      # ✅ Punto de entrada principal
├── services/
│   └── report_generator.py      # ✅ Orquestador principal
├── integrations/
│   └── mews/
│       ├── client.py            # ✅ Cliente HTTP
│       └── endpoints.py         # ✅ Endpoints de API
├── data/
│   ├── cleaners.py              # ✅ Limpieza de datos
│   └── transformers.py          # ✅ Transformación de datos
├── reports/
│   └── sheet_writer.py          # ✅ Generación de Excel
└── util/
    └── utils.py                 # ✅ Utilidades comunes
```

### 🔄 Cambios Principales

#### 1. **Configuración Centralizada** (`config.py`)
- **Antes**: Tokens y URLs hardcodeados en `sheets_client.py`
- **Después**: Configuración centralizada con variables de entorno

```python
# Antes
CLIENTOKEN = "E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D"
ACCESSTOKEN = "C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D"

# Después
CONFIG = {
    "CLIENT_TOKEN": os.getenv("MEWS_CLIENT_TOKEN", "default_value"),
    "ACCESS_TOKEN": os.getenv("MEWS_ACCESS_TOKEN", "default_value"),
    # ... más configuración
}
```

#### 2. **Separación de Responsabilidades**

**Antes**: Un solo archivo con 531 líneas
**Después**: Módulos especializados

- **`integrations/mews/client.py`**: Cliente HTTP reutilizable
- **`integrations/mews/endpoints.py`**: Lógica específica de cada endpoint
- **`data/cleaners.py`**: Validación y limpieza de datos
- **`data/transformers.py`**: Transformación de datos al formato del reporte
- **`reports/sheet_writer.py`**: Generación de archivos Excel
- **`services/report_generator.py`**: Orquestación del proceso

#### 3. **Manejo de Errores Mejorado**

```python
# Antes: Manejo básico de errores
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error {response.status_code}")

# Después: Manejo robusto con reintentos
def safe_post_with_retry(url, payload, headers, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Manejo de rate limiting
                time.sleep(retry_after)
        except Exception as e:
            print(f"Error de conexión: {e}")
    return {}
```

#### 4. **Tipado Estático**

```python
# Antes: Sin tipado
def get_customer_names(account_ids):
    # código...

# Después: Con tipado estático
def get_customer_names(client, account_ids: Set[str]) -> Dict[str, Dict]:
    # código...
```

### 🚀 Cómo Usar la Nueva Arquitectura

#### Uso Básico

```python
from services.report_generator import ReportGenerator
from config import CONFIG

# Crear generador
generator = ReportGenerator(CONFIG)

# Generar reporte
success = generator.generate()
```

#### Configuración Personalizada

```python
custom_config = CONFIG.copy()
custom_config.update({
    "START_DATE": "2025-01-01T00:00:00Z",
    "END_DATE": "2025-01-31T23:59:59Z",
    "SHEET_OUTPUT_PATH": "mi_reporte.xlsx"
})

generator = ReportGenerator(custom_config)
generator.generate()
```

### 📋 Beneficios de la Refactorización

1. **Mantenibilidad**: Código modular y fácil de mantener
2. **Testabilidad**: Cada componente puede ser probado independientemente
3. **Reutilización**: Componentes reutilizables en otros proyectos
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Legibilidad**: Código más limpio y organizado
6. **Robustez**: Mejor manejo de errores y rate limiting

### 🔧 Migración Gradual

Si necesitas migrar gradualmente:

1. **Fase 1**: Usar la nueva configuración (`config.py`)
2. **Fase 2**: Migrar endpoints uno por uno
3. **Fase 3**: Implementar limpiadores y transformadores
4. **Fase 4**: Usar el nuevo generador de reportes

### 📝 Notas Importantes

- El archivo `sheets_client.py` original se mantiene como referencia
- Todos los endpoints originales están implementados en `integrations/mews/endpoints.py`
- La funcionalidad es idéntica, pero con mejor estructura
- Se mantiene compatibilidad con la configuración existente

### 🐛 Solución de Problemas

Si encuentras problemas durante la migración:

1. Verifica que todas las dependencias estén instaladas
2. Confirma que las variables de entorno estén configuradas
3. Revisa los logs de error para identificar problemas específicos
4. Usa el archivo `example_usage.py` como referencia

### 📞 Soporte

Para preguntas sobre la migración, consulta:
- `example_usage.py` - Ejemplos de uso
- `main.py` - Implementación básica
- Documentación en cada módulo
