# APIjeux -- Descriptif rapide l'application
- ## Qu'est-ce qu'APIjeux, description du projet:
    APIjeux est le nom que nous avons choisi de donner à notre projet informatique du 1er semestre de 2ème année à l'ENSAI. L'objectif du projet est le développement d'une **RESTful API python permettant de jouer, via une application cliente, à des jeux de plateau en ligne**.
    L'un des principaux objectifs est que l'**application soit suffisament flexible pour supporter des jeux suffisamment variés sans trop de changements au niveau son code**.
- ## Notre réalisation du projet:
    Pour réaliser notre projet informatique, nous avons choisi de développer deux jeux, à savoir le **Puissance4** et le **jeu de l'Oie**. En effet, nous avons estimé que ces deux jeux étaient suffisamment différents l'un de l'autre pour prouver la fléxibiliter de notre application.
    Ainsi, dans toute la suite, APIjeux désigne l'ensemble des applications client et serveur.
    En plus des fonctionnalités demandées (pourvoir jouer à des jeux), nous avons réalisé toute une partie **gestion de compte**, avec notamment la gestion d'amis, de scores et de classements.
De plus, nous avons intégré la possibilité de jouer avec des amis ou contre des inconnus. Jouer avec des amis se fait, comme pour la plupart des jeux en ligne, en rejoignant une salle dont notre ami nous à transférer le code.
# Classes testées et commentées 
- ## Documentation et commentaires:
    Nos deux applications, client comme serveur, sont quasi-entièrement documentées via la documentation docstring selon la [convention pep257](https://www.python.org/dev/peps/pep-0257/), au [format numpy](https://numpydoc.readthedocs.io/en/latest/). Pour l'application client, les classes métiers et services sont commentées, tandis que pour l'application serveur, les classes serveur, DAO, services et métier sont commentées. De plus, lorsque nécessaire, certaines autres fonctions sont documentées. Enfin, en plus d'être documentées, les fonctions sont commentées au maximum, notamment les fonctions API qui régissent le serveur, pour comprendre au maximum comment se déroulent les actions. On notera également que, dans un soucis de clarté, le serveur effectue de nombreux *print* dans la console pour expliquer les différentes actions qu'il vient d'effectuer.
- ## Classes testées:
    Malheuresement, du fait de contraintes de temps assez élevées, nous n'avons pas vraiment respecté les règles qui veulent que nous rédigions d'abord les test unitaires puis les fonctions pour pouvoir directement tester les tests dessus. Ici, nous avons d'abord codé l'application et n'avons pu rédiger des test que sur la partie DAO de l'application.
    
    ICI, FAIRE UN BLABLA SUR LES TESTS DE MAEL!!

# Comment installer APIjeux
- ## Télécharger le code :
    Pour récupérer le code du serveur APIjeux et le code du Client APIjeux, le plus simple est de clonner le [dépot github](https://github.com/clementgabas/Projet-Info) comme si dessous :
    ```sh
    $ git clone https://github.com/clementgabas/Projet-Info
    ```
    Vous téléchargerez alors un dossier nommé **Projet-Info** contenant :
    - un dossier AppClient : dossier contenant le code de l'application cliente
    - un dossier AppServeur : dossier contenant le code de l'application serveur API
    - un fichier init_db.sql : fichier sql contennant le code sql permettant d'initialiser la base de données (cf [base de données](#base_de_données))
 
 - ## Packages python nécessaires :
   
    Les packages nécessaires au bon fonctionnement de chaque application (client et serveur) sont précisées dans les fichiers **AppClient/requirements.txt** et **AppServeur/requirements.txt**
    Pour les intaller, le plus simple est d'utiliser pip et de lancer la commande suivante 
    ```sh
    $ python -m pip install -r requirements.txt
    ```
   
    Nous listons ci-dessous cet ensemble de packages nécessaires : 
    > requests==2.24.0;
    flask_restplus==0.13.0;
    loguru==0.5.3;
    Flask_Caching==1.9.0;
    Flask==1.1.2;
    colorama==0.4.4;
    tabulate==0.8.7;
    PyInquirer==1.0.3;
    PyYAML==5.3.1;
    
     **Attention : Si lors du lancement de l'application serveur, un message d'erreur concernant le package werkzeug apparait, il faut rétrograder werkzeug à la version Werkzeug       == 0.16.1** via la commande
    ```sh
    $ python -m pip install Werkzeug==0.16.1
    ```
    
- [##Base de données](#Base_de_données):
    Le fichier *db_init.sql* contient le code SQL permettant d'initialiser la base de données. Nous avons décidé de nommer notre base de données **apijeux.db**. De plus, pour des raions techniques liée au fait qu'il était plus simple de coder depuis chez soi sans devoir se connecter au serveur SQL de l'école, nous avons opté pour une base de donnée en local, au moins le temps de la programmation. De ce fait, chacun avait sa version de la base et toutes ces versions étaient désynchronisées, mais cela n'était pas génant.
    La base de donnée est stockée dans le fichier AppServeur/database.
    Si vous voulez modifier le nom de la base de données ou son emplacement, il faudra modifier le fichier *AppServeur/DAO/gestion.py* qui contient une fonction permettant aux différentes DAO de se connecter à la base de données :
    ```sh
    def get_db_address():
        return "database/apijeux.db" #chemin de la base de données, relatif depuis AppServeur/api.py

    ```

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
