def delete_pseudo_scores(pseudo):
    """
        Procédure qui supprime tous les éléments de la table Scores à un pseudo associé.

        :parameter
        ----------
        pseudo : str
            pseudo de l'utilisateur dont on veut supprimer les scores.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.
    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("DELETE FROM Scores WHERE pseudo = ?", (pseudo,))
        con.commit()
    except:
        print("erreur dans delete_pseudo_scores")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()