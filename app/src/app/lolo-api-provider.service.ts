import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';


@Injectable()
export class LoloApiProviderService {

  constructor(public http: HttpClient) { }
  
  apiUrl = "http://localhost:5000/";
  
  doRegister(name, email) {
	return this.http.post(this.apiUrl + 'lolo/api/v1.0/user/register', {
	    data: {
		user: {
		    name : name,
		    email : email,
		}
	    }});
  }
}
