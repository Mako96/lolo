import {Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute} from '@angular/router';
import {LoloUserProviderService} from '../lolo-user-provider.service';

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

    constructor(private router: Router, private userProvider: LoloUserProviderService) {
    }


    ngOnInit() {
        this.getUserLanguage();
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
                //(page.type == 'visual' ? true : false);
                var isImage = page.type == 'visual';
                var isText = page.type == 'written';
                var isSentence = page.type == 'sentence';
                res.push({
                    isImage: isImage,
                    isText: isText,
                    isSentence: isSentence,
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
            alert("Correct");
            correct = true;
        } else {
            alert("False, the correct translation of " + this.data[this.index].test.en["word"] +
                " is " + this.data[this.index].test[this.learningLang]["word"])
        }

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
                var cbError = function (error) {
                    alert(error.message);
                };
                var cbSucces = function (data) {
                    _self.router.navigate(['main']);
                };
                this.userProvider.updateTestedWords(this.testedWords, cbSucces, cbError);
            }

            this.index++;
        }
    }

}
