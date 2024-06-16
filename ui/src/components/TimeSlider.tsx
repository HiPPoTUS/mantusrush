import React, {useState} from 'react';
import {Button, Flex, Slider, SliderSingleProps, Statistic, Tooltip} from 'antd';
import { FastBackwardOutlined, FastForwardOutlined, StepBackwardOutlined, StepForwardOutlined } from '@ant-design/icons';
import {putTimestamp} from "../api";
import dayjs from "dayjs";

const startTimestamp = 1583182800.0

const TimeSlider = () => {

    const startDate = React.useMemo(() => dayjs.unix(startTimestamp), []);
    const endDate = React.useMemo(() => startDate.add(3, 'month').add(-1, 'day'), []);
    const dateCount = React.useMemo(() => endDate.diff(startDate, 'day'), [startDate]);

    const marks: SliderSingleProps['marks'] = {};
    for (let i = 0; i <= dateCount; i = i + 7) {
        marks[i] = startDate.add(i, 'day').format('MM-DD');
    }

    const [value, setValue] = useState(0);

    const updateValue = (value: number, diff: number): number => {
        const newValue = value + diff
        if (newValue < 0) {
            return 0;
        } else if (newValue > dateCount) {
            return dateCount
        } else {
            return newValue
        }
    }
    const handleChange = (newValue: number) => {
        setValue(newValue);
        sendRequest(newValue);
    };

    const sendRequest = (newValue: number) => {
        const timestamp = startDate.add(newValue, 'day').unix()
        putTimestamp(timestamp)
            .then(data => console.log(data))
            .catch(error => console.log(error))
    };

    return (
        <Flex wrap gap="small" style={{ width: '100%' }} justify="center">
            <Slider
                min={0} max={dateCount} step={1}
                value={value}
                onChange={handleChange}
                style={{width:'50%', marginTop: "2px", marginRight: "15px"}}
                tooltip={{
                    formatter: (nextValue) =>
                        startDate.add(nextValue || 0, 'day').format('YYYY-MM-DD'),
                }}
                marks={marks}
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
            <Flex style={{}}>
                <Statistic value={startDate.add(value || 0, 'day').format('YYYY-MM-DD')} style={{marginTop: "-2px" }} />
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