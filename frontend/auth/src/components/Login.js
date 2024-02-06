import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function Login() {
    const [username, setusername] = useState("");
    const [password, setPassword] = useState("");

    const showToast = (message, type) => {
        toast(message, { type: type, autoClose: 3000 });
    };


    const navigate = useNavigate();
    const handleLogin = async (e) => {
        e.preventDefault();
    
        const user = {
            user_name: username,
            password: password,
        };
        try {
            const response = await fetch("http://localhost:8001/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            });

            if (response.ok) {
                const data = await response.json();

                const { access_token, refresh_token } = data;

                document.cookie = `access_token=${access_token}; path=/`;
                document.cookie = `refresh_token=${refresh_token}; path=/`;
                showToast("User logged in successfully", 'success')
                navigate("/");
            } else {
                const data = await response.json();
                showToast(data.detail, 'error')
            }
        } catch (error) {
            console.log(error);
            showToast("Error during login", 'error')
        }
    };

    return (
        <>
            <div className="container mt-5 pt-5">
                <div className="row">
                    <div className="col-md-6 offset-md-3 ">
                        <h2 className="mb-5">Login</h2>
                        <form onSubmit={handleLogin}>
                            <div className="form-group">
                                <label className="mb-2">Username</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={username}
                                    onChange={(e) => setusername(e.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label className="mb-2 mt-2">Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            <button type="submit" className="btn btn-primary mt-3">
                                Login
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
}