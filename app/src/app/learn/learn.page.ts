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
  public data = [];
  public learnLang = "fr";
  public knownLang = "en";
  public imageDir = "../../assets/images/"

  learnedWords = [];

  constructor(private router: Router, private route: ActivatedRoute, private userProvider: LoloUserProviderService) { }

  ngOnInit() {
    this.loadWords();
  }

  loadWords(){
      var _self=this;
    	var cbError = function(error){alert(error.message);};
    	var cbSucces = function(data){
              console.log(data);
              var res = [];
              data.words.forEach( (page) => {
                var temp = page.complementary;
                temp.push(page.to_learn);
                temp.sort(() => Math.random() - 0.5);
                res.push({learning: page.to_learn, words: temp});
              });
              console.log(res);
            	_self.data = res;
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
    if (instance==answer)
    {
      alert("Correct");
      if(this.index < this.data.length - 2){
        var learned = {"wordID": this.data[this.index].learning._id, "lang": this.learnLang};
        this.learnedWords.push(learned);
        this.index++;
      } else {
        //end of learning
        var _self = this;
        var cbError = function(error){alert(error.message);};
        var cbSucces = function(data){
              _self.router.navigate(['home']);
          };
        this.userProvider.updateLearnedWords(this.learnedWords, cbSucces, cbError);
      }
    }
    else
    {
      alert("Wrong");
    }
  }

}
