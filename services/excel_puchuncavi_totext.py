import azure.functions as func
from io import BytesIO
import pandas as pd
import logging
import json
import base64



def procesar_excel_autopista_puchuncavi(excel_b64):

    try:
        excel_bytes=base64.b64decode(excel_b64)
        excel_file=BytesIO(excel_bytes)

        lectura_excel=pd.read_excel(excel_file,engine="openpyxl")
        lineas_excel=[]

        for index,row in lectura_excel.iterrows():
            
            lineas_excel.append(procesar_fila_excel(index,row))

        return func.HttpResponse(
            json.dumps(lineas_excel,indent=4,ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
             
    except Exception as e:
        logging.error(f"Ha ocurrido un error al leer archivo autopista AUTOPISTA PUCHUNCAVI: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error al leer archivo autopista AUTOPISTA PUCHUNCAVI", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
    

def procesar_fila_excel(index,row) -> dict:
    
    #obj_linea={"ID":index+1}
    #obj_linea={}
    obj_linea={"autopista":"PUCHUNCAVI"}

    for key,value in row.items():
        if pd.notna(value):

            key_lower = key.lower().strip()

            if "portico" in key_lower or "pórtico" in key_lower:
                obj_linea["portico"]=value.strip()
            elif "patente" in key_lower:
                obj_linea["patente"]=value.upper().strip()
            elif "fecha" in key_lower and "desde" not in key_lower and "hasta" not in key_lower:
                #Agregar hora en fecha_ts
                obj_linea["fecha"]=pd.to_datetime(value,dayfirst=True).strftime('%d-%m-%Y')
                obj_linea["fecha_ts"]=pd.to_datetime(value,dayfirst=False).strftime('%Y-%m-%dT%H:%M:%SZ')
            elif "hora" in key_lower:
                obj_linea["hora"]=value.strftime('%H:%M:%S')
            elif "importe" in key_lower:
                obj_linea["importe"]=value
            else:
                pass
        else:
            logging.warning(f"Columna '{key}' tiene un valor NO VÁLIDO en la fila {index+1}.")
            obj_linea[key]="Sin Valor"

    return obj_linea







"""file_path = Path("C:/Users/E/Downloads/puchuncavi.txt")
try:
    excel_test = file_path.read_text(encoding='utf-8')
    procesar_excel_autopista_puchuncavi(excel_test)

except FileNotFoundError:
    print(f"El archivo no se encontró en la ruta: {file_path}")
except Exception as e:
    logging.error(f"Error inesperado al leer el archivo: {str(e)}")"""