import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute} from '@angular/router';
import {LoloUserProviderService} from '../lolo-user-provider.service';
import {SpeechRecognition} from "@ionic-native/speech-recognition/ngx";
import { ToastController } from '@ionic/angular';

@Component({
    selector: 'app-test',
    templateUrl: './test.page.html',
    styleUrls: ['./test.page.scss'],
})
export class TestPage implements OnInit {

    public preferences: any;
    public level: number;
    public index: number = 0;

    // these boolean values "image, text" helps to switch to the correct formula for presenting the data e.g. if the if the tested data is
    // image so image is true otherwise it's false
    image = false;
    text = true;
    public data = [];

    public learningLang;
    public knownLang = "en";
    public imageDir = "../../assets/images/";

    testedWords = [];

    pronunciationResult = false;

    public resultPageDisplay = false;

    public correctWords = 0;
    public totalWords = 0;

    constructor(private router: Router, private userProvider: LoloUserProviderService,
                private speechRecognition: SpeechRecognition, private cd: ChangeDetectorRef,private toastController: ToastController) {
    }


    ngOnInit() {
      this.resultPageDisplay = false;
      this.correctWords = 0;
      this.totalWords = 0;
        this.getUserLanguage();
        this.loadWords();
    }

    getUserLanguage() {
        var _self = this;
        var cbError = (error) => {
            this.presentToast(error.message)
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
        var cbError = (error) => {
            this.presentToast(error.message)
        };
        var cbSucces = function (data) {
            console.log(data);
            var res = [];
            data.words.forEach((page) => {
                var temp = page.complementary;
                temp.push(page.to_learn);
                temp.sort(() => Math.random() - 0.5);
                //(page.type == 'visual' ? true : false);
                var isImage = page.type == 'visual';
                var isText = page.type == 'written';
                var isSentence = page.type == 'sentence';
                res.push({
                    type: page.type,
                    test: page.to_learn,
                    words: temp,
                    sentencePos: page.sentence_index
                });
            });
            console.log(res);
            _self.data = res;
        };
        this.userProvider.getTestingWords(cbSucces, cbError);
    }

    checkAnswer(instance, answer) {
        var correct = false;
        if (instance == answer) {
            this.presentCorrectToast("Correct")
            correct = true;
        } else {
            this.presentIncorrectToast("False, the correct translation of " + this.data[this.index].test.en["word"] +
            " is " + this.data[this.index].test[this.learningLang]["word"])
            // alert("False, the correct translation of " + this.data[this.index].test.en["word"] +
            //     " is " + this.data[this.index].test[this.learningLang]["word"])
        }

        this.saveAndGoNext(correct)

    }

    saveAndGoNext(correct) {
        if (this.index < this.data.length) {
            var tested = {
                "wordID": this.data[this.index].test._id,
                "success": correct,
                "type": this.data[this.index].type,
                "lang": this.learningLang
            };
            this.testedWords.push(tested);
            if (this.index == this.data.length - 1) {
                //end of test
                var _self = this;
                var cbError = (error) => {
                    _self.presentToast(error.message)
                };
                var cbSucces = function (data) {
                  console.log(data);
                    _self.showResultPage(_self);
                };
                this.userProvider.updateTestedWords(this.testedWords, cbSucces, cbError);
            } else {
              this.index++;
            }

        }
    }

    showResultPage(_self) {
        _self.correctWords = 0;
        _self.totalWords = _self.testedWords.length;
        _self.testedWords.forEach( function(word){
          if(word.success){
            _self.correctWords++;
          }
        });
        _self.resultPageDisplay = true;
    }

    goMain() {
      this.router.navigate(['main'])
    }

    // FOR PRONUNCIATION TEST
    getPermission() {
        this.speechRecognition.hasPermission()
            .then((hasPermission) => {
                if (!hasPermission) {
                    this.speechRecognition.requestPermission();
                }
            });
    }

    startRecording(word) {

        console.log("starting")

        let lang
        if (this.learningLang == "fr")
            lang = 'fr-FR'
        else if (this.learningLang == "es")
            lang = 'es-ES'
        else if (this.learningLang == "de")
            lang = 'de-DE'

        let options = {
            language: lang
        }
        this.speechRecognition.startListening(options).subscribe(matches => {
            this.pronunciationResult = false;
            if (matches.includes(word)) {
                this.pronunciationResult = true;
            }
        });
    }

    confirmPronunciation() {
        if (this.pronunciationResult) {
            this.presentCorrectToast("Correct")
        } else {
            this.presentIncorrectToast("Wrong Pronunciation")
        }
        this.saveAndGoNext(this.pronunciationResult)

    }

    async presentToast(message) {
        let toast = await this.toastController.create({
          message: message,
          duration: 2500,
        });
        toast.present();
      }

      async presentCorrectToast(message) {
        let toast = await this.toastController.create({
          message: message,
          duration: 1500,
          position: 'bottom',
          animated:true,
          cssClass:"correct-toast",
        });
        toast.present();
      }

      async presentIncorrectToast(message) {
        let toast = await this.toastController.create({
          message: message,
        //   duration: 2500,
          showCloseButton: true,
          position: 'bottom',
          closeButtonText: 'OK',
          animated:true,
          cssClass:"incorrect-toast",
        }).then((toast) => {toast.present();});
        
      }

}
