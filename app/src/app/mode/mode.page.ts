import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { ViewChild} from '@angular/core';
import { IonSlides } from '@ionic/angular';
import { Router,NavigationExtras } from '@angular/router';

@Component({
  selector: 'app-mode',
  templateUrl: './mode.page.html',
  styleUrls: ['./mode.page.scss'],
})
export class ModePage implements OnInit {
  preferences:any;
  @ViewChild(IonSlides) slides: IonSlides;

  public value:number;

  constructor(private router: Router, private route: ActivatedRoute) {
    this.value=0;
   }

  public modes=[
    { val:5  ,type:"../../assets/images/mode/difficulty_easy.jpg" },
    { val:10 ,type:"../../assets/images/mode/difficulty_medium.jpg" },
    { val:15 ,type: "../../assets/images/mode/difficulty_hard.jpg" }
  ];

  
  
 
 /* set()
  {
   alert(this.modes[this.value].val);
  }*/


  // Slider changer function
  slideChanged() { 
    this.slides.getActiveIndex().then(
      ind=>
      this.value=ind
    );
  

}

  ngOnInit() {
   
  }
  
   // mode next Button
  nextClick()
  {

//upload the mode 
  this.router.navigate(['learn']);

  }

}
