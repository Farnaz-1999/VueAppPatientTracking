import { MapType, OlMap, ViewType } from "./map.model";
export declare const mapState: {
    mapContainer: HTMLDivElement | null;
    map: OlMap | null;
    mapType: MapType;
    zoom: number;
    poiLayer: boolean;
    trafficLayer: boolean;
    viewType: ViewType;
    scale: number;
};
