import React, {useEffect, useState} from 'react';
import {MapContainer, TileLayer} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import {getPorts, getShips, getSimplifyRoutes} from "../../api";
import {Port, Ship, SimplifyRoute} from "../../api/models";
import PortMarker from "./PortMarker";
import {GeodesicLine} from "./BaseRoute";
import {useDispatch, useSelector} from "react-redux";
import {RootState, AppDispatch} from "../../store";
import {addPorts, emptyPorts} from "../../store/portsSlice";
import {addRoutes, emptyRoutes} from "../../store/routesSlice";
import {addShips, emptyShips} from "../../store/shipsSlice";


const Map: React.FC = () => {
    const portsStore = useSelector((state: RootState) => state.ports);
    const routesStore = useSelector((state: RootState) => state.routes);
    const dispatch = useDispatch<AppDispatch>();
    const [ports, setPorts] = useState<Port[]>([])
    const [routes, setRoutes] = useState<SimplifyRoute[]>([])
    const [ships, setShips] = useState<Ship[]>([])
    useEffect(() => {
        getPorts()
            .then(data => {
                setPorts(data);
                dispatch(emptyPorts([]))
                dispatch(addPorts(data))
                console.log(data);
            })
            .catch((error) => {
                setPorts([])
            })
        getSimplifyRoutes()
            .then(data => {
                setRoutes(data);
                dispatch(emptyRoutes([]))
                dispatch(addRoutes(data))
                console.log(data);
            })
            .catch((error) => {
                setRoutes([])
            })
        getShips()
            .then(data => {
                setShips(data);
                dispatch(emptyShips([]))
                dispatch(addShips(data))
                console.log(data);
            })
            .catch((error) => {
                setShips([])
            })
    },[])
    // const simplifyRoutes: SimplifyRoute[] = []

    // useEffect(() => {
    //     routes.map((route) => {
    //         const startP1 = ports.filter(
    //             (port) => {
    //                 return port.port_id === route.start_point
    //             }
    //         );
    //         alert(startP1.length)
    //         alert(startP1.toString())
    //         const startP = startP1[0].coordinates.split(" ")
    //         const endP = ports.filter(
    //             (port) => port.port_id == route.end_point
    //         )[0].coordinates.split(" ")
    //         const newRoute: SimplifyRoute = {
    //             route_id: route.route_id,
    //             ship_id: route.ship_id,
    //             route: [[parseFloat(startP[0]), parseFloat(startP[1])],[parseFloat(endP[0]), parseFloat(endP[1])]],
    //             start_time: route.start_time,
    //         }
    //         simplifyRoutes.push(newRoute)
    //     })
    // }, [routes]);

    return (
        <MapContainer
            center={[64.95, 40.05]}
            zoom={5}
            style={{ height: '90vh', width: '80vw' }}
            attributionControl={false}
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                // url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />
            {
                portsStore.map(port =>
                    <PortMarker port={port} />
                )
            }
            {
                routesStore.map(route =>
                    <GeodesicLine route={route} />
                )
            }
        </MapContainer>
    );
};

export default Map;