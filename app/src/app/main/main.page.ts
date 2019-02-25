import { Component, OnInit } from '@angular/core';
import { Router,NavigationExtras, ActivatedRoute } from '@angular/router';
import { all } from 'q';

@Component({
  selector: 'app-main',
  templateUrl: './main.page.html',
  styleUrls: ['./main.page.scss'],
})
export class MainPage implements OnInit {
 public preferences:any;
 public level:number;
  constructor(private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.queryParams.subscribe(
      params => {
        this.preferences =JSON.parse(params["prefer"]);
        this.level =params["level"];
      }
    )
  }


  learnPage(){


  this.router.navigate(['mode']);
    
  }

  
  testPage(){


  this.router.navigate(['test']);
    
  }

  ChangePreference()
  {

    this.router.navigate(['preferences']);
  }



}
