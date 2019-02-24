## Vocabulary collection 

### Format of a document :

	{
		en: 'red',
		fr: 'rouge',
		topic: 'colours',
		url: '/data/pictures/red.png' ,
	}


*  * * 

## User collection 

### Format of a document :

	{
		email: ‘example@example.com’ ,
		interests: [‘colours’, ‘animals’],
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
			{
				wordID: 09184690238,
				lang: "fr"
				result: [
					{
						date:  Date(2013,11,10,2,35),
						sucess: True,
						type: 'Written',
					},
					{
						date:  Date(2012,19,4,2,35),
						sucess: False,
						type: 'Written',
					}
				]
			},
			{
				wordID: 09184690238,
				lang: "fr"
				result: [
					{
						date:  Date(2013,11,10,2,35),
						sucess: True,
						type: 'Written',
					},
					{
						date:  Date(2012,19,4,2,35),
						sucess: False,
						type: 'Written',
					}
				]
			}

		]
	}
