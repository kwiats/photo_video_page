import {Component, EventEmitter, Input, Output} from '@angular/core';

@Component({
  selector: 'app-popup-title',
  templateUrl: './title.component.html',
  styleUrl: './title.component.scss'
})
export class TitleComponent {
  @Input() title: any = '';
    @Output() close = new EventEmitter<boolean>();
    @Output() changedTitle = new EventEmitter<string>();

  saveTitle() {
    this.changedTitle.emit(this.title)
    this.closePopup()
  }

   closePopup() {
      this.close.emit(true)
    }
}
