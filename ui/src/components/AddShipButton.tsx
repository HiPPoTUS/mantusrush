import React, {useState} from 'react';
import {Button, Tooltip} from "antd";
import { FaShip } from "react-icons/fa6";
import AddShipModal from "./modals/AddShipModal";


const AddShipButton: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false);

    const onClick = () => {
        setIsModalOpen(true)
    }

    return (
        <>
            <Tooltip placement="left" title="Загрузить данные о новом корабле" color={"#555E"}>
                <Button
                    type="primary"
                    loading={isLoading}
                    style={{height: 50, width: 200}}
                    icon={<FaShip />}
                    onClick={onClick}
                >
                    <div style={{fontSize: "large"}}>
                        Новый корабль
                    </div>
                </Button>
            </Tooltip>
            <AddShipModal isModalOpen={isModalOpen} setIsModalOpen={setIsModalOpen}/>
        </>
    );
};

export default AddShipButton;