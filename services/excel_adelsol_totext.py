import azure.functions as func
import pandas as pd
from io import BytesIO
import logging
import json
import base64

def procesar_excel_autopista_delsol(excel_b64):
    try:
        excel_bytes=base64.b64decode(excel_b64)
        excel_file=BytesIO(excel_bytes)

        lectura_excel=pd.read_excel(excel_file,engine="openpyxl")
        lineas_excel=[]

        for index,row in lectura_excel.iterrows():
            #obj_linea={"ID":index+1}
            obj_linea={}

            for key,value in row.items():
                #obj_linea[key]=value
                if pd.notna(value):
                    if key.lower().strip()=="fecha":
                        #pd.to_datetime(df['FechaHora']).dt.strftime('%d-%m-%Y')
                        obj_linea["Fecha"]=pd.to_datetime(value,dayfirst=True).strftime('%d-%m-%Y')
                        obj_linea["Hora"]=pd.to_datetime(value,dayfirst=True).strftime('%H:%M:%S')
                    else:
                        obj_linea[key]=value
                else:
                    obj_linea[key]="Sin Valor"

            lineas_excel.append(obj_linea)
        
        return func.HttpResponse(
            json.dumps(lineas_excel,indent=4,ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )


    except Exception as e:
        logging.error(f"Ha ocurrido un error al leer archivo autopista AUTOPISTA DEL SOL: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error al leer archivo autopista AUTOPISTA DEL SOL", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )

