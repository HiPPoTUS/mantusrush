import React, {useEffect, useState} from 'react';
import {Button, Flex, Slider, SliderSingleProps, Statistic, Tooltip} from 'antd';
import { FastBackwardOutlined, FastForwardOutlined, StepBackwardOutlined, StepForwardOutlined } from '@ant-design/icons';
import {putTimestamp} from "../api";
import moment from 'moment';

const TimeSlider = () => {
    const [value, setValue] = useState(0);
    const updateValue = (value: number, diff: number): number => {
        const newValue = value + diff
        if (newValue < 0) {
            return 0;
        } else if (newValue > 100) {
            return 100
        } else {
            return newValue
        }
    }
    useEffect(() => {
        if (value < 0) {
            setValue(0);
        } else if (value > 100) {
            setValue(100)
        }
    }, [value]);
    const handleChange = (newValue: number) => {
        setValue(newValue);
        sendRequest(newValue);
    };

    const sendRequest = (newValue: number) => {
        putTimestamp(newValue)
            .then(data => console.log(data))
            .catch(error => console.log(error))
    };

    return (
        <Flex wrap gap="small" style={{ width: '100%' }} justify="center">
            <Slider
                min={0} max={100} step={1}
                value={value}
                onChange={handleChange}
                style={{width:'50%'}}
            />
            <Tooltip title="Назад на неделю">
                <Button shape="circle" icon={<FastBackwardOutlined/>} onClick={() => {
                    setValue((prev) => updateValue(prev, -7));
                }}/>
            </Tooltip>
            <Tooltip title="Назад на день">
                <Button type="primary" shape="circle" icon={<StepBackwardOutlined/>}  onClick={() => {
                    setValue((prev) => updateValue(prev, -1));
                }}/>
            </Tooltip>
            <Flex style={{width:'40px'}}>
                <Statistic value={value} style={{margin: "auto" }} />
            </Flex>
            <Tooltip title="Вперед на день">
                <Button type="primary" shape="circle" icon={<StepForwardOutlined/>}  onClick={() => {
                    setValue((prev) => updateValue(prev, 1));
                }}/>
            </Tooltip>
            <Tooltip title="Вперед на неделю">
                <Button shape="circle" icon={<FastForwardOutlined/>}  onClick={() => {
                    setValue((prev) => updateValue(prev, 7));
                }}/>
            </Tooltip>
        </Flex>
    );
};

export default TimeSlider;