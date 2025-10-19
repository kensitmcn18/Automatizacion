"""
reports/google_sheet_writer.py - Writer para generar Google Sheets con formato
"""
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Dict, List, Any
import os

class GoogleSheetWriter:
    """Escribe datos en Google Sheets con formato personalizado"""
    
    def __init__(self, sheet_id: str, credentials_path: str, sheet_name: str = "Reservas Mews"):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.credentials_path = credentials_path
        self.service = None
        self._initialize_service()
        
        # Configuración de columnas (igual que SheetWriter)
        self.column_config = {
            'columnas_cortas': {
                'columns': [
                    'Numero', 'Estado', 'Recuento noches', 'Cantidad de Personas', 
                    'Recuento camas', 'Numero habitación', 'Precio', 'Importe total',
                    'Tipo tarjeta', 'Nacionalidad','RecibeCorreosMarketing'
                ],
                'factor': 1.3,
                'margin': 3,
                'min_width': 10,
                'max_width': 12
            },
            'columnas_largas': {
                'columns': [
                    'Correo', 'Direccion', 'Productos','Tipo habitación'
                ],
                'factor': 1.2,
                'margin': 5,
                'min_width': 25,
                'max_width': 28
            },
            'columnas_fechas': {
                'columns': [
                    'Fecha de creación', 'Fecha de actualización', 'Fecha llegada', 
                    'Fecha salida'
                ],
                'factor': 1.1,
                'margin': 2,
                'min_width': 18,
                'max_width': 25
            },
            'columnas_texto_medio': {
                'columns': [
                    'Grupo', 'Apellido', 'Nombre', 'Teléfono', 'tarifa', 'Numero de tarjeta',
                    'motivo de la reserva','Fecha vencimiento'
                ],
                'factor': 1.4,
                'margin': 4,
                'min_width': 13,
                'max_width': 16
            }
        }
        self.default_config = {
            'factor': 1.5,
            'margin': 5,
            'min_width': 15,
            'max_width': 40
        }
    
    def _initialize_service(self):
        """Inicializa el servicio de Google Sheets"""
        try:
            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(f"Archivo de credenciales no encontrado: {self.credentials_path}")
            
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            self.service = build('sheets', 'v4', credentials=credentials)
            print("[SUCCESS] Servicio de Google Sheets inicializado correctamente")
            
        except Exception as e:
            print(f"[ERROR] Error al inicializar Google Sheets: {e}")
            self.service = None
    
    def write_reservations(self, reservations_data: List[Dict[str, Any]], sheet_name: str = None) -> bool:
        """Escribe las reservaciones en Google Sheets con formato"""
        if not self.service:
            print("[ERROR] Servicio de Google Sheets no disponible")
            return False
        
        try:
            # Usar el nombre de sheet proporcionado o el por defecto
            target_sheet_name = sheet_name or self.sheet_name
            
            # Crear DataFrame
            df = pd.DataFrame(reservations_data)
            # Normalizar columnas (teléfono y fechas)
            df = self._normalize_dataframe(df)
            
            # Limpiar la hoja existente
            self._clear_sheet(target_sheet_name)
            
            # Escribir datos
            self._write_data_to_sheet(df, target_sheet_name)
            
            # Aplicar formato
            self._apply_formatting(target_sheet_name, df)
            
            print(f"[SUCCESS] Datos escritos exitosamente en Google Sheets: {target_sheet_name}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error al escribir en Google Sheets: {e}")
            return False
    
    def _clear_sheet(self, sheet_name: str):
        """Limpia el contenido de la hoja"""
        try:
            # Obtener el rango de la hoja
            range_name = f"{sheet_name}!A:Z"
            
            # Limpiar el rango
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
        except Exception as e:
            print(f"[WARNING] Advertencia al limpiar la hoja: {e}")
    
    def _write_data_to_sheet(self, df: pd.DataFrame, sheet_name: str):
        """Escribe los datos en la hoja"""
        try:
            # Convertir DataFrame a lista de listas
            data = [df.columns.tolist()] + df.values.tolist()
            
            # Escribir datos
            range_name = f"{sheet_name}!A1"
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body={'values': data}
            ).execute()
            
        except Exception as e:
            print(f"[ERROR] Error al escribir datos: {e}")
            raise
    
    def _apply_formatting(self, sheet_name: str, df: pd.DataFrame):
        """Aplica formato a la hoja de Google Sheets"""
        try:
            # Obtener el ID de la hoja
            sheet_id = self._get_sheet_id(sheet_name)
            if sheet_id is None:
                print(f"[WARNING] No se pudo encontrar la hoja: {sheet_name}")
                return
            
            # Aplicar formato de encabezados
            self._format_headers(sheet_id, len(df.columns))
            
            # Ajustar anchos de columna
            self._adjust_column_widths(sheet_id, df)
            
            # Aplicar formato de fuente
            self._apply_font_formatting(sheet_id, len(df) + 1)

            # Aplicar formato de número/fecha por columna
            self._apply_number_and_date_formats(sheet_id, df)
            
        except Exception as e:
            print(f"[ERROR] Error al aplicar formato: {e}")
    
    def _get_sheet_id(self, sheet_name: str) -> int:
        """Obtiene el ID de la hoja por nombre"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.sheet_id
            ).execute()
            
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            
            return None
            
        except Exception as e:
            print(f"[ERROR] Error al obtener ID de la hoja: {e}")
            return None
    
    def _format_headers(self, sheet_id: int, num_columns: int):
        """Aplica formato a los encabezados"""
        try:
            requests = [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": num_columns
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {
                                    "bold": True,
                                    "fontSize": 10,
                                    "fontFamily": "Calibri"
                                },
                                "horizontalAlignment": "LEFT"
                            }
                        },
                        "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
                    }
                }
            ]
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body={'requests': requests}
            ).execute()
            
        except Exception as e:
            print(f"[ERROR] Error al formatear encabezados: {e}")
    
    def _adjust_column_widths(self, sheet_id: int, df: pd.DataFrame):
        """Ajusta los anchos de las columnas"""
        try:
            requests = []
            
            for i, column_name in enumerate(df.columns):
                config = self._get_column_config(column_name)
                max_length = len(str(column_name))
                
                # Calcular longitud máxima del contenido
                for value in df[column_name]:
                    if value is not None:
                        max_length = max(max_length, len(str(value)))
                
                # Calcular ancho ajustado
                adjusted_width = self._calculate_column_width(max_length, config)
                
                requests.append({
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "COLUMNS",
                            "startIndex": i,
                            "endIndex": i + 1
                        },
                        "properties": {
                            "pixelSize": int(adjusted_width * 7)  # Convertir a píxeles
                        },
                        "fields": "pixelSize"
                    }
                })
            
            if requests:
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.sheet_id,
                    body={'requests': requests}
                ).execute()
                
        except Exception as e:
            print(f"[ERROR] Error al ajustar anchos de columna: {e}")
    
    def _apply_font_formatting(self, sheet_id: int, num_rows: int):
        """Aplica formato de fuente a todas las celdas"""
        try:
            requests = [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": num_rows
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {
                                    "fontSize": 10,
                                    "fontFamily": "Calibri"
                                }
                            }
                        },
                        "fields": "userEnteredFormat.textFormat"
                    }
                }
            ]
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body={'requests': requests}
            ).execute()
            
        except Exception as e:
            print(f"[ERROR] Error al aplicar formato de fuente: {e}")
    
    def _get_column_config(self, column_name: str) -> Dict[str, Any]:
        """Obtiene la configuración para una columna específica"""
        for category, config in self.column_config.items():
            if column_name in config['columns']:
                return config
        return self.default_config
    
    def _calculate_column_width(self, max_length: int, config: Dict[str, Any]) -> float:
        """Calcula el ancho de columna basado en la configuración"""
        calculated_width = max_length * config['factor'] + config['margin']
        return max(min(calculated_width, config['max_width']), config['min_width'])
    
    def get_sheet_url(self) -> str:
        """Retorna la URL de la Google Sheet"""
        return f"https://docs.google.com/spreadsheets/d/{self.sheet_id}"

    def _normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza columnas específicas: teléfono sin '+' y fechas como texto ISO."""
        df_copy = df.copy()
        # Normalizar teléfono: quitar '+' y cualquier carácter no numérico y dejar como número entero
        phone_columns = [col for col in df_copy.columns if col.lower() in ["teléfono", "telefono", "tel"]]
        for col in phone_columns:
            try:
                df_copy[col] = (
                    df_copy[col]
                    .astype(str)
                    .str.replace("+", "", regex=False)
                    .str.replace(r"[^0-9]", "", regex=True)
                )
                # Convertir a número sin decimales (entero); celdas vacías quedan vacías
                df_copy[col] = df_copy[col].apply(lambda x: int(x) if x.isdigit() else "")
            except Exception:
                pass

        # Normalizar fechas: mantener formato yyyy-MM-dd HH:mm:ss como texto para USER_ENTERED
        date_like_cols = [
            col for col in df_copy.columns
            if col.lower().startswith("fecha") or col.lower() in ["fecha llegada", "fecha salida", "fecha de creación", "fecha de actualización", "fecha vencimiento"]
        ]
        for col in date_like_cols:
            try:
                # Intentar parsear a datetime y luego formatear
                series = pd.to_datetime(df_copy[col], errors='coerce')
                df_copy[col] = series.dt.strftime('%Y-%m-%d %H:%M:%S')
                # Donde no se pudo parsear, mantener valor original
                mask_na = series.isna()
                if mask_na.any():
                    df_copy.loc[mask_na, col] = df.loc[mask_na, col]
            except Exception:
                pass

        return df_copy

    def _apply_number_and_date_formats(self, sheet_id: int, df: pd.DataFrame):
        """Aplica formato numérico a teléfonos y formato de fecha a columnas de fecha."""
        try:
            requests = []

            # Formato de encabezado ya aplica Calibri 10 en _format_headers y _apply_font_formatting

            # Detectar columnas
            phone_indexes = [i for i, c in enumerate(df.columns) if c.lower() in ["teléfono", "telefono", "tel"]]
            date_indexes = [
                i for i, c in enumerate(df.columns)
                if c.lower().startswith("fecha") or c.lower() in ["fecha llegada", "fecha salida", "fecha de creación", "fecha de actualización", "fecha vencimiento"]
            ]

            # Aplicar formato a teléfonos: número entero sin decimales
            for idx in phone_indexes:
                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 1,  # Excluir encabezado
                            "startColumnIndex": idx,
                            "endColumnIndex": idx + 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": {
                                    "type": "NUMBER",
                                    "pattern": "0"
                                },
                                "textFormat": {
                                    "fontSize": 10,
                                    "fontFamily": "Calibri"
                                }
                            }
                        },
                        "fields": "userEnteredFormat(numberFormat,textFormat)"
                    }
                })

            # Aplicar formato a fechas: yyyy-MM-dd HH:mm:ss
            for idx in date_indexes:
                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 1,
                            "startColumnIndex": idx,
                            "endColumnIndex": idx + 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": {
                                    "type": "DATE_TIME",
                                    "pattern": "yyyy-MM-dd HH:mm:ss"
                                },
                                "textFormat": {
                                    "fontSize": 10,
                                    "fontFamily": "Calibri"
                                }
                            }
                        },
                        "fields": "userEnteredFormat(numberFormat,textFormat)"
                    }
                })

            if requests:
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.sheet_id,
                    body={'requests': requests}
                ).execute()
        except Exception as e:
            print(f"[ERROR] Error al aplicar formatos de número/fecha: {e}")


