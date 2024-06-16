import React from 'react';
import {Modal, Spin} from 'antd';

type Props = {
    isModalOpen: boolean;
    setIsModalOpen:  React.Dispatch<React.SetStateAction<boolean>>;
}

const AddRouteModal: React.FC<Props> = (props) => {

    const showModal = () => {
        props.setIsModalOpen(true);
    };

    const handleOk = () => {
        props.setIsModalOpen(false);
    };

    const handleCancel = () => {
        props.setIsModalOpen(false);
    };

    return (
        <Modal title="Загрузка" open={props.isModalOpen} onOk={handleOk} onCancel={handleCancel}>
            <Spin size="large" />
        </Modal>
    );
};

export default AddRouteModal;