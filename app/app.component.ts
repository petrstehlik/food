import { Component } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';

import { Observable }     from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Component({
  selector: 'my-app',
  templateUrl: 'app/app.name.html'
})
export class AppComponent {
	name = 'Food agregator';
	restaurants : JSON[] = [];

	constructor (public http: Http) {};

	getRestaurants() {
		this.getRestaurant(16506890);
		this.getRestaurant(16505998);
		this.getRestaurant(16506806);
		this.getRestaurant(16506807);
		this.getRestaurant(16505905);
		this.getRestaurant(18235286);
		this.getRestaurant(16511895);
		this.getRestaurant(10000000);
	}

	getRestaurant(id : Number) {
		this.http.get('api/restaurants/' + id)
			.map(res => res.text())
			.subscribe(
				data => this.restaurants.push( JSON.parse(data) ),
				err => this.handleError(err)
			);
	}

	ngOnInit(): void {
		this.getRestaurants();
	}

	private handleError(error : Response) {
		console.log("Error");
	}
}

