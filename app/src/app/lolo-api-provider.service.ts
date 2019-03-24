import {Injectable} from '@angular/core';

import {HttpClient} from '@angular/common/http';


@Injectable()
export class LoloApiProviderService {

    constructor(public http: HttpClient) {
    }

    //apiUrl = "http://127.0.0.1:5000/lolo/api/v1.0/";
    apiUrl = 'https://chatbook.xyz/lolo/lolo/api/v1.0/';

    doRegister(name, email, language_to_learn) {
        return this.http.post(this.apiUrl + 'user/register', {
            data: {
                user: {
                    name: name,
                    email: email,
                    language_to_learn: language_to_learn
                }
            }
        });
    }

    doAuth(email) {
        return this.http.post(this.apiUrl + 'user/auth', {
            data: {
                user: {
                    email: email,
                }
            }
        });
    }

    getLearningWords(count, userid) {
        return this.http.get(this.apiUrl + 'user/' + userid + '/learn/words/' + count);
    }

    getTestingWords(count, userid) {
        return this.http.get(this.apiUrl + 'user/' + userid + '/test/words/' + count);
    }

    getTopics() {
        return this.http.get(this.apiUrl + 'topics');
    }

    getLanguages() {
        return this.http.get(this.apiUrl + 'languages');
    }

    getPreferences(userid) {
        return this.http.get(this.apiUrl + 'user/' + userid + '/preferences');
    }

    setPreferences(preferences, userid) {
        return this.http.post(this.apiUrl + 'user/' + userid + '/preferences', {
            "data": {
                "preferences": preferences //an array of selected preferences//
            }
        });
    }

    getUserLanguage(userid) {
        return this.http.get(this.apiUrl + 'user/' + userid + '/language_to_learn');
    }

    setUserLanguage(language, userid) {
        return this.http.post(this.apiUrl + 'user/' + userid + '/language_to_learn', {
            "data": {
                "language_to_learn": language //an array of selected preferences//
            }
        });
    }


    updateLearnedWords(words, userid) {
        return this.http.post(this.apiUrl + 'user/' + userid + '/learn/update', {
            "data": {
                "learned": words
            }
        });
    }

    updateTestedWords(words, userid) {
        return this.http.post(this.apiUrl + 'user/' + userid + '/test/update', {
            "data": {
                "tested": words
            }
        });
    }
}
