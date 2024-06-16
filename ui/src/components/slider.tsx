import React from 'react';
import type { DatePickerProps } from 'antd';
import { DatePicker, Slider, Space } from 'antd';
import dayjs from 'dayjs';

const onChange: DatePickerProps['onChange'] = (date, dateString) => {

};

const MyDatePanel = () => {

    // Value
    const startDate = React.useMemo(() => dayjs().date(1).month(0), []);
    const [innerValue, setInnerValue] = React.useState(startDate);

    // Range
    const dateCount = React.useMemo(() => {
        const endDate = startDate.add(1, 'year').add(-1, 'day');
        return endDate.diff(startDate, 'day');
    }, [startDate]);

    const sliderValue = Math.min(Math.max(0, innerValue.diff(startDate, 'day')), dateCount);

    // Render
    return (
        <Slider
            min={0}
            max={dateCount}
            value={sliderValue}
            onChange={(nextValue) => {
                const nextDate = startDate.add(nextValue, 'day');
                setInnerValue(nextDate);
            }}
            tooltip={{
                formatter: (nextValue) => startDate.add(nextValue || 0, 'day').format('YYYY-MM-DD'),
            }}
        />
    );
};

const TimerPicker: React.FC = () => (
    <Space direction="vertical">
        <DatePicker
            showNow={false}
            onChange={onChange}
        />
    </Space>
);

export default TimerPicker;