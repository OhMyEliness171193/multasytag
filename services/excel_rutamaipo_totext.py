import azure.functions as func
from io import BytesIO
import base64
import json
import logging
import pandas as pd

def procesar_excel_rutadelmaipo(excelb64):
    try:
        excel_bytes = base64.b64decode(excelb64)
        excel_file = BytesIO(excel_bytes)

        # Leer el archivo completo inicialmente sin saltar filas
        temp_df = pd.read_excel(excel_file, engine="openpyxl", sheet_name=0, header=None)

        skip_rows = 0
        for idx, row in temp_df.iterrows():
            if row.str.lower().str.contains("patente", na=False).any():
                skip_rows = idx
                break

        excel_file.seek(0)

        df = pd.read_excel(excel_file, engine="openpyxl", sheet_name=0, header=skip_rows)

        # Limpiar los nombres de las columnas para evitar problemas de formato
        #df.columns = df.columns.str.strip()

        # Seleccionar solo las columnas necesarias
        #df = df[['Patente', 'Categoria', 'FechaHora', 'Hora', 'Plaza', 'Importe']]
        column_indices = [1, 2, 4, 5, 6, 11]  
        column_names = ['Patente', 'Categoria', 'FechaHora', 'Hora', 'Plaza', 'Importe']
        df = df.iloc[:, column_indices]
        df.columns = column_names

        # Convertir las columnas FechaHora y Hora al formato deseado
        df['FechaHora'] = pd.to_datetime(df['FechaHora']).dt.strftime('%d-%m-%Y')
        df['Hora'] = pd.to_datetime(df['Hora']).dt.strftime('%H:%M:%S')

        #df.insert(0, 'ID', range(1, len(df) + 1))

        # Asegurarse de que todos los datos sean serializables en JSON
        df = df.map(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)

        lineas_excel = df.to_dict(orient='records')
        
        return func.HttpResponse(
            json.dumps(lineas_excel,indent=4,ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )


    except Exception as e:
        logging.error(f"Ha ocurrido un error al leer archivo autopista RUTA DEL MAIPO: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error al leer archivo autopista RUTA DEL MAIPO", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )

