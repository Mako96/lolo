import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-learn',
  templateUrl: './learn.page.html',
  styleUrls: ['./learn.page.scss'],
})
export class LearnPage implements OnInit {
 
  public index:number=0;
  public preferences:any;
  public level:number;
  public data = [
    { word: 'Blue :: Bleu', w1:'Bleu', w2:'Rouge',  w3:'Vert', w4:'Orange', im1:"../../assets/Data/Bleu.png",im2:"../../assets/Data/Rouge.png",im3:"../../assets/Data/Vert.png",im4:"../../assets/Data/Orange.png" },
    { word: 'Run :: Courir ', w1:'marche', w2:'Saut',  w3:'courir', w4:'nager', im1:"../../assets/Data/marche.jpg",im2:"../../assets/Data/Saut.jpg",im3:"../../assets/Data/courir.jpg",im4:"../../assets/Data/nager.jpg"  }
  ];

  constructor(private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
  }

  next(){
    // index for the Data ( for demo just two values (0,1) )
    this.index=Math.round(Math.random());
    alert(this.index);
  }


}
