import {Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute} from '@angular/router';
import {LoloUserProviderService} from '../lolo-user-provider.service';
import {TextToSpeech} from '@ionic-native/text-to-speech/ngx';

@Component({
    selector: 'app-learn',
    templateUrl: './learn.page.html',
    styleUrls: ['./learn.page.scss'],
})
export class LearnPage implements OnInit {

    public index: number = 0;
    public instance: any;
    public answer: any;
    public level: number;
    public data = [];
    public learningLang;
    public knownLang = "en";
    public imageDir = "../../assets/images/";

    learnedWords = [];

    constructor(private router: Router, private route: ActivatedRoute, private userProvider: LoloUserProviderService, private tts: TextToSpeech) {
    }

    ngOnInit() {
        this.getUserLanguage()
        this.loadWords();
    }

    getUserLanguage() {
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
            _self.learningLang = "fr" //if it fails the default language is french
        };
        var cbSucces = function (data) {
            console.log(data);
            _self.learningLang = data.lang
        };
        this.userProvider.getUserLanguage(cbSucces, cbError);
    }

    loadWords() {
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
        };
        var cbSucces = function (data) {
            console.log(data);
            var res = [];
            data.words.forEach((page) => {
                var temp = page.complementary;
                temp.push(page.to_learn);
                temp.sort(() => Math.random() - 0.5);
                res.push({learning: page.to_learn, words: temp});
            });
            console.log(res);
            _self.data = res;
        };
        this.userProvider.getLearningWords(cbSucces, cbError);
    }

    next() {
        // index for the Data ( for demo just two values (0,1) )
        this.index = Math.round(Math.random());
        alert(this.index);
    }

    check(instance, answer) {
        if (instance == answer) {
            alert("Correct");
            console.log(this.data.length)
            if (this.index < this.data.length) {
                var learned = {"wordID": this.data[this.index].learning._id, "lang": this.learningLang};
                this.learnedWords.push(learned);
                console.log(this.index)
                if (this.index == this.data.length - 1) {
                    //end of learning
                    var _self = this;
                    var cbError = function (error) {
                        alert(error.message);
                    };
                    var cbSucces = function (data) {
                        _self.router.navigate(['main']);
                    };
                    this.userProvider.updateLearnedWords(this.learnedWords, cbSucces, cbError);
                }

                this.index++;
            }
        }
        else {
            alert("Wrong");
        }
    }
    playText(word) {
        let lang  
        if(this.learningLang == "fr") 
          lang = 'fr-FR'
        else if (this.learningLang == "es")
            lang ='es-ES'
        else if (this.learningLang == "de")
            lang = 'de-DE'   
        this.tts.speak({
          text: word,
          locale: lang
        })
          .then(() => console.log('Success'))
          .catch((reason: any) => console.log(reason));
      }
}
