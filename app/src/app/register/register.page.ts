import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {LoloUserProviderService} from '../lolo-user-provider.service';


@Component({
    selector: 'app-register',
    templateUrl: './register.page.html',
    styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {

    firstName_V: string;
    lastName_V: string;
    email_V: string;
    languages = {};
    language_selector;

    diaplay_to_lang = {"French": "fr", "German": "de", "Spanish": "es"};

    constructor(private router: Router, private userProvider: LoloUserProviderService) {

    }

    ngOnInit() {
        this.getLanguages()
    }

    getLanguages() {
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
        };
        var cbSucces = function (data) {
            console.log(data);

            _self.languages = data
        };
        this.userProvider.getLanguages(cbSucces, cbError);
    }


    submitClick() {
        var _self = this;
        if (typeof this.firstName_V !== 'undefined' && typeof this.email_V !== 'undefined' && typeof this.lastName_V !== 'undefined' &&
            typeof this.language_selector !== 'undefined') {
            console.log(this.language_selector)
            const display = this.language_selector
            const lng = _self.diaplay_to_lang[display]
            console.log(lng)
            var cbError = function (error) {
                alert(error.message);
            };
            var cbSucces = function (data) {
                alert(data.message);
                _self.router.navigate(["main"]);
            };
            this.userProvider.doRegister(this.firstName_V, this.email_V, lng, cbSucces, cbError);
        }
        else
            alert("Fill in the blanks, please");
    }

    goBack() {
        this.router.navigate(['home']);
    }

}
