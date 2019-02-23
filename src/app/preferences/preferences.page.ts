import { Component, OnInit } from '@angular/core';
import { Router,NavigationExtras } from '@angular/router';

@Component({
  selector: 'app-preferences',
  templateUrl: './preferences.page.html',
  styleUrls: ['./preferences.page.scss'],
})
export class PreferencesPage implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  buttonClick(item){
    alert(item);
  }
  
  public form = [
    { val: 'Animals', isChecked: false , img:"../../assets/images/topics/animals.jpg" },
    { val: 'Colors', isChecked: false  , img: "../../assets/images/topics/colors.jpg" },
    { val: 'fruits', isChecked: true  , img: "../../assets/images/topics/fruits.jpg" },
    { val: 'Sports', isChecked: false , img:"../../assets/images/topics/sports.jpg" },
    { val: 'Stationery', isChecked: false , img:"../../assets/images/topics/Stationery.jpg" },
    { val: 'Clothes', isChecked: false , img:"../../assets/images/topics/cloth.jpg"  }
  ];

  nextClick(data)
  {
    
    let navigationExtras: NavigationExtras = {
      queryParams: {
          prefer:JSON.stringify(data)
          }
        };

  this.router.navigate(['mode'],navigationExtras);
  }
}


