import React from "react";
import { Redirect, Route } from "react-router";

export default function AuthenticatedRoute({ component: C, appProps, ...rest }) {
    console.log(appProps, "authentacedroute")
  return (
    <Route
      {...rest}
      render={props =>
        appProps.isAuthenticated
          ? <C {...props} {...appProps} />
          : <Redirect
              to={`/login?redirect=${props.location.pathname}${props.location.search}`}
            />}
    />
  );
}