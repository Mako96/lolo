import { Component, OnInit } from '@angular/core';
import {LoloUserProviderService} from '../lolo-user-provider.service';
import { ToastController } from '@ionic/angular';


@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.page.html',
  styleUrls: ['./statistics.page.scss'],
})
export class StatisticsPage implements OnInit {


  public completedWords = {};
  constructor(private userProvider: LoloUserProviderService) { }

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
  }



}
