import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';


@Injectable()
export class LoloApiProviderService {

  constructor(public http: HttpClient) { }
  
  apiUrl = "http://localhost:5000/lolo/api/v1.0/";
  
  doRegister(name, email) {
	return this.http.post(this.apiUrl + 'user/register', {
	    data: {
		user: {
		    name : name,
		    email : email,
		}
	    }});
  }
  
  doAuth(email) {
	return this.http.post(this.apiUrl + 'user/auth', {
	    data: {
		user: {
		    email : email,
		}
	    }});
  }
  
  getPreferences() {
	return this.http.get(this.apiUrl + 'preferences');
  }
  setPreferences(preferences, userid){
  	return this.http.post(this.apiUrl + 'user/'+userid+'/preferences', {
	    "data": {
			"preferences": preferences //an array of selected preferences//
		    }
	});
  }
}
