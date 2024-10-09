export interface ApiResponse<T> {
    count: number;
    next: string;
    previous: string;
    results: T[];
}

export interface MediaResponse {
    pk: string;

    title: string;
    fileType: 'image' | 'video';
    file: string;
    thumbnail: string;
    createDate: string;
    updateDate: string;
    isDeleted: boolean;
}

export interface MediaPositionResponse {
    pk: string;
    name: string;
    layout: any
    createDate: string;
    updateDate: string;
    isDeleted: boolean;
}