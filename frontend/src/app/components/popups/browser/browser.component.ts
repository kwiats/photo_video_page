import {Component, EventEmitter, Input, Output} from '@angular/core';
import {ActionBrowser, MediaItem} from "../../../core/models/media.model";
import {environment} from "../../../../environments/environment";


@Component({
    selector: 'app-popup-browser',
    templateUrl: './browser.component.html',
    styleUrl: './browser.component.scss'
})
export class BrowserComponent {
    @Input() mediaItems: MediaItem[] = [];
    @Input() multiple: boolean = true;
    selectedMedia: MediaItem | null = null;
    selectedItems: MediaItem[] = [];
    @Output() close = new EventEmitter<boolean>();
    @Output() select = new EventEmitter<ActionBrowser[]>();

    constructor() {
    }

    ngOnInit(): void {

    }


    openMediaViewer(item: MediaItem): void {
        this.selectedMedia = item;
    }

    getUrl(url: string) {
        return environment.apiUrl.split('/api')[0] + url
    }

    closeMediaViewer(): void {
        this.selectedMedia = null;
    }

    closePopup() {
        this.close.emit(true)
    }

    updateSelectedItems(item: MediaItem): void {
        if (this.multiple) {
            this.selectedItems = this.mediaItems.filter((item) => item.selected);
        } else {
            this.mediaItems.forEach((mediaItem) => {
                if (mediaItem.pk !== item.pk) {
                    mediaItem.selected = false;
                }
            });

            this.selectedItems = this.mediaItems.filter((item) => item.selected);
        }
    }

    addSelectedItems(): void {
        this.emitValue('selected', this.selectedItems);
        this.clearSelection();
    }

    deleteSelectedItems(): void {
        this.emitValue('deleted', this.selectedItems);

        this.mediaItems = this.mediaItems.filter(item => !item.selected);
        this.selectedItems = [];
    }


    emitValue(action: 'deleted' | 'selected' | 'closed', data: MediaItem[]){
       // @ts-ignore
        this.select.emit({action: action, data: data});
        this.closePopup();
    }

    clearSelection(): void {
        this.mediaItems.forEach(item => item.selected = false);
        this.selectedItems = [];
    }
}
