from flask import jsonify

from requests import codes as http_codes

def make_reponse(p_object=None, status_code=http_codes.OK):
    """
    Fonction qui permet de formater toutes les sorties api au même format

    :parameter
    ----------
    p_object : dict
        Dictionaire contenant le code http de la reponse, et un message personnalisé et potentiellement d'autres informations nécessaires.
    status_code : int
        Code http corespondant à la réponse de la requête.


    :return
    -------
    json_response : json
        Renvoie le que doit renvoyer l'API
    """
    if p_object is None and status_code == http_codes.NOT_FOUND:
        p_object = {
            "status": {
                "status_content": [
                    {"code": "404 - Not Found", "message": "Resource not found"}
                ]
            }
        }
    json_response = jsonify(p_object)
    json_response.status_code = status_code
    json_response.content_type = "application/json;charset=utf-8"
    json_response.headers["Cache-Control"] = "max-age=3600"
    return json_response



