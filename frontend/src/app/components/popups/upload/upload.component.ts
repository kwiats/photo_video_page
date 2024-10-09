import {Component, EventEmitter, Output} from '@angular/core';
import {ApiService} from "../../../core/services/api.service";
import {LoaderService} from "../../../core/services/loader.service";

@Component({
    selector: 'app-popup-upload',
    templateUrl: './upload.component.html',
    styleUrl: './upload.component.scss'
})
export class UploadComponent {
    files: File[] = [];
    @Output() close = new EventEmitter<boolean>();

    constructor(private apiService: ApiService, private loaderService: LoaderService) {
    }

    onFileDropped(event: any) {
        this.prepareFilesList(event);
    }

    fileBrowseHandler(files: any) {
        this.prepareFilesList(files.target.files);
    }

    async uploadFiles() {
        this.loaderService.show();
        if (this.files.length === 0) {
            console.log('No files selected');
            return;
        }

        const formData = new FormData();

        for (let file of this.files) {
            formData.append('files', file, file.name);
        }
        try {
            await this.apiService.uploadMedias(formData).toPromise();
        } catch (error) {
            console.error(error);
        } finally {
            this.loaderService.hide();
            this.closePopup()
        }

    }

    prepareFilesList(files: Array<any>) {
        for (const item of files) {
            this.files.push(item);
        }
    }

    closePopup() {
        this.close.emit(true)
    }

    preventDefault($event: DragEvent) {

    }
}
