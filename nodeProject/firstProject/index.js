const moduleHttp = require('http');                 // Pour crée une variable nommée moduleHttp qui sera lié à la classe http que l'on vient d'importer 
const { createServer } = require('http');           // Pour crée une variable nommée createServer qui sera lié a la fonction createServer qui est elle même dans la classe http

// console.log('Module http :', moduleHttp);        // Va afficher le menu "help" de la classe http

const monServeur = createServer();                  // Création d'une variables lié a la fonction createServer 
let port = 8070;                                    // Création d'une variable contenant le port du de notre serveur
let host = '127.0.0.1';                             // Création d'une variable contenant le nom d'hôtes de notre serveur

// console.log('Mon serveur :', monserveur);        // Va afficher les informations de l'object de type server crée par la focntioncreateServer

monServeur.on('request', (request, response) => {
    // console.log('Request:', request);                    // Affiche la requète http complète (Enormément d'informations)
    console.log('Url requested:', request.url);             // Affiche le chemin demandé dans la requète http (/, /home, /test...)
    console.log('Http method requested:', request.method);  // Affiche la méthode http utilisé (GET, POST, DELETE...)
    const first_message = '<h1>Bienvenue sur le site!</h1></ br><hr>\n<p>Hereux de vous revoir :)!</p>';
    const different_message = "<h1>Tu n'est pas le bienvenue sur le site<h1></br><hr>\n<p>Casse toi :(!</p>";
    function header(message) {
        response.writeHead(                                     // Utiliser pour encoder les Headers
            200,                                                // Status code
            'Tout va bien :)',                                  // Message de status
            {
                'Content-type': 'text/html; charset=utf-8',     // Type du contenue à envoyé + choix de l'encodage (ici utf-8)
                'Content-length': Buffer.byteLength(message)    // Recupération de la taille du contenue qui va etre envoyé
            }
        );
    }
    if ( request.url == '/test' ) {
        header(different_message)
        response.write(different_message);                  // Répond à une requète htpp la variable different_message   
    }
    else {
        header(first_message)
        response.write(first_message);                            // Répond à une requète htpp la variable message   
    }
                                     
});

monServeur.listen(port, host, () => {               // () => {} est une fonction flex et est équivalent à : function() {}.
    console.log(`Server listening on port ${port}`);
    console.log(`Access the server : http://${host}:${port}`);
});

/* 
Il est aussi possible d'utiliser une fonction préexistante à la place d'une fonction flex comme ceci:
function launchServer() {
    console.log(`Server listening on port ${port}`);
    console.log(`Access the server : http://${host}:${port}`);
};

monServeur.listen(port, host, launchServer);
*/