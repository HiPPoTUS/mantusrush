
export interface Port {
    port_id: number;
    name: string;
    coordinates: string;
}

export interface Ship {
    ship_id: number;
    name: string;
    type?: string; // type может быть null, поэтому мы используем необязательное свойство
    description?: string; // description может быть null, поэтому мы используем необязательное свойство
    max_speed: number;
    ice_class: number;
}

export interface ShipRequest {
    ship_id?: number;
    name: string;
    max_speed: number;
    ice_class: number;
}

export interface Route {
    route_id: number;
    ship_id: number;
    start_point: number;
    end_point: number;
    start_time: Date;
    arrival_time?: Date; // arrival_time может быть null
}

export interface RouteRequest {
    ship_id: number;
    start_point_idx: number;
    end_point_idx: number;
    start_time: Date;
}

export interface SimplifyRoute {
    route_id: number;
    ship_id: number;
    route: [[number, number], [number, number]];
    start_time: Date;
    arrival_time?: Date; // arrival_time может быть null
}

export interface CurrentRoute {
    current_route_id: number;
    route_id: number;
    waypoint: string;
    waypoint_time: Date;
}

export interface PredictedRoute {
    predicted_route_id: number;
    route_id: number;
    waypoint: string;
    waypoint_time: Date;
}