import {Injectable} from '@angular/core';
import {from, Observable} from 'rxjs';
import {HttpClient, HttpHeaders, HttpParams,} from '@angular/common/http';
import {environment} from "../../../environments/environment";
import {jwtDecode} from "jwt-decode";
@Injectable({
  providedIn: 'root',
})
export class HttpService {
  sessionId = '';

  constructor(
    private httpClient: HttpClient,
  ) {
  }

  get getServer() {
    return environment.apiUrl
  }

  public get<T>(url: string, params?: HttpParams | null, contentType?: string, noAuth?: boolean, fullPath?: boolean): Observable<T> {
  return from(new Promise<T>(async (resolve, reject) => {
    const headers = await this.getHeaders(contentType || 'json', noAuth || false);
    const options: any = {
      headers,
      params: params || null,
    };
    if (contentType === 'blob') {
      options['responseType'] = 'blob';
    }

    const requestUrl = (fullPath) ? url : `${this.getServer}${url}`;

    this.httpClient
      .get<T>(requestUrl, options)
      .subscribe(
        (res: any) => {
          try {
            resolve(res);
          } catch (error) {
            reject('Response parsing error');
          }
        },
        (err) => reject(err)
      );
  }));
}

  public post<T>(url: string, data: T, contentType?: string, responseType?: string): Observable<T> {
    return from(new Promise<T>(async (resolve, reject) => {
      const headers = await this.getHeaders(contentType || 'json');
      const options: any = {
        headers,
      };
      if (contentType === 'blob') {
        options['responseType'] = responseType ? responseType : 'blob';
      }
      this.httpClient
        .post<T>(`${this.getServer}${url}`, data, options)
        .subscribe(res => {
          // @ts-ignore
          resolve(res);
        }, (err) => reject(err));
    }));
  }

  public put<T>(url: string, data: T, contentType?: string): Observable<T> {
    return from(new Promise<T>(async (resolve, reject) => {
      const headers = await this.getHeaders(contentType || 'json');
      const options: any = {
        headers,
      };
      if (contentType === 'blob') {
        options['responseType'] = 'blob';
      }
      this.httpClient
        .put<T>(`${this.getServer}${url}`, data, options)
        .subscribe(res => {
          // @ts-ignore
          resolve(res);
        }, (err) => reject(err));
    }));
  }

  public patch<T>(url: string, data: T): Observable<T> {
    return from(new Promise<T>(async (resolve, reject) => {
      const headers = await this.getHeaders();
      this.httpClient
        .patch<T>(`${this.getServer}${url}`, data, {
          headers
        })
        .subscribe(res => {
          resolve(res);
        }, (err) => reject(err));
    }));
  }

  public delete<T>(url: string): Observable<T> {
    return from(new Promise<T>(async (resolve, reject) => {
      const headers = await this.getHeaders();
      this.httpClient
        .delete<T>(`${this.getServer}${url}`, {
          headers
        })
        .subscribe(res => {
          resolve(res);
        }, (err) => reject(err));
    }));
  }

  async getHeaders(type: string = 'json', noAuth: boolean = false): Promise<HttpHeaders> {
    let headers = new HttpHeaders();
    if (!noAuth) {
      const token = await this.getAuthToken();
      if (token) {
        headers = headers.set(
          'Authorization',
          `Bearer ${token}`
        );
      }
    }
    if (type === 'json') {
      headers = headers.set('Content-Type', 'application/json; charset=utf-8;');
    }
    return headers;
  }

  async getAuthToken(): Promise<string | null> {
  return new Promise(resolve => {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      const res = localStorage.getItem('access');
      if (res) {
        try {
          const tokenData = jwtDecode(res) as any;
          if (tokenData.exp >= (new Date().getTime() / 1000)) {
            resolve(res);
          } else {
            resolve(null);
          }
        } catch (e) {
          resolve(null);
        }
      } else {
        resolve(null);
      }
    } else {
      resolve(null); // Server side rendering
    }
  });
}
}
