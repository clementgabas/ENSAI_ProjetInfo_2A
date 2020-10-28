
def colprint(color, text):
    """
    Alternative colorée et plaisante à la fonction native print. La fonction colprint prend en compte la langue anglais et française.

    Parameters
    ----------
    color :  str
        La couleur dans laquelle on souhaite print notre texte.
    text :   str
        Le texte à print en couleur via colprint.

    Liste des couleurs codées
    --------------------------
    - Bleu / Blue
    - Rouge / Red
    - Vert / Green
    - Jaune / Yellow
    - Violet / Purple


    Returns
    -------
    Si la couleur est programmée, renvoit le texte dans la couleur choisie (plus présisement, le texte est print en blanc sur un fond de la couleur choisie). Si la couleur n'existe pas, un message apparrait pour le signaler et le texte est print comme avec un print classique.'

    """
    color = color.lower()

    if color in ("blue", "bleu"):
        return(print('\33[44m' + text + '\x1b[0m'))

    elif color in ("red", "rouge"):
        return(print('\33[41m' + text + '\x1b[0m'))

    elif color in ("green", "vert"):
        return(print('\33[42m' + text + '\x1b[0m'))

    elif color in ('jaune', 'yellow'):
        return(print('\33[43m' + text + '\x1b[0m'))

    elif color in ('violet', 'purple') :
        return print('\33[45m' + text + '\x1b[0m')

    else :
        colprint('red', "La couleur choisie n'existe pas. Veuillez choisir une autre couleur.")
        return(print(text))

def timePrint(text):
    from datetime import datetime
    return print(f"{str(datetime.now())}]: "+ text)