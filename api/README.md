# Lolo REST API

## Services

| HTTP Method | URI                                             | Action                         | Content type     | Response         |
|-------------|-------------------------------------------------|--------------------------------|------------------|------------------|
| POST        | http://lolo.ai/lolo/api/v1.0/user/register      | Register a new user to the DB  | application/json | application/json |
| POST        | http://lolo.ai/lolo/api/v1.0/user/auth          | Authenticate a user            | application/json | application/json |
| GET         | http://lolo.ai/lolo/api/v1.0/preferences        | Retrieve lolo categories       | application/json | application/json |
| POST        | http://lolo.ai/lolo/api/v1.0/user/{iduser}/preferences   | Save user selected preferences | application/json | application/json |
| GET         | http://lolo.ai/lolo/api/v1.0/user/{iduser}/learn/words   | Retrieve set of words to learn | application/json | application/json |
| GET         | http://lolo.ai/lolo/api/v1.0/user/{iduser}/test/words    | Retrieve set of words to test  | application/json | application/json |
| POST         | http://lolo.ai/lolo/api/v1.0/user/{iduser}/learn/update | Update user learn progress     | application/json | application/json |
| POST         | http://lolo.ai/lolo/api/v1.0/user/{iduser}/test/update  | Update user test progress      | application/json | application/json |

### Register
This services will require a payload with the following structure:
```json
{
    "data": {
        "user": {
            "name" : "any name",
            "email" : "any email"
        }
    }
}
```
The response will be:
```json
{
    "data":{
        "message" : "Successfully registered",
        "userid": "some user id"
    },
    "error":{
        "message" : "Something went wrong"
    }
}
```

### Authenticate
This should be saved in mobile phone and send it each time a request is done.
```json
{
    "data": {
        "user": {
            "email" : "any email"
        }
    }
}
```
The response will be:
```json
{
    "data":{
        "message" : "Authentication correct"
    },
    "error":{
        "message" : "Authentication failed
    }
}
```
### Choose preferences
The first step is to get the available preferences from the server to show to the user
The response will be:
```json
{
    "data":{
        "preferences" : [
            {
                "name" : "category1", 
                "image": "http://......"
            },
            {
                "name" : "category2", 
                "image": "http://......"
            },
        ]
    },
    "error":{
        "message" : "failed"
    }
}
```

### Set preferences
When the user has selected his/her preferences a post action has to be done in order to save them in the database:
```json
{
    "data": {
        "preferences":[ "category2" ]
    }
}
```
The response will be:
```json
{
    "data":{
        "message" : "Preferences successfully saved"
    },
    "error":{
        "message" : "Something went wrong"
    }
}
```

### Get words to learn
The response will be:
```json
{
    "data":{
        "words": [
            {
                "to_learn": {
                    "_id": "5c713a8802045a96c31771a6",
                    "en": "chicken",
                    "fr": "poulet",
                    "topic": "animals",
                    "url": "pictures/animals/chicken.jpg"
                },
                "complementary": [
                    {
                        "_id": "5c713a8802045a96c31771b4",
                        "en": "frog",
                        "fr": "la grenouille",
                        "topic": "animals",
                        "url": "pictures/animals/frog.jpg"
                    },
                    {
                        "_id": "5c713a8802045a96c31771ce",
                        "en": "rat",
                        "fr": "rat",
                        "topic": "animals",
                        "url": "pictures/animals/rat.jpg"
                    },
                    {
                        "_id": "5c713a8802045a96c31771e6",
                        "en": "weasel",
                        "fr": "belette",
                        "topic": "animals",
                        "url": "pictures/animals/weasel.jpg"
                    }
                ]
            }
        ]
    },
    "error":{
        "message" : "Something went wrong with the words"
    }
}
```

### Get words to test
The response will be:
```json
{
    "data":{
        "words": [
            {
                "to_learn": {
                    "_id": "5c713a8802045a96c31771a6",
                    "en": "chicken",
                    "fr": "poulet",
                    "topic": "animals",
                    "url": "pictures/animals/chicken.jpg"
                },
                "complementary": [
                    {
                        "_id": "5c713a8802045a96c31771b4",
                        "en": "frog",
                        "fr": "la grenouille",
                        "topic": "animals",
                        "url": "pictures/animals/frog.jpg"
                    },
                    {
                        "_id": "5c713a8802045a96c31771ce",
                        "en": "rat",
                        "fr": "rat",
                        "topic": "animals",
                        "url": "pictures/animals/rat.jpg"
                    },
                    {
                        "_id": "5c713a8802045a96c31771e6",
                        "en": "weasel",
                        "fr": "belette",
                        "topic": "animals",
                        "url": "pictures/animals/weasel.jpg"
                    }
                ]
            }
        ]
    },
    "error":{
        "message" : "Something went wrong with the words"
    }
}
```
### Update learn progress
The body of the POST request should be:
```json
{
    "data":{
        "learned" : [
            {
                "wordID": "a word id", "lang": "FR"
            },
            {
                "wordID": "a word id", "lang": "FR"
            }
        ]
    }
}
```
response:
```json
{
    "data":{
        "message" : "Successfully updated"
    },
    "error":{
        "message" : "Something went wrong"
    }
}
```

### Update test progress
```json
{
    "data":{
        "tested" : [
            {
                "wordID": "a word id", "success": true, "type": "written", "lang": "fr"
            },
            {
                "wordID": "a word id", "success": false, "type": "written", "lang": "fr"
            }
        ]
    }
}
```
response:
```json
{
    "data":{
        "message" : "Successfully updated"
    },
    "error":{
        "message" : "Something went wrong"
    }
}