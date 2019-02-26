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
  constructor(private router: Router,private apiProvider: LoloApiProviderService, private userProvider: LoloUserProviderService){

  }

  ngOnInit() {
  }

  submitClick()
  {
    if (this.firstName_V.length > 0 && this.email_V.length > 0 && this.lastName_V.length > 0)
    {
    	this.apiProvider.doRegister(this.firstName_V, this.email_V).subscribe((data: any)=>{
            console.log(data);
            if(data.error !== undefined){
            	alert(data.error.message);
            } else if (data.data !== undefined) {
            	this.userProvider.setUserID(data.data.userid);
            	alert(data.data.message);
            	this.router.navigate(["main"]);
            } else {
            	alert('Unknown API error, please try again later');
            }
        });
    }
    else
     alert("Fill in the blanks, please");
  }

  goBack(){
    this.router.navigate(['home']);
  }

}
