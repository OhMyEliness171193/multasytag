from services.pdf_costaarauco_totext import pdf_to_text_costaarauco
from services.excel_acentral_totext import procesar_excel_autopista_central
from services.excel_stgolampa_totext import procesar_excel_autopista_stgolampa
from services.excel_rutamaipo_totext import procesar_excel_rutadelmaipo
from services.excel_adelsol_totext import procesar_excel_autopista_delsol
from services.excel_puchuncavi_totext import procesar_excel_autopista_puchuncavi
import utils.response_utils as utils

AUTOPISTA_HANDLERS = {
    "COSTA ARAUCO":pdf_to_text_costaarauco,
    "AUTOPISTA CENTRAL":procesar_excel_autopista_central,
    "SANTIAGO LAMPA":procesar_excel_autopista_stgolampa,
    "RUTA DEL MAIPO":procesar_excel_rutadelmaipo,
    "AUTOPISTA DEL SOL":procesar_excel_autopista_delsol,
    "PUCHUNCAVI":procesar_excel_autopista_puchuncavi
}

def procesa_file_to_text(data):

    file_b64 = data.get("file_b64")
    autopista=data.get("autopista")
    #nombre_campo="autopista" if not autopista else "file_b64" if not file_b64 else ""
    nombre_campo="autopista" if autopista is None else "file_b64" if file_b64 is None else ""

    if nombre_campo:
        return utils.mensaje_error_campo(nombre_campo)
    
    try:
        handler = AUTOPISTA_HANDLERS.get(autopista.upper())
        if handler:
            return handler(file_b64)
        else:
            return utils.mensaje_autopista_novalida(autopista.upper())
    
    except Exception as e:
        return utils.mensaje_excepcion_fn(str(e))
        

    
