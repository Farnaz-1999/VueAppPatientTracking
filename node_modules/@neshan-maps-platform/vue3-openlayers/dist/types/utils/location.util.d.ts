import { ReverseResult } from '../store/markers/markers.model';
import { Coordinate } from 'openlayers';
import { CoordsObj } from '../components/Map.model';
/**
 * Creates the sufficent title based on result data.
 * @param data - result of neshan web search
 * @returns title
 */
export declare const getTitleFromData: (data: ReverseResult) => string;
/**
 * Get the object of location and turns it into array
 * @param loc - location object
 * @returns
 */
export declare const sanitizeLocation: (loc?: CoordsObj | undefined) => Coordinate | undefined;
/**
 * Gets the device location
 * if it was succesfull, formats it and returns
 * otherwise, sends Neshan locaton
 * @returns location array
 */
export declare const getLocation: () => Promise<Coordinate>;
/**
 * Create an object for a quick lat lng access
 */
export declare const createCoordsObject: () => {
    longitude: number;
    latitude: number;
};
/**
 * Transforms common latlng to open layers-friendly latlng
 * @param point
 * @param from
 * @param to
 * @returns points
 */
export declare const transformCoords: (point: Coordinate, from?: string, to?: string) => Coordinate;
