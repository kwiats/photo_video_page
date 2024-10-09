import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {PageConfig} from "../../core/models/media.model";


@Component({
    selector: 'app-images',
    templateUrl: './images.component.html',
    styleUrls: ['./images.component.scss']
})
export class ImagesComponent implements OnInit {
    config: PageConfig | null = null;

    constructor(private route: ActivatedRoute, private http: HttpClient) {
    }

    ngOnInit(): void {
        this.route.paramMap.subscribe(params => {
            const title = params.get('title');
            if (title) {
                // this.fetchPageConfig(title).subscribe(config => {
                //   this.config = config;
                // });
                this.config = {
                    "title": {
                        "text": "Example Title",
                        "backgroundUrl": "assets/images/Print.jpg",
                        "backgroundColor": "#ff0000",
                        "x": 100, "y": 50,
                        "size": "48px",
                        "opacity": 0.8,
                        "fontFamily": "Arial, sans-serif",
                        "fontWeight": "bold",
                        "color": "#ffffff"
                    },
                    "media": [
                        {
                            "pk": '844884',
                            "src": "assets/images/Print.jpg",
                            "x": 50,
                            "y": 150,
                            "width": 300,
                            "height": 200,
                            "opacity": 0.9
                        },
                        {
                            "pk": '1234123',
                            "src": "assets/images/Print.jpg",
                            "x": 200,
                            "y": 450,
                            "width": 400,
                            "height": 300,
                            "opacity": 0.7
                        },
                        {
                            "pk": '12313131',
                            "src": "assets/images/example.mp4",
                            "type": 'video',
                            "x": 20,
                            "y": 450,
                            "width": 400,
                            "height": 300,
                            "opacity": 0.7
                        }],
                    "backgroundUrl": "assets/images/Print.jpg",
                    "backgroundRepeat": true,
                    "textVisible": true
                }

            }
        });
    }

    fetchPageConfig(title: string): Observable<PageConfig> {
        return this.http.get<PageConfig>(`/api/config/${title}`);
    }

    isValidUrl(url: string): boolean {
        try {
            new URL(url);
            return true;
        } catch (_) {
            return false;
        }
    }
}
