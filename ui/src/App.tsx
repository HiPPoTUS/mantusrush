import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import Map from './components/map/Map';
import TimeSlider from './components/TimeSlider';
import OptimizeRoutesButton from './components/OptimizeRoutesButton';
import AddShipButton from "./components/AddShipButton";
import AddRouteButton from "./components/AddRouteButton";
import {Flex} from "antd";


const App: React.FC = () => {
  return (
      <Provider store={store}>
        <Flex wrap gap={"large"}>
          <Flex vertical gap={"large"} align={"center"} style={{height: "100vh"}}>
            <Map />
            <TimeSlider />
          </Flex>
          <Flex vertical gap={"large"} align={"center"} style={{margin: "auto"}}>
            <OptimizeRoutesButton />
            <AddShipButton />
            <AddRouteButton />
          </Flex>
        </Flex>
      </Provider>
  );
};

export default App;