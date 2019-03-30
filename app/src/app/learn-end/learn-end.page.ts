import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-learn-end',
  templateUrl: './learn-end.page.html',
  styleUrls: ['./learn-end.page.scss'],
})
export class LearnEndPage {

  constructor(private router: Router) { }

  goMain() {
  	this.router.navigate(['main'])
  }
  goLearn() {
  	this.router.navigate(['learn'])
  }
  goTest() {
  	this.router.navigate(['test'])
  }
}
