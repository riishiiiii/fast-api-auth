import React, { useEffect, useState } from 'react'
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function Home() {

    const [username, setUsername] = useState('');
    const showToast = (message, type) => {
        toast(message, { type: type, autoClose: 3000 });
    };
    const handleLogout = () => {
        showToast("User logged out successfully", 'success')
        document.cookie = `access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
        document.cookie = `refresh_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;

        window.location.href = '/login';
    };

    useEffect(() => {
        const accessToken = document.cookie.split('; ').find(row => row.startsWith('access_token='));
        if (!accessToken) {
            window.location.href = '/login';
        } else {
            const [, tokenValue] = accessToken.split('=');
            const tokenExpires = parseInt(tokenValue);
            const currentTimestamp = new Date().getTime();

            if (currentTimestamp > tokenExpires) {
                handleLogout();
            }
        }
    }, []);


    useEffect(() => {
        const fetchData = async () => {
            try {
                const access_token = document.cookie.split('; ').find(row => row.startsWith('access_token=')).split('=')[1];
                const response = await fetch('http://localhost:8001/auth/me', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${access_token}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setUsername(data.user_name);
                } else {
                    const data = await response.json();
                    showToast(data.detail, 'error');
                }
            } catch (error) {
                console.error(error);
                showToast('Error during fetching user data', 'error');
            }
        };

        fetchData();
    }, []); //


    return (
        <div className="container mt-5 pt-5">
            <div className="row">
                <div className="col-md-6 offset-md-3 ">
                    <button className='btn btn-danger' onClick={handleLogout} style={{ position: 'absolute', top: '0', right: '0', margin: "20px" }}>Logout</button>
                    <h2 className="mb-5">Home</h2>
                    <p>Welcome to the home page <span className='fs-3 '> {username} </span></p>
                </div>
            </div>
        </div>
    );
}