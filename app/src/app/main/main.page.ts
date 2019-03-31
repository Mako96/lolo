import { Component, OnInit } from '@angular/core';
import { Router,NavigationExtras, ActivatedRoute } from '@angular/router';
import {SpeechRecognition} from "@ionic-native/speech-recognition/ngx";
import { NavController } from '@ionic/angular';
import { Storage } from '@ionic/storage';
import { all } from 'q';

@Component({
  selector: 'app-main',
  templateUrl: './main.page.html',
  styleUrls: ['./main.page.scss'],
})
export class MainPage implements OnInit {
 public preferences:any;
 public level:number;
  constructor(public navCtrl: NavController, public storage: Storage,private router: Router, private route: ActivatedRoute, private speechRecognition: SpeechRecognition ) {this.getPermission }

  ngOnInit() {

    /*this.route.queryParams.subscribe(
      params => {
        this.preferences =JSON.parse(params["prefer"]);
        this.level =params["level"];
      }
    )*/

    this.getPermission()
  }

  getPermission() {
        this.speechRecognition.hasPermission()
            .then((hasPermission) => {
                if (!hasPermission) {
                    this.speechRecognition.requestPermission();
                }
            });
    }


  learnPage(){


  this.router.navigate(['mode']);

  }


  testPage(){


  this.router.navigate(['test']);

  }

  ShowStatistics()
  {

    this.router.navigate(['statistics']);
  }

  ChangePreference()
  {

    this.router.navigate(['preferences']);
  }

  Logout(){
    this.router.navigate(['login']);
  }
}
