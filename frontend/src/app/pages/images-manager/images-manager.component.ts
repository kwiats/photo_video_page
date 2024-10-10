import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {forkJoin} from 'rxjs';
import {MediaConfig, MediaItem, PageConfig, TitleConfig} from "../../core/models/media.model";
import {faAdd, faEdit, faImage, faRedo, faSave, faTrash} from "@fortawesome/free-solid-svg-icons";
import {ApiService} from "../../core/services/api.service";
import {MediaResponse} from "../../core/models/response.model";
import {LoaderService} from "../../core/services/loader.service";
import {environment} from "../../../environments/environment";
import {IPosition} from "angular2-draggable";


@Component({
    selector: 'app-images-manager',
    templateUrl: './images-manager.component.html',
    styleUrls: ['./images-manager.component.scss']
})
export class ImagesManagerComponent implements OnInit {
    faTrash = faTrash;
    faAdd = faAdd;
    faSave = faSave;
    faRedo = faRedo;
    faEdit = faEdit;
    faImage = faImage;

    config: PageConfig = {media: []};
    selectedImage: MediaConfig | null = null;
    isResizing: boolean = false;
    resizingItem: MediaConfig | null = null;
    private initialWidth: number = 0;
    private initialHeight: number = 0;
    private initialMouseX: number = 0;
    private initialMouseY: number = 0;
    private initialX: number = 0;
    private initialY: number = 0;
    openToolbar: boolean = false;
    defaultLayout: any = {
        x: 50,
        y: 150,
        width: 300,
        height: 200,
        opacity: 0.9,
    };
    toolbarOptions: any[] = [
        {
            icon: faAdd,
            label: 'Dodaj media',
            callback: () => this.openUploadPopup()
        },
        {
            icon: faImage,
            label: 'Pokaż media',
            callback: () => this.openBrowserPopup()
        },
        {
            icon: faRedo,
            label: 'Zresetuj widok',
            callback: () => this.initLoadData()
        },
        {
            icon: faTrash,
            label: 'Usuń wszystkie media',
            action: 'delete'
        },
        {
            icon: faEdit,
            label: 'Edytuj tło',
            callback: () => this.openBrowserPopup(false)
        },
        {
            icon: faEdit,
            label: 'Edytuj tytuł',
            callback: () => this.openTitlePopup()
        },
        {
            icon: faSave,
            label: 'Zapisz widok',
            callback: () => this.onSave()
        }
    ]
    medias: MediaItem[] = [];
    multiSelect: boolean = true;
    private layoutName: string = '';

    constructor(
        private cdr: ChangeDetectorRef,
        private route: ActivatedRoute,
        private apiService: ApiService,
        private loaderService: LoaderService
    ) {
        this.layoutName = this.route.snapshot.params['title'];
    }


    ngOnInit(): void {
        if (this.layoutName) {
            this.initLoadData();
        } else {
            this.layoutName = this.route.snapshot.params['title'];
            this.initLoadData()
        }
    }

    initLoadData() {
        this.loaderService.show();
        forkJoin({
            images: this.apiService.getAllImages(),
            page: this.apiService.fetchLayout(this.layoutName)
        }).subscribe((data) => {
            this.medias = data.images.results.map(this.convertMediaResponseToMediaItem);
            this.config = JSON.parse(data.page.layout);
            this.cdr.detectChanges();
        }, (error) => {
            console.error('Error fetching data:', error);
            this.loaderService.hide();
        }, () => {
            this.loaderService.hide();
        });
    }

    loadMedias() {
        this.loaderService.show();
        this.apiService.getAllImages().subscribe((data) => {
            this.medias = data.results.map(this.convertMediaResponseToMediaItem);
        }, (error) => {
            console.error('Error fetching data:', error);
            this.loaderService.hide();
        }, () => {
            this.loaderService.hide();
        });
    }


    convertMediaResponseToMediaItem(response: MediaResponse): MediaItem {
        return {
            pk: response.pk,
            type: response.fileType,
            url: response.file,
            thumbnailUrl: response.thumbnail,
            name: response.title,
            selected: false,
        };
    }

    onDrag(event: IPosition, media: MediaConfig,) {
        const centerX = event.x + event.x / 2;
        const centerY = event.y;

    }

    onDragEnd(event: any, item: MediaConfig | TitleConfig, type: string) {
        const centerX = event.x;
        const centerY = event.y;

        switch (type) {
            case 'media':
                const index = this.config.media.findIndex(mediaItem => mediaItem === item);
                if (index !== -1) {
                    this.config.media[index].x = centerX;
                    this.config.media[index].y = centerY;
                }
                break;
            case 'title':
                if (this.config && this.config.title) {
                    this.config.title.x = centerX;
                    this.config.title.y = centerY;
                }
                break;
        }
    }

    async onSave() {
        if (this.config) {
            let data = {
                name: this.layoutName,
                layout: JSON.stringify(this.config)
            }
            this.loaderService.show();
            try {
                await this.apiService.uploadLayout(data).toPromise()
                this.loaderService.hide();
            } catch (e) {
                console.log(e)
                this.loaderService.hide();
            }

        }
    }


    onSelectMedia(image: MediaConfig) {
        this.selectedImage = image;
    }

    startResizing(event: MouseEvent, item: MediaConfig) {
        this.isResizing = true;
        this.resizingItem = item;
        this.initialWidth = item.width;
        this.initialHeight = item.height;
        this.initialMouseX = event.clientX;
        this.initialMouseY = event.clientY;

        this.initialX = item.x
        this.initialY = item.y

        document.addEventListener('mousemove', this.resizeImage.bind(this));
        document.addEventListener('mouseup', this.stopResizing.bind(this));
    }

    resizeImage(event: MouseEvent) {
        if (this.isResizing && this.resizingItem) {
            const deltaX = event.clientX - this.initialMouseX;
            const deltaY = event.clientY - this.initialMouseY;

            this.resizingItem.width = this.initialWidth + deltaX;
            this.resizingItem.height = this.initialHeight + deltaY;
            this.resizingItem.x = this.initialX + deltaX / 2
            this.resizingItem.y = this.initialY + deltaY / 2
        }
    }

    stopResizing() {
        this.isResizing = false;
        this.resizingItem = null;

        document.removeEventListener('mousemove', this.resizeImage.bind(this));
        document.removeEventListener('mouseup', this.stopResizing.bind(this));
    }


    toolbarToggled($event: boolean) {
        this.openToolbar = $event;
    }

    deleteMedia(media: MediaConfig) {
        if (this.config) {
            this.config.media = this.config.media?.filter(item => item.pk !== media.pk);
        }

    }

    showUploadPopup: boolean = false;
    showBrowserPopup: boolean = false;
    showTitlePopup: boolean = false;

    private openUploadPopup() {
        this.showUploadPopup = true
    }

    private openBrowserPopup(multiSelect: boolean = true) {
        this.loadMedias();
        this.multiSelect = multiSelect;
        this.showBrowserPopup = true
    }

    closeUploadPopup() {
        this.showUploadPopup = false;
    }

    closeBrowserPopup() {
        this.showBrowserPopup = false;
    }

    browserSelected(items: any) {
        switch (items.action) {
            case 'deleted':
                break;
            case 'selected':
                if (this.multiSelect) {

                    this.config = {
                        ...this.config,
                        media: [...this.config.media, ...items.data.map(this.parseMediaItems.bind(this))],
                    };
                } else {
                    this.config = {
                        ...this.config,
                        backgroundRepeat: true,
                        backgroundUrl: items.data[0].url,
                    };
                }
                break;
            case 'closed':

                break
        }
        this.cdr.detectChanges();

    }

    getUrl(url: string | undefined) {
        return environment.apiUrl.split('/api')[0] + url
    }

    parseMediaItems(item: MediaItem): any {

        return {
            pk: item.pk,
            src: item.url,
            type: item.type,
            ...this.defaultLayout,
        }

    }

    openTitlePopup() {
        this.showTitlePopup = true
    }

    changeTitle(title: string) {
        if (this.config && this.config.title) {
            this.config.title.text = title

        } else {
            this.config = {
                ...this.config,
                title: {
                    text: title,
                    backgroundUrl: "assets/images/Print.jpg",
                    backgroundColor: "#ff0000",
                    x: 100,
                    y: 50,
                    size: "48px",
                    opacity: 0.8,
                    fontFamily: "Arial, sans-serif",
                    fontWeight: "bold",
                    color: "#ffffff"
                }
            }
        }
        this.config.textVisible = true
        this.cdr.detectChanges();


    }

    closeTitlePopup() {
        this.showTitlePopup = false
    }


    getMediaStyle(media: MediaConfig) {
        return {
            'width.px': media.width,
            'height.px': media.height,
            'opacity': 1,
            'position': 'absolute',
            'transform': `translate(${media.x}px, ${media.y}px)`
        };
    }
}
