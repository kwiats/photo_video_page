import {Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {PageConfig} from "../../core/models/media.model";
import {ApiService} from "../../core/services/api.service";
import {LoaderService} from "../../core/services/loader.service";
import {environment} from "../../../environments/environment";


@Component({
    selector: 'app-images',
    templateUrl: './images.component.html',
    styleUrls: ['./images.component.scss']
})
export class ImagesComponent {
    config: PageConfig | null = null;
    private layoutName: string = 'default';

    constructor(private route: ActivatedRoute, private apiService: ApiService,
                private loaderService: LoaderService) {
        this.layoutName = this.route.snapshot.params['title'];
    }

    ngOnInit(): void {
        this.layoutName = this.layoutName || this.route.snapshot.params['title'];
        if (this.layoutName) {
            this.initLoadData();
        }
    }

    initLoadData() {
        console.log('initLoadData')
        this.loaderService.show();
        if (this.layoutName) {
            this.apiService.fetchLayout(this.layoutName).subscribe(
                (data) => {
                    this.config = JSON.parse(data.layout);
                    console.log(this.config);
                    this.loaderService.hide()
                },
                (error) => {
                    console.error('Error fetching data:', error);
                    this.loaderService.hide()
                }
            );
        } else {
            console.error('Layout name is undefined or empty.');
        }
    }

    getUrl(url: string | undefined) {
        return environment.apiUrl.split('/api')[0] + url + '?quality=1'
    }
}
