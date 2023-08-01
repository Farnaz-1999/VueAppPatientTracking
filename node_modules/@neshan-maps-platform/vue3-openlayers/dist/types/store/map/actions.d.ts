import { Context } from "../store.model";
import { MapType } from "./map.model";
export declare const mapActions: {
    shakeMap: (context: Context, delay?: number) => void;
    togglePoi: (context: Context, value?: boolean) => void;
    toggleTraffic: (context: Context, value?: boolean) => void;
    setMapType: (context: Context, value: MapType) => void;
};
