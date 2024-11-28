import azure.functions as func
import logging
import pandas as pd
import json
import base64
from io import BytesIO


def procesar_excel_autopista_central(excel_b64):
    try:
        # Decodificar archivo Excel en base64
        excel_bytes = base64.b64decode(excel_b64)
        excel_file = BytesIO(excel_bytes)

        # Leer el archivo Excel desde el objeto BytesIO -> Quité: sheet_name='Hoja1',
        df = pd.read_excel(excel_file, engine='openpyxl')
        lineas_excel = []
        id_linea=1

        for index, row in df.iterrows():

            obj_linea = {"ID": id_linea}
            id_linea+=1

            for key, value in row.items():
                if "patente" in key.lower():
                    key = "Patente"
                elif "fecha de" in key.lower():
                    key = "Fecha_Creacion"
                elif "tiempo de" in key.lower():
                    key = "Hora_Creacion"
                elif "id p" in key.lower():
                    key = "Portico"
                elif "importe" in key.lower():
                    key = "Importe"

                if isinstance(value, pd.Timestamp) or hasattr(value, 'isoformat'):
                    obj_linea[key] = value.isoformat()
                else:
                    if key!="Importe":
                        obj_linea[key] = str(value)
                    else:
                        obj_linea[key]=f"{value:.2f}"
            
            lineas_excel.append(obj_linea)

        return func.HttpResponse(
            json.dumps(lineas_excel,indent=4),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Ha ocurrido un error inesperado: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error inesperado", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )