import {Marker, Popup} from "react-leaflet";
import React from "react";
import {Port} from "../../api/models";
import L from "leaflet";

// Установите кастомный икон для маркера
const customIcon = new L.Icon({
    iconUrl: '/map/anchor.svg', // Укажите путь к вашей картинке
    iconSize: [32, 32], // Размер иконки
    iconAnchor: [16, 16], // Точка привязки иконки (относительно верхнего левого угла)
    popupAnchor: [0, -16] // Точка привязки всплывающего окна (относительно точки привязки иконки)
});

type Props = {
    port: Port
}

const PortMarker: React.FC<Props> = (props) => {
    const coordinates = props.port.coordinates.split(" ")
    const pos = coordinates.map(coord => parseFloat(coord))
    return (
        <Marker position={[pos[0], pos[1]]} icon={customIcon}>
            <Popup>
                {props.port.name}
            </Popup>
        </Marker>
    )
}

export default PortMarker;