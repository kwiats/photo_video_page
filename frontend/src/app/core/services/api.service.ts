import {Injectable} from '@angular/core';
import {HttpService} from "./http.service";
import {Observable} from "rxjs";
import {PageConfig} from "../models/media.model";
import {ApiResponse, MediaPositionResponse, MediaResponse} from "../models/response.model";

@Injectable({
    providedIn: 'root'
})
export class ApiService {

    constructor(
        private httpClient: HttpService,
    ) {
    }

    getAllImages(): Observable<ApiResponse<MediaResponse>> {
        return this.httpClient.get<ApiResponse<MediaResponse>>('images/')
    }

    fetchLayout(title: string): Observable<ApiResponse<MediaPositionResponse>> {
        return this.httpClient.get<ApiResponse<MediaPositionResponse>>(`media-positions/?name=${title}`);
    }

    uploadLayout(data: any): Observable<any> {
        return this.httpClient.post('media-positions/', data);
    }

    uploadMedias(data: FormData): Observable<any> {
        return this.httpClient.post('upload/', data, 'multipart/form-data');
    }
}
