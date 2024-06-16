import { configureStore } from '@reduxjs/toolkit';
import shipsReducer from './shipsSlice';
import routesReducer from './routesSlice';
import portsReducer from './portsSlice';

const store = configureStore({
    reducer: {
        ships: shipsReducer,
        routes: routesReducer,
        ports: portsReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch;


export default store;