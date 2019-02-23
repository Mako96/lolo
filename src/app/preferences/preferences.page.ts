import { Component, OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-preferences',
  templateUrl: './preferences.page.html',
  styleUrls: ['./preferences.page.scss'],
})
export class PreferencesPage implements OnInit {
  firstName:string;
  lastName:string;
  email:string;
  constructor(private router: Router, private navCtrl:NavController,private route: ActivatedRoute) { }

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

  ConfirmClick(data)
  {
    


// there we should save the data in the server ////////////////

this.router.navigate(["main"]);
  
  }
}


