import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { formArrayNameProvider } from '@angular/forms/src/directives/reactive_directives/form_group_name';
import { PreferencesPage } from '../preferences/preferences.page';
import { ToastController } from '@ionic/angular';
import { LoloUserProviderService } from '../lolo-user-provider.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  email_V:string;
  message:any;
  constructor(private router:Router, private userProvider: LoloUserProviderService, private toastController: ToastController) { }

  ngOnInit() {
  }

  start(){
  	var _self = this;
  	var cbError = (error) => {this.presentToast(error.message)};
    var cbSucces = (data) => {
              // alert(data.message);
              // this.message = data.message
              this.presentToast(data.message)
              _self.router.navigate(["main"]);
              
        };
      this.userProvider.doLogin(this.email_V, cbSucces, cbError);
      
  }

  goBack(){
    this.router.navigate(['tutorial']);
  }

  goRegister(){
    this.router.navigate(['register']);
    
  }

  async presentToast(message) {
    let toast = await this.toastController.create({
      message: message,
      duration: 2000,
    });
    toast.present();
  }
}