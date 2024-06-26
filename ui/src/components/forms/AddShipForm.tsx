import React, { useState } from 'react';
import {AutoComplete, Button, Form, Input, Spin} from 'antd';
import {ShipRequest} from "../../api/models";
import {useDispatch, useSelector} from 'react-redux';
import {AppDispatch, RootState} from "../../store";
import {addShip} from "../../api";
import {addShip as addShipStore} from "../../store/shipsSlice";

const dateFormat = 'YYYY-MM-DD';

type FieldType = {
    ship_name: string;
    arc: string;
    velocity: number;
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

const AddShipForm: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const ships = useSelector((state: RootState) => state.ships);

    const arcs = ["3", "4", "5", "6", "7", "9"].map((arcClass) => "Arc " + arcClass)
    arcs.push("Нет")

    const [optionsArcs, setOptionsArcs] = useState<{ value: string }[]>(getPanelValue("", arcs));
    const [isModalOpen, setIsModalOpen] = useState(false);

    const [form] = Form.useForm();

    const onFinish = () => {
        setIsModalOpen(true)
        const formFields: FieldType = {
            ship_name: form.getFieldValue("ship_name").toString(),
            arc: form.getFieldValue("arc").toString(),
            velocity: Number(form.getFieldValue("velocity").toString())
        }
        const ship = ships.find(ship => ship.name === formFields.ship_name);
        const arc = arcs.find(arc => arc === formFields.arc);
        if (ship !== undefined) {
            alert("Такой корабль уже существует")
            return
        }
        if (arc === undefined) {
            alert("Нет такого ледового класса")
            return
        }
        if (formFields.velocity <= 0) {
            alert("Такая скорость недопустима")
            return
        }
        let ice_class = 0
        if (arc !== "Нет") {
            ice_class = Number(arc.split(" ")[1])
        }
        const request: ShipRequest = {
            name: formFields.ship_name,
            max_speed: formFields.velocity,
            ice_class: ice_class
        }
        const jsonRequest =JSON.stringify(request)
        console.log(jsonRequest)
        addShip(jsonRequest)
            .then((data) => {
                dispatch(addShipStore(data))
            })
            .catch(err => alert(err))
            .finally(() => {
                setIsModalOpen(false)
            })
        form.resetFields(["ship_name", "arc", "velocity"])
    }

    return (
        <Form
            layout={"vertical"}
            form={form}
            onFinish={() => {
                onFinish()
                setIsModalOpen(false)
            }}
            clearOnDestroy
        >
            <Form.Item<FieldType>
                name="ship_name"
                label="Название корабля"
                rules={[{ required: true, message: 'Пожалуйста введите название корабля' }]}
            >
                <Input placeholder="Введите название корабля"/>
            </Form.Item>

            <Form.Item<FieldType>
                name="arc"
                label="Ледовый класс корабля"
                rules={[{ required: true, message: 'Пожалуйста введите ледовый класс корабля' }]}
            >
                <AutoComplete
                    options={optionsArcs}
                    onSearch={(text) => setOptionsArcs(getPanelValue(text, arcs))}
                    placeholder="Введите ледовый класс корабля"
                />
            </Form.Item>

            <Form.Item<FieldType>
                name="velocity"
                label="Максимальная скорость"
                rules={[{ required: true, message: 'Пожалуйста введите максимальную скорость' }]}
            >
                <Input placeholder="Введите максимальную скорость корабля"/>
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

export default AddShipForm;