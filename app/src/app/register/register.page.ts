import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {

  firstName_V:string;
  lastName_V:string;
  email_V:string;
  constructor(private router: Router){

  }

  ngOnInit() {
  }

  submitClick()
  {
    if (this.firstName_V.length > 0 && this.email_V.length > 0 && this.lastName_V.length > 0)
    {
    alert("Thank you for Registration");
    }
    else
     alert("Fill in the blanks, please");

  }

  goBack(){
    this.router.navigate(['home']);
  }

}
