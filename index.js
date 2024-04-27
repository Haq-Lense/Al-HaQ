function fetchTweets() {
    // Remplacez URL_DU_ENDPOINT par l'URL de l'API qui fournit les tweets au format JSON
    const apiUrl = "http://localhost:8081/stock/fournisseur";


    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Une fois que les données sont récupérées avec succès, vous pouvez les traiter ici
            console.log("Tweets récupérés:", data);
            // Vous pouvez appeler une fonction pour traiter les tweets ici
            processTweets(data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function processTweets(tweets) {
    // Cette fonction peut être utilisée pour traiter les tweets récupérés
    // Par exemple, vous pouvez afficher les tweets dans une liste sur la page web
    // ou les manipuler d'une autre manière selon vos besoins
    tweets.forEach(tweet => {
        console.log("Tweet:", tweet);
        // Faites quelque chose avec chaque tweet, par exemple l'afficher sur la page web
    });
}

// Utilisez la fonction fetchTweets pour récupérer les tweets
fetchTweets();