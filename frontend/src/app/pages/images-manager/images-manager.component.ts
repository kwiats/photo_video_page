import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {forkJoin} from 'rxjs';
import {MediaConfig, MediaItem, PageConfig, TitleConfig} from "../../core/models/media.model";
import {faAdd, faEdit, faImage, faRedo, faSave, faTrash} from "@fortawesome/free-solid-svg-icons";
import {ApiService} from "../../core/services/api.service";
import {MediaResponse} from "../../core/models/response.model";
import {LoaderService} from "../../core/services/loader.service";
import {environment} from "../../../environments/environment";


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

    constructor(
        private cdr: ChangeDetectorRef,
        private route: ActivatedRoute,
        private apiService: ApiService,
        private loaderService: LoaderService
    ) {
    }


    ngOnInit(): void {
        console.log('ngOnInit')
        this.initLoadData();
    }

    initLoadData() {
        this.loaderService.show();
        forkJoin({
            images: this.apiService.getAllImages(),
            layout: this.apiService.fetchLayout('example laylout')
        }).subscribe((data) => {
            this.medias = data.images.results.map(this.convertMediaResponseToMediaItem);
            this.config = JSON.parse(data.layout.results[0].layout);
            console.log(data.layout)
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

    exmplConfig() {
        this.route.paramMap.subscribe(params => {
            const title = params.get('title');
            if (title) {
                this.config = {
                    "title": {
                        "text": "Example Title",
                        "backgroundUrl": "assets/images/Print.jpg",
                        "backgroundColor": "#ff0000",
                        "x": 100,
                        "y": 50,
                        "size": "48px",
                        "opacity": 0.8,
                        "fontFamily": "Arial, sans-serif",
                        "fontWeight": "bold",
                        "color": "#ffffff"
                    },
                    "media": [
                        {
                            "pk": "1",
                            "src": "assets/images/example.mp4",
                            "type": "video",
                            "x": 50,
                            "y": 150,
                            "width": 300,
                            "height": 200,
                            "opacity": 0.9
                        },
                        {
                            "pk": "2",
                            "src": "assets/images/Print.jpg",
                            "x": 200,
                            "y": 450,
                            "width": 400,
                            "height": 300,
                            "opacity": 0.7
                        }
                    ],
                    "backgroundUrl": "assets/images/Print.jpg",
                    "backgroundRepeat": true,
                    "textVisible": true
                }
                // this.fetchPageConfig(title).subscribe(config => {
                //   this.config = config;
                // });
            }
        });
    }


    onDragEnd(event: any, item: MediaConfig | TitleConfig) {
        item.x = event.x;
        item.y = event.y;
    }

    async onSave() {
        if (this.config) {
            console.log(JSON.stringify(this.config))
            let data = {
                name: 'example laylout',
                layout: JSON.stringify(this.config)
            }
            try {

                await this.apiService.uploadLayout(data).toPromise()
            } catch (e) {
                console.log(e)
            }

        }
    }

    onCropImage(event: any) {
        if (this.selectedImage) {
            this.selectedImage.src = event.base64;
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
            console.log(this.resizingItem.x, this.resizingItem.y, this.resizingItem.width, this.resizingItem.height)
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
        console.log($event)
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
                console.log('deleted')
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
                console.log('closed')
                break
        }
        this.cdr.detectChanges();
        console.log(this.config)

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
}
