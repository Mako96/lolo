import {Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute} from '@angular/router';
import {NavController} from '@ionic/angular';

import {LoloUserProviderService} from '../lolo-user-provider.service';


@Component({
    selector: 'app-preferences',
    templateUrl: './preferences.page.html',
    styleUrls: ['./preferences.page.scss'],
})
export class PreferencesPage implements OnInit {
    firstName: string;
    lastName: string;
    email: string;

    constructor(private userProvider: LoloUserProviderService, private router: Router, private navCtrl: NavController, private route: ActivatedRoute) {
    }

    ngOnInit() {
        this.loadTopics();
    }

    loadTopics() {
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
        };
        var cbSucces = function (data) {
            console.log(data);
            var res = [];
            data.topics.forEach((topic) => {
                res.push({val: topic.name, isChecked: false, img: '../../assets/images/' + topic.image});
            });
            console.log(res);
            _self.form = res;
            _self.loadUserPrefs();
        };
        this.userProvider.getTopics(cbSucces, cbError);
    }

    loadUserPrefs() {
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
        };
        var cbSucces = function (data) {
            console.log(data);
            // this can probably be done more performant manner
            data.preferences.forEach((pref) => {
                _self.form.forEach((topic) => {
                    if (pref == topic.val) {
                        topic.isChecked = true;
                    }
                });
            });
        };
        this.userProvider.getPreferences(cbSucces, cbError);
    }

    buttonClick(item) {
        alert(item);
    }

    public form = [
        {val: 'Animals', isChecked: false, img: "../../assets/images/topics/animals.jpg"},
        {val: 'Colors', isChecked: false, img: "../../assets/images/topics/colors.jpg"},
        {val: 'fruits', isChecked: true, img: "../../assets/images/topics/fruits.jpg"},
        {val: 'Sports', isChecked: false, img: "../../assets/images/topics/sports.jpg"},
        {val: 'Stationery', isChecked: false, img: "../../assets/images/topics/Stationery.jpg"},
        {val: 'Clothes', isChecked: false, img: "../../assets/images/topics/cloth.jpg"}
    ];

    ConfirmClick(data) {

        var prefs = [];
        this.form.forEach((topic) => {
            if (topic.isChecked) {
                prefs.push(topic.val);
            }
        });
        console.log(prefs);
        var _self = this;
        var cbError = function (error) {
            alert(error.message);
        };
        var cbSucces = function (data) {
            alert(data.message);
            _self.router.navigate(["main"]);
        };

        this.userProvider.setPreferences(prefs, cbSucces, cbError);


// there we should save the data in the server ////////////////

    }
}
