import { inlineSvgs, defaultIcons } from ".";
export declare type RouteTypes = keyof typeof inlineSvgs;
export declare type CategoryName = keyof typeof defaultIcons;
export declare interface Icon {
    d: string;
    color?: string;
    size?: number;
    scale?: number;
}
