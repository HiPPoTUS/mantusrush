import React, { useState } from 'react';
import {AutoComplete, Button, DatePicker, Form, Spin} from 'antd';
import {RouteRequest} from "../../api/models";
import {useDispatch, useSelector} from 'react-redux';
import {AppDispatch, RootState} from "../../store";
import {addRoute} from "../../api";
import dayjs from 'dayjs';
import {addRoute as addRouteStore} from "../../store/routesSlice";

const dateFormat = 'YYYY-MM-DD';

type FieldType = {
    ship_name: string;
    end_point: string;
    start_point: string;
    date: Date;
};

const getPanelValue = (searchText: string, searchList: string[]) => {
    searchText = searchText.toLowerCase()
    return searchList.filter(
        (name) => name.toLowerCase().includes(searchText)
    ).map(
        (name) => {
            return {value: name}
        }
    )
}

const AddRouteForm: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const ports = useSelector((state: RootState) => state.ports);
    const ships = useSelector((state: RootState) => state.ships);

    const shipsNames = ships.map((ship) => ship.name)
    const portsNames = ports.map((port) => port.name)


    const [optionsShips, setOptionsShips] = useState<{ value: string }[]>(getPanelValue("", shipsNames));
    const [optionsPortsArr, setOptionsPortsArr] = useState<{ value: string }[]>(getPanelValue("", portsNames));
    const [optionsPortsDep, setOptionsPortsDep] = useState<{ value: string }[]>(getPanelValue("", portsNames));
    const [isModalOpen, setIsModalOpen] = useState(false);



    const [form] = Form.useForm();

    const onFinish = () => {
        setIsModalOpen(true)
        const formFields: FieldType = {
            ship_name: form.getFieldValue("ship_name").toString(),
            start_point: form.getFieldValue("start_point").toString().toLowerCase(),
            end_point: form.getFieldValue("end_point").toString().toLowerCase(),
            date: form.getFieldValue("date")
        }
        console.log(ports)
        const ship = ships.find(ship => ship.name === formFields.ship_name);
        const start = ports.find(port => port.name === formFields.start_point);
        const end = ports.find(port => port.name === formFields.end_point);
        if (ship === undefined) {
            alert("Нет такого корабля")
            return
        }
        if (start === undefined) {
            alert("Нет такого начального порта")
            return
        }
        if (end === undefined) {
            alert("Нет такого конечного порта")
            return
        }
        const ship_id = ship.ship_id
        const start_point_idx = start.port_id
        const end_point_idx = end.port_id
        const request: RouteRequest = {
            ship_id: ship_id,
            start_point_idx: start_point_idx,
            end_point_idx: end_point_idx,
            start_time: formFields.date
        }
        const jsonRequest =JSON.stringify(request)
        console.log(jsonRequest)

        addRoute(jsonRequest)
            .then((data) => {
                dispatch(addRouteStore(data))
            })
            .catch(err => alert(err))
            .finally(() => {
                setIsModalOpen(false)
            })
        form.resetFields(["ship_name", "end_point", "start_point", "date"])
    }
    return (
        <Form
            layout={"vertical"}
            form={form}
            onFinish={() => {
                onFinish()
            }}
            clearOnDestroy
        >
            <Form.Item<FieldType>
                name="ship_name"
                label="Название корабля"
                rules={[{ required: true, message: 'Пожалуйста введите название корабля' }]}
            >
                <AutoComplete
                    options={optionsShips}
                    onSearch={(text) => setOptionsShips(getPanelValue(text, shipsNames))}
                    placeholder="Введите название корабля"
                />
            </Form.Item>

            <Form.Item<FieldType>
                name="start_point"
                label="Пункт отправления"
                rules={[{ required: true, message: 'Пожалуйста введите пункт отправления' }]}
            >
                <AutoComplete
                    options={optionsPortsDep}
                    onSearch={(text) => setOptionsPortsDep(getPanelValue(text, portsNames))}
                    placeholder="Введите пункт отправления"
                />
            </Form.Item>

            <Form.Item<FieldType>
                name="end_point"
                label="Пункт прибытия"
                rules={[{ required: true, message: 'Пожалуйста введите пункт назначения' }]}
            >
                <AutoComplete
                    options={optionsPortsArr}
                    onSearch={(text) => setOptionsPortsArr(getPanelValue(text, portsNames))}
                    placeholder="Введите пункт прибытия"
                />
            </Form.Item>

            <Form.Item<FieldType>
                name="date"
                label="Дата готовности к отплытию"
                rules={[{ required: true, message: 'Пожалуйста выберите дату' }]}
            >
                <DatePicker
                    defaultValue={dayjs('2020-03-03', dateFormat)}
                    minDate={dayjs('2020-03-03', dateFormat)}
                    maxDate={dayjs('2020-06-03', dateFormat)}
                    placeholder="Выберите дату"
                />
            </Form.Item>

            <Form.Item >
                <Button type="primary" htmlType="submit">
                    Добавить
                </Button>
                { isModalOpen && <Spin style={{marginLeft: "10px"}} size="default" /> }
            </Form.Item>
        </Form>
);
};

export default AddRouteForm;