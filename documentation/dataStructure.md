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
				word: ’red’ ,
				lang: 'fr',
				topic : 'colours',
				datelastSeen:  Date(2013,11,10,2,35),
				numberOfTimesSeen: 4,
			},
			{
				word: ’orange’ ,
				lang: 'fr',
				topic : 'colours',
				datelastSeen:  Date(2013,11,10,2,35)
				numberOfTimesSeen: 10,
			}
		]
	 

		testedWords: [
			{
				word: ’red’ ,
				lang: 'fr',
				topic : 'colours',
				datelastSeen:  Date(2015,5,10,2,5),
				result: [
					{
						date:  Date(2013,11,10,2,35),
						sucess: True,
						test: 'Written',
					},
					{
						date:  Date(2012,19,4,2,35),
						sucess: False,
						test: 'Written',
					}
				]
			},
			{
				word: ’orange’ ,
				lang: 'fr',
				topic : 'colours',
				result: [
					{
						date:  Date(2013,11,10,2,35),
						sucess: True,
						test: 'Written',
					},
					{
						date:  Date(2012,19,4,2,35),
						sucess: Flase,
						test: 'Written',
					}
				]
			}

		]
	}
