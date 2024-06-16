import React from 'react';
import { Modal } from 'antd';
import AddShipForm from "../forms/AddShipForm";

type Props = {
    isModalOpen: boolean;
    setIsModalOpen:  React.Dispatch<React.SetStateAction<boolean>>;
}

const AddShipModal: React.FC<Props> = (props) => {

    const handleOk = () => {
        props.setIsModalOpen(false);
    };

    const handleCancel = () => {
        props.setIsModalOpen(false);
    };

    return (
        <Modal title="Добавление нового корабля" open={props.isModalOpen} onOk={handleOk} onCancel={handleCancel}>
            <AddShipForm/>
        </Modal>
    );
};

export default AddShipModal;