import { Component, OnInit } from '@angular/core';
import {LoloUserProviderService} from '../lolo-user-provider.service';
import { ToastController } from '@ionic/angular';


@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.page.html',
  styleUrls: ['./statistics.page.scss'],
})
export class StatisticsPage implements OnInit {


  public completedWords = [];
  constructor(private userProvider: LoloUserProviderService) { }

  getCompletedWords() {
    var _self = this;
    //TODO complete this function and userprovider getCompletedWords function too
    _self.completedWords = this.userProvider.getCompletedWords();
    //TODO: for each topic: we make a circle with number of words completed in tests

  }

  ngOnInit() {
  }



}
