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

  ngOnInit() {
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
