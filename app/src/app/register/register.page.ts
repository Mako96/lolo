import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';


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
  constructor(private router: Router,private http: HttpClient){

  }

  ngOnInit() {
  }

  submitClick()
  {
    if (this.firstName_V.length > 0 && this.email_V.length > 0 && this.lastName_V.length > 0)
    {
    this.http.post('http://localhost:5000/lolo/api/v1.0/user/register', {
    data: {
        user: {
            name : this.firstName_V,
            email : this.email_V
        }
    }}).subscribe(response => {
    this.data = response;
    console.log(this.data);
    console.log('response :'+response);
    });
    }
    else
     alert("Fill in the blanks, please");
  }

  goBack(){
    this.router.navigate(['home']);
  }

}
