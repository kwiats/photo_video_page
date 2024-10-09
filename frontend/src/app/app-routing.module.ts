import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from "./pages/home/home.component";
import {ImagesComponent} from "./pages/images/images.component";
import {ImagesManagerComponent} from "./pages/images-manager/images-manager.component";

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: ':title',
    component: ImagesComponent
  },
  {path: 'edit/:title', component: ImagesManagerComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
