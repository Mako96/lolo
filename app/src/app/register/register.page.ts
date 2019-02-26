import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoloApiProviderService } from '../lolo-api-provider.service';
import { LoloUserProviderService } from '../lolo-user-provider.service';


@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {

  firstName_V:string;
  lastName_V:string;
  email_V:string;
  data:any;
  resp:string;
  constructor(private router: Router, private userProvider: LoloUserProviderService){

  }

  ngOnInit() {
  }

  submitClick()
  {
    var _self=this;
    if (this.firstName_V.length > 0 && this.email_V.length > 0 && this.lastName_V.length > 0)
    {
    	var cbError = function(error){alert(error.message);};
    	var cbSucces = function(data){
            	alert(data.message);
            	_self.router.navigate(["main"]);
        };
    	this.userProvider.doRegister(this.firstName_V, this.email_V, cbSucces, cbError);
    }
    else
     alert("Fill in the blanks, please");
  }

  goBack(){
    this.router.navigate(['home']);
  }

}
