import { Map } from "openlayers";
export declare interface OlMap extends Map {
    setMapType(value: MapType): void;
    switchPoiLayer(value: boolean): void;
    switchTrafficLayer(value: boolean): void;
}
export declare type MapType = "neshan" | "dreamy" | "dreamy-gold" | "standard-night" | "standard-day" | "osm-bright";
export declare type ViewType = undefined | 'desktop' | 'mobile';
