# APIjeux -- Descriptif rapide l'application
- ## Qu'est-ce qu'APIjeux, description du projet
    APIjeux est le nom que nous avons choisi de donner à notre projet informatique du 1er semestre de 2ème année à l'ENSAI. L'objectif du projet est le développement d'une **RESTful API permettant de jouer, via une application cliente, à des jeux de plateau en ligne**.
    L'un des principaux objectifs est que l'**application soit suffisament flexible pour supporter des jeux suffisamment variés sans trop de changements au niveau son code**.
- ## Notre réalisation du projet
    Pour réaliser notre projet informatique, nous avons choisi de développer deux jeux, à savoir le **Puissance4** et le **jeu de l'Oie**. En effet, nous avons estimé que ces deux jeux étaient suffisamment différents l'un de l'autre pour prouver la fléxibiliter de notre application.
    Ainsi, dans toute la suite, APIjeux désigne l'ensemble des applications client et serveur.
    En plus des fonctionnalités demandées (pourvoir jouer à des jeux), nous avons réalisé toute une partie **gestion de compte**, avec notamment la gestion d'amis, de scores et de classements.
De plus, nous avons intégré la possibilité de jouer avec des amis ou contre des inconnus. Jouer avec des amis se fait, comme pour la plupart des jeux en ligne, en rejoignant une salle dont notre ami nous à transférer le code.
# Classes testées et commentées 
blabla

# Comment installer APIjeux
- ## Télécharger le code :
    Pour récupérer le code du serveur APIjeux et le code du Client APIjeux, le plus simple est de clonner le [dépot github](https://github.com/clementgabas/Projet-Info) comme si dessous :
    ```sh
    $ git clone https://github.com/clementgabas/Projet-Info
    ```
    Vous téléchargerez alors un dossier nommé **Projet-Info** contenant deux sous-dossiers :
    - AppClient : dossier contenant le code de l'application cliente
    - AppServeur : dossier contenant le code de l'application serveur API
 
 - ## Packages python nécessaires :
   
    Les packages nécessaires au bon fonctionnement de chaque application (client et serveur) sont précisées dans les fichiers **AppClient/requirements.txt** et **AppServeur/requirements.txt**

    Ici, nous listons ci-dessous l'ensemble des packages python nécessaires pour les deux application confondues et expliquons en quelques lignes leur intérêt.
    > Application Cliente : 
    > colorama == 0.4.4 --> pour l'affichage des couleurs (pour les jetons) en ascii
    > tabulate == 0.8.7 --> pour l'affichage de tableaux propres et simples à construire
    > requests == 2.24.0 --> pour communiquer avec le serveur API
    > PyInquirer == 1.0.3 --> pour pouvoir se déplacer dans les menus avec les flèches directionnelles

    > Applcation Serveur API :
    > Flask == 1.1.2
    > flask_restplus == 0.13.0
    > Flask_Cors == 3.0.9
    > Flask_Caching == 1.9.0
    > loguru == 0.5.3
    > requests == 2.24.0
    > PyYAML == 5.3.1

    Tous ces packages servent au bon fonctionnement du serveur API.

# Comment démarrer APIjeux pour pouvoir jouer
- ## Démarrer et paramétrer le serveur API : 
    Pour fonctionner, APIjeux requiert que l'API soit opérationnelle, c'est-à-dire que le serveur API tourne. Evidemment, nous faisons tourner ce serveur API en local (localhost, l'adresse et le port sont modifiables dans le fichier AppServeur/api.py).
    ```sh
    if __name__ == "__main__":
        DAOuser.put_all_users_disconnected()
        cf_port = conf["port"]
        if cf_port is None:
            #adresse et port modifiables ici
            app.run(host="localhost", port=5001, debug=True) 
        else:
            app.run(host="localhost", port=int(cf_port), debug=True)
    ```
    
    Pour faire tourner le serveur, il faut exécuter le fichier python AppServeur/api.py.

    ```sh
    $ cd AppServeur
    $ python api.py
    ```
    Si le texte suivant apparait, c'est que l'API est bien fonctionnelle et est connectée sur le localhost.
    ```sh
    * Serving Flask app "api" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: on
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 149-997-926
     * Running on http://localhost:9090/ (Press CTRL+C to quit)
     ```
     
- ## Démarrer et paramétrer le client : 
    Pour jouer, il faut lancer l'application Client.
    Cette application client ira se connecter, lorsque nécessaire, à l'API. Si vous modifiez l'adresse de l'API, il faut également la modifier dans le fichier AppClient/RequestsTools/AddressTools dans la fonction get_absolute_address.
    ```sh
    def get_absolute_address():
        return 'http://localhost:9090' #adresse de l'API
    ```
    Pour lancer l'application Client, il faut executer le fichier python AppClient/appClient.py
    ```sh
    $ cd AppClient
    $ python appClient.py
    ```

- Si l'application serveur et l'application client sont lancées, vous pourrez jouer sans difficultés! Bien sur, pour ce projet, il est nécessaire de lancer au moins 2 applications clients (et pourquoi pas plus) afin de pouvoir jouer en local.
     
# Autres informations importantes :
