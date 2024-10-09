import {Injectable} from '@angular/core';
import {BehaviorSubject} from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class LoaderService {
    private loadingSubject = new BehaviorSubject<boolean>(false);
    isLoading$ = this.loadingSubject.asObservable();

    setLoading(isLoading: boolean) {
        this.loadingSubject.next(isLoading);
    }

    show(): void {
        this.setLoading(true);
    }

    hide(): void {
        this.setLoading(false);

    }
}