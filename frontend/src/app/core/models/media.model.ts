export interface MediaConfig {
    pk: string;
    src: string;
    x: number;
    y: number;
    type?: string;
    width: number;
    height: number;
    opacity: number;
}

export interface TitleConfig {
  text: string;
  backgroundUrl?: string;
  backgroundColor?: string;
  x: number;
  y: number;
  size: string;
  opacity: number;
  fontFamily: string;
  fontWeight: string;
  color: string;
}

export interface PageConfig {
    title?: TitleConfig;
    media: MediaConfig[];
    backgroundUrl?: string;
    backgroundRepeat?: boolean;
    textVisible?: boolean;
}

export interface MediaItem {
    pk: string;
    type: 'image' | 'video';
    url: string;
    thumbnailUrl?: string;
    name: string;
    selected: boolean;
}

export interface ActionBrowser{
    action: 'deleted' | 'selected';
    data: MediaItem[];
}
