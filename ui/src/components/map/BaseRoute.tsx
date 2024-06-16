import {Marker, Polyline, Popup, useMap} from "react-leaflet";
import React, {useEffect, useRef} from "react";
import {Port, Route, SimplifyRoute} from "../../api/models";
import L, {LatLngExpression} from "leaflet";
import './BaseRoute.css';
import 'leaflet.geodesic';
// import { GeodesicLine } from 'react-leaflet-geodesic';


type Props = {
    route: SimplifyRoute
}


export const GeodesicLine = (props: Props) => {
    const map = useMap();

    useEffect(() => {
        const line: LatLngExpression[] = [
            L.latLng(props.route.route[0][0], props.route.route[0][1]), // Начальная точка
            L.latLng(props.route.route[1][0], props.route.route[1][1])    // Конечная точка
        ];

        const geodesic = L.geodesic([line], {
            color: 'red',
            dashArray: "5, 5",
            dashOffset: "0",
            className: "moving-line",
            weight: 1,
            opacity: 0.5,
        }).addTo(map);

        return () => {
            map.removeLayer(geodesic);
        };
    }, [map]);

    return null;
};

const BaseRoute: React.FC<Props> = (props) => {
    const polylineRef = useRef(null);
    return (
        <Polyline
            ref={polylineRef}
            positions={props.route.route}
            color="red"
            dashArray="5, 5"
            dashOffset="0"
            className="moving-line"
            weight={1}
        />
    )
}

export default BaseRoute;