import { Component, OnInit } from '@angular/core';
import {LoloUserProviderService} from '../lolo-user-provider.service';
import { Router,NavigationExtras, ActivatedRoute } from '@angular/router';
import { ToastController } from '@ionic/angular';


@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.page.html',
  styleUrls: ['./statistics.page.scss'],
})
export class StatisticsPage implements OnInit {

  public learningLang;
  public langs = {"fr":"French", "de":"German","swe":"Swedish"}
  public completedWords = {};
  constructor(private userProvider: LoloUserProviderService,private router: Router) { }

  getUserStatistics() {
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
            _self.completedWords = []
        };
        var cbSucces = function (data) {
            console.log(data);
            _self.completedWords = data.stat
        };
        this.userProvider.getUserStatistics(cbSucces, cbError);
    }

  ngOnInit() {
    this.getUserStatistics()
    this.getUserLanguage()
  }

  getUserLanguage() {
      var _self = this;
      var cbError = function (error) {
          alert(error.message);
          _self.learningLang = "fr" //if it fails the default language is french
      };
      var cbSucces = function (data) {
          console.log(data);
          _self.learningLang = data.lang
      };
      this.userProvider.getUserLanguage(cbSucces, cbError);
  }


  goBack()
  {

    this.router.navigate(['main']);
  }



}
