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
| PUT         | http://lolo.ai/lolo/api/v1.0/user/{iduser}/learn/summary | Update user learn progress     | application/json | application/json |
| PUT         | http://lolo.ai/lolo/api/v1.0/user/{iduser}/test/summary  | Update user test progress      | application/json | application/json |

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
        "message" : "Successfully registered"
    },
    "error":{
        "code" : "failed"
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
        "code" : "failed",
        "message" : "The user is not registered yet"
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
        "code" : "failed"
    }
}
```

### Set preferences
When the user has selected his/her preferences a post action has to be done in order to save them in the database:
```json
{
    "data": {
        "preferences":[
            {
                "name" : "category2"
            }
        ]
    }
}
```
The response will be:
```json
{
    "data":{
        "message" : "Preferences saved"
    },
    "error":{
        "code" : "failed",
        "message" : "There is an error in the preferences"
    }
}
```

### Get words to learn
The response will be:
```json
{
    "data":{
        "learn": {
            "words" : [
                {
                    "EN" : "Hello",
                    "FR" : "Salut",
                    "IMG" : "http://...."
                },
                {
                    "EN" : "Bye",
                    "FR" : "Aurevoir",
                    "IMG" : "http://...."
                }
            ]
        },
        "complementary" : {
            "words" : [
                {
                    "EN" : "Morning",
                    "FR" : "Matin",
                    "IMG" : "http://...."
                },
                {
                    "EN" : "Night",
                    "FR" : "soir",
                    "IMG" : "http://...."
                }
            ]
        }
    },
    "error":{
        "code" : "failed",
        "message" : "Something wrong with the words"
    }
}
```

### Get words to test
The response will be:
```json
{
    "data":{
        "test": {
            "words" : [
                {
                    "EN" : "Hello",
                    "FR" : "Salut",
                    "IMG" : "http://...."
                },
                {
                    "EN" : "Bye",
                    "FR" : "Aurevoir",
                    "IMG" : "http://...."
                }
            ]
        },
        "complementary" : {
            "words" : [
                {
                    "EN" : "Morning",
                    "FR" : "Matin",
                    "IMG" : "http://...."
                },
                {
                    "EN" : "Night",
                    "FR" : "soir",
                    "IMG" : "http://...."
                }
            ]
        }
    },
    "error":{
        "code" : "failed",
        "message" : "Something wrong with the words"
    }
}
```
### Update learn progress
To define ...

### Update test progress
To define ...