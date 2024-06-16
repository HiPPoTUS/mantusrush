import React, {useState} from 'react';
import {App, Button, notification, Spin, Tooltip} from "antd";
import {updateRoutes} from "../api";
import {CalculatorOutlined} from '@ant-design/icons';
import {FaCalculator} from "react-icons/fa6";


const OptimizeRoutesButton: React.FC = () => {
    const [isLoading, setIsLoading] = useState(false)
    const { message, modal, notification } = App.useApp();

    const onClick = () => {
        setIsLoading(true)
        updateRoutes()
            .then(data => {
                showNotification(0, data)
                console.log(data)
            })
            .catch(err => {
                showNotification(1, err)
                console.log(err)
            })
            .finally(() => setIsLoading(false))
    }
    const showNotification = (level: number, data: string) => {
        if (level === 0) {
            notification.info({
                message: `Успех`,
                description: "Пути успешно перестроены",
                placement: 'topLeft',
            });
        } else if (level === 1) {
            notification.error({
                message: `Ошибка`,
                description: data,
                placement: 'topLeft',
            });
        }
    };

    return (
        <Tooltip placement="left" title="Рассчитать и обновить пути кораблей" color={"#555E"}>
            <Button
                type="primary"
                loading={isLoading}
                style={{height: 50, width: 200}}
                icon={<FaCalculator />}
                onClick={onClick}
            >
                <div style={{fontSize: "large"}}>
                    Обновить пути
                </div>
            </Button>
        </Tooltip>
    );
};

export default OptimizeRoutesButton;