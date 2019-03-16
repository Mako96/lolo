import {Injectable} from '@angular/core';
import {LoloApiProviderService} from './lolo-api-provider.service';
import {Storage} from '@ionic/storage';

@Injectable({
    providedIn: 'root'
})
export class LoloUserProviderService {

    constructor(private apiProvider: LoloApiProviderService, private storage: Storage) {

    }

    userid = undefined;
    genericApiErrorMsg = 'Unknown API error, please try again later';

    setUserID(userid) {
        console.log('set userid ' + userid);
        this.storage.set('userid', userid);
        this.userid = userid;
    }

    getUserID(cb) {
        if (this.userid !== undefined && this.userid !== null) {
            cb(this.userid);
        } else {
            this.storage.get('userid').then((uid) => {
                cb(uid);
            });
        }

    }


    setPreferences(preferences, cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.setPreferences(preferences, userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    getPreferences(cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.getPreferences(userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    getTopics(cbSucces, cbError) {
        var _self = this;
        this.apiProvider.getTopics().subscribe((data: any) => {
            if (data.error !== undefined) {
                cbError(data.error);
            } else if (data.data !== undefined) {
                cbSucces(data.data);
            } else {
                cbError({'message': _self.genericApiErrorMsg});
            }
        });
    }

    setUserLanguage(language, cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.setUserLanguage(language, userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    getLanguages(cbSucces, cbError) {
        var _self = this;
        this.apiProvider.getLanguages().subscribe((data: any) => {
            if (data.error !== undefined) {
                cbError(data.error);
            } else if (data.data !== undefined) {
                cbSucces(data.data);
            } else {
                cbError({'message': _self.genericApiErrorMsg});
            }
        });
    }

    doRegister(firstname, email, language_to_learn, cbSucces, cbError) {
        this.apiProvider.doRegister(firstname, email, language_to_learn).subscribe((data: any) => {
            if (data.error !== undefined) {
                cbError(data.error);
            } else if (data.data !== undefined) {
                this.setUserID(data.data.id);
                cbSucces(data.data);
            } else {
                cbError({'message': this.genericApiErrorMsg});
            }
        });
    }

    doLogin(email, cbSucces, cbError) {
        this.apiProvider.doAuth(email).subscribe((data: any) => {
            if (data.error !== undefined) {
                cbError(data.error);
            } else if (data.data !== undefined) {
                this.setUserID(data.data.id);
                cbSucces(data.data);
            } else {
                cbError({'message': this.genericApiErrorMsg});
            }
        });
    }

    getUserLanguage(cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.getUserLanguage(userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    getLearningWords(cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.getLearningWords(5, userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    updateLearnedWords(words, cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.updateLearnedWords(words, userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    getTestingWords(cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.getTestingWords(5, userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

    updateTestedWords(words, cbSucces, cbError) {
        var _self = this;
        this.getUserID(function (userid) {
            _self.apiProvider.updateTestedWords(words, userid).subscribe((data: any) => {
                if (data.error !== undefined) {
                    cbError(data.error);
                } else if (data.data !== undefined) {
                    cbSucces(data.data);
                } else {
                    cbError({'message': _self.genericApiErrorMsg});
                }
            });
        });
    }

}
