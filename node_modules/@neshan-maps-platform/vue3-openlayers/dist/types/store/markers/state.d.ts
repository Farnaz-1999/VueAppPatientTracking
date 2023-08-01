import { Coordinate } from "openlayers";
import { ReverseResult, SearchItem, SelectedMarker } from "./markers.model";
export declare const markersState: {
    selectedMarker: SelectedMarker;
    mainMarker: import("openlayers").layer.Vector | null;
    mainMarkerCoords: Coordinate | null;
    reverseResult: ReverseResult | null;
    searchMarkers: import("openlayers").layer.Vector | null;
    searchResults: SearchItem[];
};
