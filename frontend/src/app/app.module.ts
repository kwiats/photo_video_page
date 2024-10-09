import {CUSTOM_ELEMENTS_SCHEMA, NgModule} from '@angular/core';
import {BrowserModule, provideClientHydration} from '@angular/platform-browser';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HomeComponent} from './pages/home/home.component';
import {ImagesComponent} from './pages/images/images.component';
import {HttpClientModule, provideHttpClient, withFetch} from '@angular/common/http';
import {ImagesManagerComponent} from './pages/images-manager/images-manager.component';
import {ImageCropperModule} from 'ngx-image-cropper';
import {AngularDraggableModule} from 'angular2-draggable';
import {MediaPlayerComponent} from './components/media-player/media-player.component';
import {ToolbarComponent} from './components/toolbar/toolbar.component';
import {FontAwesomeModule} from '@fortawesome/angular-fontawesome';
import {UploadComponent} from './components/popups/upload/upload.component';
import {BrowserComponent} from './components/popups/browser/browser.component';
import {FormsModule} from "@angular/forms";
import {LoaderComponent} from './components/loader/loader.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import { TitleComponent } from './components/popups/title/title.component';

@NgModule({
    declarations: [
        AppComponent,
        HomeComponent,
        ImagesComponent,
        ImagesManagerComponent,
        MediaPlayerComponent,
        ToolbarComponent,
        UploadComponent,
        BrowserComponent,
        LoaderComponent,
        TitleComponent
    ],
    imports: [
        BrowserAnimationsModule,
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        ImageCropperModule,
        AngularDraggableModule,
        FontAwesomeModule,
        FormsModule,
    ],
    providers: [
        provideClientHydration(),
        provideHttpClient(withFetch()),
    ],
    bootstrap: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule {
}
