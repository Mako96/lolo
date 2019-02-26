import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoloUserProviderService {

  constructor() { }
  userid = 0;
  
  setUserID(userid) {
  	this.userid = userid;
  }
  getUserID() {
  	return this.userid;
  }
}
