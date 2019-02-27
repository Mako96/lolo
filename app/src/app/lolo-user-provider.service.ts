import { Injectable } from '@angular/core';
import { LoloApiProviderService } from './lolo-api-provider.service';
import { Storage } from '@ionic/storage';

@Injectable({
  providedIn: 'root'
})
export class LoloUserProviderService {

  constructor(private apiProvider: LoloApiProviderService, private storage: Storage) {

  }
  userid = undefined;
  genericApiErrorMsg = 'Unknown API error, please try again later';

  setUserID(userid) {
    console.log('set userid '+userid);
    this.storage.set('userid', userid);
    this.userid = userid;
  }
  getUserID(cb) {
    console.log(this.userid);
    if(this.userid !== undefined && this.userid !== null){
      cb(this.userid);
    } else {
      this.storage.get('userid').then((uid) => {
        cb(uid);
      });
    }

  }


  setPreferences(preferences, cbSucces, cbError) {
  	this.apiProvider.setPreferences(preferences, this.userid).subscribe((data: any)=>{
            if(data.error !== undefined){
            	cbError(data.error);
            } else if (data.data !== undefined) {
            	cbSucces(data.data);
            } else {
            	cbError({'message': this.genericApiErrorMsg});
            }
        });
  }
  getPreferences(cbSucces, cbError) {
  	this.apiProvider.getPreferences().subscribe((data: any)=>{
            if(data.error !== undefined){
            	cbError(data.error);
            } else if (data.data !== undefined) {
            	cbSucces(data.data);
            } else {
            	cbError({'message': this.genericApiErrorMsg});
            }
        });
  }

  doRegister(firstname, email, cbSucces, cbError) {
  	this.apiProvider.doRegister(firstname, email).subscribe((data: any)=>{
            if(data.error !== undefined){
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
  	this.apiProvider.doAuth(email).subscribe((data: any)=>{
            if(data.error !== undefined){
            	cbError(data.error);
            } else if (data.data !== undefined) {
            	this.setUserID(data.data.id);
            	cbSucces(data.data);
            } else {
            	cbError({'message': this.genericApiErrorMsg});
            }
        });
    }
    getLearningWords(cbSucces, cbError) {
      var _self = this;
      this.getUserID(function(userid){
       	_self.apiProvider.getLearningWords(10, userid).subscribe((data: any)=>{
                 if(data.error !== undefined){
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
      this.getUserID(function(userid){
       	_self.apiProvider.updateLearnedWords(words, userid).subscribe((data: any)=>{
                 if(data.error !== undefined){
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
      this.getUserID(function(userid){
       	_self.apiProvider.getTestingWords(userid).subscribe((data: any)=>{
                 if(data.error !== undefined){
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
      this.getUserID(function(userid){
       	_self.apiProvider.updateTestedWords(words, userid).subscribe((data: any)=>{
                 if(data.error !== undefined){
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
