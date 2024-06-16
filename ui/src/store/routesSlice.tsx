import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {SimplifyRoute as StorageRoute} from "../api/models";

const initialState: StorageRoute[] = [];

const routesSlice = createSlice({
    name: 'routes',
    initialState,
    selectors: {
        getRoute: (state, action: PayloadAction<number>): StorageRoute | undefined => {
            return state.find(route => route.route_id === action.payload);
        },
        getRoutes: (state, action: PayloadAction<number>): StorageRoute[] => {
            return state
        }
    },
    reducers: {
        addRoute: (state, action: PayloadAction<StorageRoute>) => {
            state.push(action.payload);
        },
        addRoutes: (state, action: PayloadAction<StorageRoute[]>) => {
            state.push(...action.payload);
        },
        rewriteRoutes: (state, action: PayloadAction<StorageRoute[]>) => {
            state = action.payload;
        },
        deleteRoute: (state, action: PayloadAction<number>) => {
            state.filter((route) => route.route_id !== action.payload);
        },
        emptyRoutes: (state, action: PayloadAction<StorageRoute[]>) => {
            state.splice(0, state.length)
        },
    },
});


export const {
    addRoute,
    addRoutes,
    rewriteRoutes,
    deleteRoute,
    emptyRoutes
} = routesSlice.actions;
export const {
    getRoute,
    getRoutes
} = routesSlice.selectors;
export default routesSlice.reducer;