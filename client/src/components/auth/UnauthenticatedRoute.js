import React from "react";
import { Redirect, Route } from "react-router";

export default function UnauthenticatedRoute({ component: C, appProps, ...rest }) {
  console.log(appProps)
  return (
        <Route
          {...rest}
          render={props =>
            !appProps.isAuthenticated
              ? <C {...props} {...appProps} />
              : <Redirect to="/dashboard" />}
        />
  )

}
