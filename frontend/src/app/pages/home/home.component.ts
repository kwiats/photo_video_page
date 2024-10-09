import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  isDown = false;
  startX = 0;
  scrollLeft = 0;

  images = [
    {
      src: 'https://placehold.co/600x400',
      title: 'Title 1',
      routerLink: '/route1'
    },
    {
      src: 'https://placehold.co/500x400',
      title: 'Title 2',
      routerLink: '/route2'
    },
    {
      src: 'https://placehold.co/600x700',
      title: 'Title 3',
      routerLink: '/route3'
    },
    {
      src: 'https://placehold.co/100x400',
      title: 'Title 4',
      routerLink: '/route4'
    }
    // Add more images as needed
  ];

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
