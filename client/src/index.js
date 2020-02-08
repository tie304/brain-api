import React from 'react';
import jwt_decode from "jwt-decode";
import ReactDOM from 'react-dom';
import {BrowserRouter} from 'react-router-dom';
import axios from "axios";
import App from './App';


// Add a request interceptor
axios.interceptors.request.use(function (config) {
    const token = window.localStorage.getItem("token");
    config.headers.common['Authorization'] = `Bearer ${token}`
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });




ReactDOM.render(
  <BrowserRouter>
      <App />
</BrowserRouter>,
  document.getElementById('root')
);
