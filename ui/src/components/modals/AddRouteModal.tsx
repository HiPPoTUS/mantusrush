import React from 'react';
import { Modal } from 'antd';
import AddRouteForm from "../forms/AddRouteForm";

type Props = {
    isModalOpen: boolean;
    setIsModalOpen:  React.Dispatch<React.SetStateAction<boolean>>;
}

const AddRouteModal: React.FC<Props> = (props) => {

    const handleOk = () => {
        props.setIsModalOpen(false);
    };

    const handleCancel = () => {
        props.setIsModalOpen(false);
    };

    return (
        <Modal title="Добавление нового маршрута" open={props.isModalOpen} onOk={handleOk} onCancel={handleCancel}>
            <AddRouteForm/>
        </Modal>
    );
};

export default AddRouteModal;