import {Injectable} from '@angular/core';
import {HttpService} from "./http.service";
import {Observable} from "rxjs";
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

    fetchLayout(title: string = 'default'): Observable<MediaPositionResponse> {
        return this.httpClient.get<MediaPositionResponse>(`media-positions/${title}/`);
    }

    fetchAllLayouts(): Observable<ApiResponse<MediaPositionResponse>> {
        return this.httpClient.get<ApiResponse<MediaPositionResponse>>(`media-positions/`);
    }

    uploadLayout(data: any): Observable<any> {
        const slug = data['name']
        return this.httpClient.put(`media-positions/${slug}/`, data);
    }

    uploadMedias(data: FormData): Observable<any> {
        return this.httpClient.post('upload/', data, 'multipart/form-data');
    }
}
