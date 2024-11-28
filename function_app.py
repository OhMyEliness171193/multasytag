import azure.functions as func
from services.fragmentar_excel import dividir_excel_base64
import utils.response_utils as utils
from handlers.file_to_text_handler import procesa_file_to_text



#V 1.12
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="file_to_text_service")
@app.route(route="file_to_text_service")

def file_to_text_service(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        data = req.get_json()
        response=procesa_file_to_text(data)

        return response

    except Exception as e:
        return utils.mensaje_excepcion_fn(e)
    



    
    
@app.route(route="excel_fragment_service")

def excel_fragment_service(req: func.HttpRequest) -> func.HttpResponse:
    
    data=req.get_json()

    excel_b64=data.get("excel_b64")
    hoja=data.get("nombre_hoja")
    nombre_campo="excel_b64" if not excel_b64 else "nombre_hoja" if not hoja else ""

    if nombre_campo:
        return utils.mensaje_error_campo(nombre_campo)
    else:
        try:
            fragmentos_excel_b64=dividir_excel_base64(excel_b64,hoja)
            return fragmentos_excel_b64
        except Exception as ex:
            return utils.mensaje_excepcion_fn(ex)




