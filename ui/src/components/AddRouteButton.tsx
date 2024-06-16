import React, {useState} from 'react';
import {Button, Tooltip} from "antd";
import {FaRoute} from "react-icons/fa6";
import AddRouteModal from "./modals/AddRouteModal";


const AddRouteButton: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false);

    const onClick = () => {
        setIsModalOpen(true)
    }

    return (
        <>
            <Tooltip placement="left" title="Загрузить данные о новом маршруте" color={"#555E"}>
                <Button
                    type="primary"
                    loading={isLoading}
                    style={{height: 50, width: 200}}
                    icon={<FaRoute/>}
                    onClick={onClick}
                >
                    <div style={{fontSize: "large"}}>
                        Новый маршрут
                    </div>
                </Button>
            </Tooltip>
            <AddRouteModal isModalOpen={isModalOpen} setIsModalOpen={setIsModalOpen}/>
        </>
    );
};

export default AddRouteButton;