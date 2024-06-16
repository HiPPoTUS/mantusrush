import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {Ship as StorageShip} from "../api/models";

const initialState: StorageShip[] = [];

const shipsSlice = createSlice({
    name: 'ships',
    initialState,
    selectors: {
        getShip: (state, action: PayloadAction<number>): StorageShip | undefined => {
            return state.find(ship => ship.ship_id === action.payload);
        },
        getShips: (state, action: PayloadAction<number>): StorageShip[] => {
            return state
        }
    },
    reducers: {
        addShip: (state, action: PayloadAction<StorageShip>) => {
            state.push(action.payload);
        },
        addShips: (state, action: PayloadAction<StorageShip[]>) => {
            state.push(...action.payload);
        },
        rewriteShips: (state, action: PayloadAction<StorageShip[]>) => {
            state = action.payload;
        },
        deleteShip: (state, action: PayloadAction<number>) => {
            state.filter((ship) => ship.ship_id !== action.payload);
        },
        emptyShips: (state, action: PayloadAction<StorageShip[]>) => {
            state.splice(0, state.length)
        },
    },
});


export const {
    addShip,
    addShips,
    rewriteShips,
    deleteShip,
    emptyShips
} = shipsSlice.actions;
export const {
    getShip,
    getShips
} = shipsSlice.selectors;
export default shipsSlice.reducer;