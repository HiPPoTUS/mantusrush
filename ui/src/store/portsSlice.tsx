import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {Port as StoragePort} from "../api/models";

const initialState: StoragePort[] = [];

const portsSlice = createSlice({
    name: 'ports',
    initialState,
    selectors: {
        getPort: (state, action: PayloadAction<number>): StoragePort | undefined => {
            return state.find(port => port.port_id === action.payload);
        },
        getPorts: (state, action: PayloadAction<number>): StoragePort[] => {
            return state
        }
    },
    reducers: {
        addPort: (state, action: PayloadAction<StoragePort>) => {
            state.push(action.payload);
        },
        addPorts: (state, action: PayloadAction<StoragePort[]>) => {
            state.push(...action.payload);
        },
        rewritePorts: (state, action: PayloadAction<StoragePort[]>) => {
            state = action.payload;
        },
        deletePort: (state, action: PayloadAction<number>) => {
            state.filter((port) => port.port_id !== action.payload);
        },
        emptyPorts: (state, action: PayloadAction<StoragePort[]>) => {
            state.splice(0, state.length)
        },
    },
});


export const {
    addPort,
    addPorts,
    rewritePorts,
    deletePort,
    emptyPorts
} = portsSlice.actions;
export const {
    getPort,
    getPorts
} = portsSlice.selectors;
export default portsSlice.reducer;