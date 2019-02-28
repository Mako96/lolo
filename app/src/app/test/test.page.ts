import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { LoloUserProviderService } from '../lolo-user-provider.service';

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
  public data = [];

  public learnLang = "fr";
  public knownLang = "en";
  public imageDir = "../../assets/images/";

  testedWords = [];

  constructor(private router: Router, private userProvider: LoloUserProviderService) { }


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
                var isImage = (page.type == 'visual' ? true : false);
                var isText = !isImage;
                res.push({isImage: isImage, isText: isText, type: page.type, test: page.to_learn, words: temp});
              });
              console.log(res);
            	_self.data = res;
        };
    	this.userProvider.getTestingWords( cbSucces, cbError);
  }

  checkAnswer(instance,answer)
  {
    var correct = false;
    if (instance==answer){
      alert("Correct");
      correct = true;
    } else {
      alert("False, the correct answer was " + this.data[this.index].test.fr)
    }

    if(this.index < this.data.length - 2){
      var tested = {"wordID": this.data[this.index].test._id, "success": correct, "type": this.data[this.index].type, "lang": this.learnLang};
      this.testedWords.push(tested);
      this.index++;
    } else {
      //end of learning
      var _self = this;
      var cbError = function(error){alert(error.message);};
      var cbSucces = function(data){
            _self.router.navigate(['main']);
        };
      this.userProvider.updateTestedWords(this.testedWords, cbSucces, cbError);
    }
  }

}
