import {Component, EventEmitter, Input, Output} from '@angular/core';
import {faAdd, faEdit, faImage, faRedo, faSave, faTrash} from "@fortawesome/free-solid-svg-icons";

@Component({
    selector: 'app-toolbar',
    templateUrl: './toolbar.component.html',
    styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent {
    toolbarOpen: boolean = false;
    @Input() toolbarOptions: any[] = [];
    @Output() toolbarToggled = new EventEmitter<boolean>();

    toggleToolbar() {
        this.toolbarOpen = !this.toolbarOpen;
        this.toolbarToggled.emit(this.toolbarOpen);
    }

    doSomething(option: string) {
        console.log(`${option} clicked!`);
    }

    protected readonly faAdd = faAdd;
    protected readonly faSave = faSave;
    protected readonly faTrash = faTrash;
    protected readonly faRedo = faRedo;
    protected readonly faEdit = faEdit;
    protected readonly faImage = faImage;

    callback(func: any) {
        func()
    }
}