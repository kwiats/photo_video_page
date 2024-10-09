import {Component, ElementRef, Input, ViewChild} from '@angular/core';

@Component({
    selector: 'app-media-player',
    templateUrl: './media-player.component.html',
    styleUrl: './media-player.component.scss'
})
export class MediaPlayerComponent {
    @ViewChild('videoElement') videoElement: ElementRef | undefined;

    @Input() src: string = '';
    @Input() alt: string = '';
    @Input() type: string = 'photo';

    ngAfterViewInit() {
        if (this.type === 'video' && this.videoElement) {
            this.videoElement.nativeElement.muted = true;
        }
    }
}
