import azure.functions as func
import base64
import pandas as pd
from io import BytesIO
import logging
import json

def dividir_excel_base64(excel_b64,nombre_hoja,tamaño_fragmento=30000):
    try:
        # Decodificar el archivo Excel en base64
        excel_bytes = base64.b64decode(excel_b64)
        excel_file = BytesIO(excel_bytes)

        contenido_excel = pd.read_excel(excel_file,sheet_name=nombre_hoja, engine='openpyxl')
        partes_excel = [contenido_excel[i: i+tamaño_fragmento] for i in range(0,len(contenido_excel),tamaño_fragmento)]

        fragmentos_b64 = []
        for index, fragmento in enumerate(partes_excel):
            
            # Guardar cada fragmento como un archivo Excel
            fragmento_excel = BytesIO()
            fragmento.to_excel(fragmento_excel, index=False, engine='openpyxl')
            fragmento_excel.seek(0)

            fragmento_b64 = base64.b64encode(fragmento_excel.getvalue()).decode('utf-8')
            fragmentos_b64.append({
                "fragmento_id": index+1,
                "contenido_base64": fragmento_b64
            })

        #return fragmentos_b64
        return func.HttpResponse(
            json.dumps(fragmentos_b64,indent=4),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f"Ha ocurrido un error al fragmentar el excel: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error al fragmentar el excel", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
    

