import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { formArrayNameProvider } from '@angular/forms/src/directives/reactive_directives/form_group_name';
import { PreferencesPage } from '../preferences/preferences.page';
@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  constructor(private router:Router) { }

  ngOnInit() {
  }

  start(){
    //here there must be checking if the email is registered "for now it's -ture condition-"
    if (true)
    { 
    this.router.navigate(['preferences']);
    }
    else
    {
      alert("Invalid credentials");
    }
  }

  goBack(){
    this.router.navigate(['home']);
  }
}
