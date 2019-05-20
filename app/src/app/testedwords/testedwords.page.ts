import { Component, OnInit } from '@angular/core';
import {LoloUserProviderService} from '../lolo-user-provider.service';
import { Router,NavigationExtras, ActivatedRoute } from '@angular/router';
import { ToastController } from '@ionic/angular';


@Component({
  selector: 'app-testedwords',
  templateUrl: './testedwords.page.html',
  styleUrls: ['./testedwords.page.scss'],
})
export class TestedwordsPage implements OnInit {

  constructor(private userProvider: LoloUserProviderService,private router: Router) { }
  public completedWords = {};
  ngOnInit() {
    this.getUserTestedWords();
  }

  getUserTestedWords(){
    /*TODO*/
    var _self = this;
    var cbError = function (error) {
        alert(error.message);
        _self.completedWords = []
    };
    var cbSucces = function (data) {
        console.log(data);
        _self.completedWords = data.stat
    };
    this.userProvider.getUserTestedWords(cbSucces, cbError);
  }








  goBack()
  {
    this.router.navigate(['main']);
  }
  goStatistics()
  {
    this.router.navigate(['statistics']);
  }
}
