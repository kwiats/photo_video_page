import { Component } from '@angular/core';
import { LoaderService } from '../../core/services/loader.service';
import { animate, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.scss'],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('300ms', style({ opacity: 1 })),
      ]),
      transition(':leave', [animate('300ms', style({ opacity: 0 }))]),
    ]),

  ],
})
export class LoaderComponent {
  isLoading$ = this.loaderService.isLoading$;

  constructor(private loaderService: LoaderService) {}
}