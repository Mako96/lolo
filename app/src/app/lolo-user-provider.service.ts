import { Injectable } from '@angular/core';
import { LoloApiProviderService } from './lolo-api-provider.service';

@Injectable({
  providedIn: 'root'
})
export class LoloUserProviderService {

  constructor(private apiProvider: LoloApiProviderService,) { }
  userid = 0;
  genericApiErrorMsg = 'Unknown API error, please try again later';

  setUserID(userid) {
  	this.userid = userid;
  }
  getUserID() {
  	return this.userid;
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
            	this.setUserID(data.data.userid);
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
            	this.setUserID(data.data.userid);
            	cbSucces(data.data);
            } else {
            	cbError({'message': this.genericApiErrorMsg});
            }
        });
    }
    getLearningWords(cbSucces, cbError) {
     	this.apiProvider.getLearningWords(10, this.getUserID()).subscribe((data: any)=>{
               if(data.error !== undefined){
               	cbError(data.error);
               } else if (data.data !== undefined) {
               	cbSucces(data.data);
               } else {
               	cbError({'message': this.genericApiErrorMsg});
               }
           });
    }

}
