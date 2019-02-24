import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-test',
  templateUrl: './test.page.html',
  styleUrls: ['./test.page.scss'],
})
export class TestPage implements OnInit {

  public preferences:any;
  public level:number;
  public index:number=0;

  // these boolean values "image, text" helps to switch to the correct formula for presenting the data e.g. if the if the tested data is
  // image so image is true otherwise it's false 
  image=false;
  text=true;
  public data = [
    { word: 'Bleu', v1:'Blue', v2:'Red',  v3:'Green', v4:'Orange',answer: 'Blue'},
    { word: "../../assets/Data/courir.jpg", v1:'marche', v2:'Saut',  v3:'courir', v4:'nager',answer:'courir'}
  ];
  constructor(private router: Router) { }


  ngOnInit() {

  }

  checkAnswer(value,answer)
  {
    //update the index
    this.index=1;



    if(this.data[this.index].word.includes("assets"))
    {
      this.image=true;
      this.text=false;
    }
    else
    {
      this.image=false;
      this.text=true;
    }

    if(value==answer)
    {
    alert("Correct");

    }
    else{
      alert("wrong");
    }
  }

}
