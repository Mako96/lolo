import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { LoloUserProviderService } from '../lolo-user-provider.service';

@Component({
  selector: 'app-learn',
  templateUrl: './learn.page.html',
  styleUrls: ['./learn.page.scss'],
})
export class LearnPage implements OnInit {

  public index:number=0;
  public instance:any;
  public answer:any;
  public level:number;
  public data = [
    { word: 'Blue :: Bleu', w1:'Bleu', w2:'Rouge',  w3:'Vert', w4:'Orange', im1:"../../assets/Data/Bleu.png",im2:"../../assets/Data/Rouge.png",im3:"../../assets/Data/Vert.png",im4:"../../assets/Data/Orange.png",answer: "../../assets/Data/Bleu.png"},
    { word: 'Run :: Courir ', w1:'marche', w2:'Saut',  w3:'courir', w4:'nager', im1:"../../assets/Data/marche.jpg",im2:"../../assets/Data/Saut.jpg",im3:"../../assets/Data/courir.jpg",im4:"../../assets/Data/nager.jpg",answer: "../../assets/Data/courir.jpg" }
  ];

  constructor(private router: Router, private route: ActivatedRoute, private userProvider: LoloUserProviderService) { }

  ngOnInit() {
    this.loadWords();
  }

  loadWords(){
      var _self=this;
    	var cbError = function(error){alert(error.message);};
    	var cbSucces = function(data){
              console.log(data);
            	_self.data = data;
        };
    	this.userProvider.getLearningWords( cbSucces, cbError);
  }

  next(){
    // index for the Data ( for demo just two values (0,1) )
    this.index=Math.round(Math.random());
    alert(this.index);
  }

  check(instance,answer)
  {
    this.instance=JSON.stringify(instance);
    this.answer=JSON.stringify(answer);

if (this.instance==this.answer)
{

  alert("Correct!!");

  /// display new instance by index
  // for the demo I have two instances so the index will be 0 or 1
  this.index=Math.round(Math.random());
}
else
{
  alert("Wrong");
}
  }

}
