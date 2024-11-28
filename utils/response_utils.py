import azure.functions as func
import logging

def mensaje_error_campo(campo) -> func.HttpResponse:

    logging.error(f'ERROR: El campo \'{campo}\' es obligatorio')

    return func.HttpResponse(
        f'{{"error":"El campo \'{campo}\' es obligatorio"}}',
        status_code=400,
        mimetype="application/json"
    )


def mensaje_excepcion_fn(excepcion) -> func.HttpResponse:

    logging.error(f"Error al procesar la solicitud: {str(excepcion)}")
    
    return func.HttpResponse(
        f'{{"error": "Error al procesar la solicitud: {str(excepcion)}"}}',
        status_code=500,
        mimetype="application/json"
    )


def mensaje_autopista_novalida(autopista) -> func.HttpResponse:

    logging.error(f"Error al procesar la autpista: '{autopista}' NO EXISTE.")
    
    return func.HttpResponse(
        f'{{"error": "Error al procesar la autopista: \'{autopista}\' NO EXISTE."}}',
        status_code=404,
        mimetype="application/json"
    )

#print(mensaje_error_campo("autopista").get_body().decode('utf-8'))