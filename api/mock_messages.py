

register_message = {
    "data": {
        "message": "Successfully registered"
    },
    "error": {
        "code": "failed"
    }
}

auth_message = {
    "data": {
        "message": "Authentication correct"
    },
    "error": {
        "code": "failed",
        "message": "The user is not registered yet"
    }
}

preferences_message = {
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

set_preferences_message = {
    "data":{
        "message" : "Preferences saved"
    },
    "error":{
        "code" : "failed",
        "message" : "There is an error in the preferences"
    }
}

learn_words_message = {
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

test_words_message = {
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

learn_summary_message = {
    "dont": "yet"
}

test_summary_message = {
    "dont": "yet"
}