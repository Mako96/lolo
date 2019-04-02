## Vocabulary collection 

### Format of a document :

	{
	
       "_id":ObjectId("5c93ee042344ef2258888088"),
       "topic":"animals",
       "id":"bear",
       "url":"pictures/animals/bear.jpg",          
       "es":{
          "word":"oso",
          "difficulty_level":0,
          "score": 0,
          "sentences":[
             "También describió a otros gatos, lobos, osos, pecaríes, camellos y muchos otros vertebrados de La Brea; La imagen de la derecha lo muestra en el campo en La Brea.",
             "En algunas partes de América, a las personas les gusta cazar ciervos, alces y osos, mientras que en otras áreas cazan jabalíes.",
             "De América del Norte vinieron ardillas y mapaches, osos y bisontes, águilas y un alce.",
             "Esta vez la señora Blade llama y ella es un oso por la mañana."
          ]
       },
       
       "en":{
          "word":"bear",
          "difficulty_level":0,
          "score": 0,
          "sentences":[
             [
                "He also described other cats, wolves, bears, peccaries, camels, and many other vertebrates from La Brea; the picture on the right depicts him in the field at La Brea.",
                "In some parts of America, people like to hunt deer, elk and bears, while in other areas they hunt wild boars.",
                "From North America came squirrels and raccoons, bears and bison, eagles and an elk.",
                "This time Mrs. Blade calls in and she is a bear in the morning."
             ]
          ]
       },
       "fr":{
          "word":"ours",
          "difficulty_level":0,
          "score": 0,
          "sentences":[
             "Il a également décrit d'autres chats, loups, ours, pécaris, chameaux et de nombreux autres vertébrés de La Brea; la photo de droite le représente sur le terrain à La Brea.",
             "Dans certaines régions d'Amérique, les habitants aiment chasser le cerf, le wapiti et l'ours, tandis que dans d'autres régions, ils chassent les sangliers.",
             "Les écureuils et les ratons laveurs, les ours et les bisons, les aigles et un wapiti venaient d'Amérique du Nord.",
             "Cette fois, Mme Blade appelle et elle est un ours le matin."
          ]
       },
       "de":{
          "word":"Bär",
          "difficulty_level":0,
          "score": 0,
          "sentences":[
             "Er beschrieb auch andere Katzen, Wölfe, Bären, Pekaris, Kamele und viele andere Wirbeltiere aus La Brea; Das Bild rechts zeigt ihn auf dem Feld von La Brea.",
             "In einigen Gegenden Amerikas jagen die Menschen gerne Rehe, Elche und Bären, während sie in anderen Gegenden Wildschweine jagen.",
             "Aus Nordamerika kamen Eichhörnchen und Waschbären, Bären und Bisons, Adler und ein Elch.",
             "Diesmal ruft Mrs. Blade an und ist am Morgen ein Bär."
          ]
       },
   
    }


*  * *

## Language collection 

### Format of a document :

	{ 
        "display_name" : "German", 
        "lang" : "de" 
	}


*  * *  

## User collection 

### Format of a document :

	{
		email: ‘example@example.com’ ,
		interests: [‘colours’, ‘animals’],
		learning_language: "fr" //or "es" or "de" 
		taughtWords: [
			{
				wordID: 09184650943,
				lang: "fr"
				dateLastSeen:  Date(2013,11,10,2,35),
				numberOfTimesSeen: 4,
			},
			{
				wordID: 09184690238,
				lang: "fr"
				dateLastSeen:  Date(2015,5,10,2,5),
				numberOfTimesSeen: 10,
			}
		]
	 

		testedWords: [
		    // uniquely identied by: wordID, lang, type
			{
				wordID: 09184690238,
				lang: "fr",
				type: "visual",
				dateLastSeen: Date()
				nbOfFailures: 0,
				nbOfSuccess:0,
				lastResult: True //or False if the user failed the last time
			},
		]
	}
