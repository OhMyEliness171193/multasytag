import azure.functions as func
import pandas as pd
import base64
import logging
import json
from io import BytesIO
import math

def procesar_excel_autopista_stgolampa(excel_b64):

    try:

        excel_bytes=base64.b64decode(excel_b64)
        excel_file=BytesIO(excel_bytes)

        lectura_excel=pd.read_excel(excel_file,sheet_name="Detalle sin filtro",engine="openpyxl")
        lineas_excel=[]

        for index,row in lectura_excel.iterrows():
            obj_linea={}
            
            for key,value in row.items():
                
                if key.lower()=="fecha" or key.lower()=="hora":

                    if pd.notna(value) and hasattr(value,'isoformat'):
                        obj_linea[key] = value.isoformat()

                elif pd.notna(value) and not (isinstance(value,float) and math.isnan(value)):
                    obj_linea[key]=value
                

            if obj_linea and "total" not in str(obj_linea).lower():
                lineas_excel.append(obj_linea)

        return func.HttpResponse(
            json.dumps(lineas_excel,indent=4,ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
    

    except Exception as e:
        logging.error(f"Ha ocurrido un error al leer archivo autopista STGO-LAMPA: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error al leer archivo autopista STGO-LAMPA", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
    
"""file_path = Path("C:/Users/E/Downloads/stgolampa_test.txt")
try:
    excel_test = file_path.read_text(encoding='utf-8')
    procesar_excel_autopista_stgolampa(excel_test)

except FileNotFoundError:
    print(f"El archivo no se encontró en la ruta: {file_path}")"""
