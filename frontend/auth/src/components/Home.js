import React ,{ useEffect } from 'react'
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; 

export default function Home() {

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



    return (
        <div className="container mt-5 pt-5">
            <div className="row">
                <div className="col-md-6 offset-md-3 ">
                    <button className='btn btn-danger' onClick={handleLogout} style={{ position: 'absolute', top: '0', right: '0' ,margin: "20px"}}>Logout</button>
                    <h2 className="mb-5">Home</h2>
                    <p>Welcome to the home page</p>
                </div>
            </div>
        </div>
    );
}