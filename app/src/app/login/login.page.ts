import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { formArrayNameProvider } from '@angular/forms/src/directives/reactive_directives/form_group_name';
import { PreferencesPage } from '../preferences/preferences.page';

import { LoloUserProviderService } from '../lolo-user-provider.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  email_V:string;
  constructor(private router:Router, private userProvider: LoloUserProviderService) { }

  ngOnInit() {
  }

  start(){
  	var _self = this;
  	var cbError = function(error){alert(error.message);};
    	var cbSucces = function(data){
            	alert(data.message);
            	_self.router.navigate(["main"]);
        };
    	this.userProvider.doLogin(this.email_V, cbSucces, cbError);
  }

  goBack(){
    this.router.navigate(['home']);
  }
}
