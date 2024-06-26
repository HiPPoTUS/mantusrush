import axios from 'axios';
import {Route, Ship, CurrentRoute, PredictedRoute, Port, SimplifyRoute} from "./models";

const API_URL = 'backend:5000';
// const API_URL = process.env.API_URL
// console.log(API_URL)

export const updateRoutes = async () => {
    const response = await axios.post<string>(`${API_URL}/update`);
    return response.data;
};

export const addShip = async (ship: string) => {
    const response = await axios.post<Ship>(`${API_URL}/new_ship`, ship, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return response.data;
};

export const addRoute = async (route: string) => {
    const response = await axios.post<SimplifyRoute>(`${API_URL}/new_route`, route, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return response.data;
};

export const getPorts = async () => {
    const url = process.env.API_URL
    console.log(url)
    const response = await axios.get<Port[]>(`${API_URL}/ports`);
    return response.data;
};

export const getShips = async () => {
    const response = await axios.get<Ship[]>(`${API_URL}/ships`);
    return response.data;
};

export const getRoutes = async () => {
    const response = await axios.get<Route[]>(`${API_URL}/routes`);
    return response.data;
};

export const getSimplifyRoutes = async () => {
    const response = await axios.get<SimplifyRoute[]>(`${API_URL}/routes/simplify`);
    return response.data;
};

export const getCurrentRoutes = async () => {
    const response = await axios.get<CurrentRoute[]>(`${API_URL}/routes/current`);
    return response.data;
};

export const getPredictedRoute = async () => {
    const response = await axios.get<PredictedRoute[]>(`${API_URL}/routes/predicted`);
    return response.data;
};

export const putTimestamp = async (timestamp: number) => {
    const response = await axios.put(`${API_URL}/timestamp/` + timestamp);
    return response.data;
};