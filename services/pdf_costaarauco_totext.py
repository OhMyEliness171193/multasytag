import azure.functions as func
import PyPDF2
import re
import base64
import json
from io import BytesIO

#aplicar try-except: PENDIENTE
def pdf_to_text_costaarauco(pdf_base64):

    try:
        # Decodificar el archivo Base64 en bytes
        pdf_bytes = base64.b64decode(pdf_base64)
        archivo_pdf = BytesIO(pdf_bytes)

        # Procesar el PDF para extraer las patentes y las líneas
        patentes_y_lineas = []
        patente_pattern = r'DETALLE DE TRANSACCIÓN PATENTE: (\b[A-Z]{2,}\d{2,}\b)'
        linea_cobro_pattern = r'^\d+\s+\d{2}/\d{2}/\d{4}.*$'
        total_patente_pattern = r'^TOTAL PATENTE : (\b[A-Z]{2,}\d{2,}\b)'

        lector_pdf = PyPDF2.PdfReader(archivo_pdf)
        patente_actual = None
        lineas_cobro_actuales = []

        for pagina in lector_pdf.pages:
            text = pagina.extract_text()
            if text:
                lineas = text.splitlines()
                for linea in lineas:
                    match_patente = re.search(patente_pattern, linea)
                    if match_patente:
                        if patente_actual and lineas_cobro_actuales:
                            patentes_y_lineas.append({
                                "patente": patente_actual,
                                "lineas_cobro": lineas_cobro_actuales
                            })

                        patente_actual = match_patente.group(1)
                        lineas_cobro_actuales = []

                    elif patente_actual and re.match(linea_cobro_pattern, linea):
                        lineas_cobro_actuales.append(linea)

                    match_total = re.search(total_patente_pattern, linea)
                    if match_total and match_total.group(1) == patente_actual:
                        lineas_cobro_actuales.append(linea)

        if patente_actual and lineas_cobro_actuales:
            patentes_y_lineas.append({
                "patente": patente_actual,
                "lineas_cobro": lineas_cobro_actuales
            })

        # Convertir el resultado a JSON usando el módulo json
        return func.HttpResponse(
            json.dumps(patentes_y_lineas,indent=4,ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": "Ha ocurrido un error al procesar el pdf autopista costa arauco", "detalle": str(e)}),
            status_code=400,
            mimetype="application/json"
        )