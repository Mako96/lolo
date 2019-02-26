import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';


@Injectable()
export class LoloPreferencesProviderService {

  constructor(public http: HttpClient) { }

  apiUrl = "http://localhost:5000/";

  getPreferences() {
	   return this.http.get(this.apiUrl + 'lolo/api/v1.0/preferences');
  }
}
