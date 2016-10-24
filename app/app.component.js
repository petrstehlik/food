"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var http_1 = require('@angular/http');
require('rxjs/add/operator/map');
var AppComponent = (function () {
    function AppComponent(http) {
        this.http = http;
        this.name = 'Food agregator';
        this.restaurants = [];
    }
    ;
    AppComponent.prototype.getRestaurants = function () {
        this.getRestaurant(16506890);
        this.getRestaurant(16505998);
        this.getRestaurant(16506806);
        this.getRestaurant(16506807);
        this.getRestaurant(16505905);
    };
    AppComponent.prototype.getRestaurant = function (id) {
        var _this = this;
        this.http.get('api/restaurants/' + id)
            .map(function (res) { return res.text(); })
            .subscribe(function (data) { return _this.restaurants.push(JSON.parse(data)); }, function (err) { return _this.handleError(err); });
    };
    /*extractData(res : Response) {
        let rest = res.json();
        return rest.data || { };
    }*/
    AppComponent.prototype.ngOnInit = function () {
        this.getRestaurants();
    };
    AppComponent.prototype.handleError = function (error) {
        console.log("Error");
    };
    AppComponent = __decorate([
        core_1.Component({
            selector: 'my-app',
            templateUrl: 'app/app.name.html'
        }), 
        __metadata('design:paramtypes', [http_1.Http])
    ], AppComponent);
    return AppComponent;
}());
exports.AppComponent = AppComponent;
//# sourceMappingURL=app.component.js.map