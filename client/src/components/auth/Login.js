import React, { useState, useContext } from 'react';
import axios from "axios"


const Login = (props) => {
    console.log(props)

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const updateForm = (e) => {
        if (e.target.name === "email") {
            setEmail(e.target.value)
        } else if (e.target.name === "password") {
            setPassword(e.target.value)
        }
    }


    const onSubmit = (e) => {
        e.preventDefault();
        axios.post('/api/login', {
            email: email,
            password: password
        }).then((res) => {
            window.localStorage.setItem('token', res.data.access_token);
            props.setAuth(true)
            props.history.push("/dashboard");
        }).catch((err) => {
            alert(err.message)
            console.log(err.message)
        })
    }

    return (
        <form onSubmit={onSubmit} className="form form--login">
            <h1>Login</h1>
            <input onChange={updateForm} placeholder="email" type="text" name="email" id="email"/>
            <input onChange={updateForm} placeholder="password" type="password" name="password" id="password"/>
            <button type="submit" style={{width: "100%", marginTop: "2rem"}} className="button">Login</button>
        </form>
    )

}





export default Login;

