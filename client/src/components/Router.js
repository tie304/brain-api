import React, { useContext, useEffect, useState } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import ProjectManager from "./dashboard/ProjectManager"
import Login from "./auth/Login"

import AuthenticatedRoute from "./auth/AuthenticatedRoute";
import UnauthenticatedRoute from "./auth/UnauthenticatedRoute";
import jwt_decode from "jwt-decode";

const Router = (props) => {
     const [auth,setAuth] = useState(false)

     useEffect(() => {
         if (localStorage.getItem("token")) {
            const decodedToken = jwt_decode(localStorage.getItem("token"));
            const currentTime = Date.now() / 1000;
            if (decodedToken.exp < currentTime) {
                setAuth(false)
            } else {
                setAuth(true)
            }
         }

    }, [])

     return (
          <Switch>
                <AuthenticatedRoute path='/dashboard' appProps={{isAuthenticated: auth}} component={ProjectManager}/>
                <UnauthenticatedRoute  path="/login" component={Login} appProps={{ isAuthenticated:auth , setAuth} } />
           </Switch>
         )

}

export default Router;