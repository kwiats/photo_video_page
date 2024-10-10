import {Component} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {ApiService} from "../../core/services/api.service";
import {LoaderService} from "../../core/services/loader.service";

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent {
    isDown = false;
    startX = 0;
    scrollLeft = 0;
    images: any[] = [];
    currentYear: number = new Date().getFullYear();

    constructor(private route: ActivatedRoute, private apiService: ApiService,
                private loaderService: LoaderService) {
    }

    ngOnInit(): void {
        this.loadOptions()
    }

    loadOptions() {
        this.loaderService.show();
        this.apiService.fetchAllLayouts().subscribe((data) => {
            console.log(data)
            this.images = data.results;
        }, (error) => {
            console.error('Error fetching data:', error);
            this.loaderService.hide();
        }, () => {
            this.loaderService.hide();
        })
    }

    onMouseDown(event: MouseEvent) {
        this.isDown = true;
        const slider = event.currentTarget as HTMLElement;
        this.startX = event.pageX - slider.offsetLeft;
        this.scrollLeft = slider.scrollLeft;
    }

    onMouseLeave() {
        this.isDown = false;
    }

    onMouseUp() {
        this.isDown = false;
    }

    onMouseMove(event: MouseEvent) {
        if (!this.isDown) return;
        event.preventDefault();
        const slider = event.currentTarget as HTMLElement;
        const x = event.pageX - slider.offsetLeft;
        const walk = (x - this.startX) * 2; // Scroll-fast
        slider.scrollLeft = this.scrollLeft - walk;
    }
}
