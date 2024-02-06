import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {  toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


export default function Register() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const showToast = (message, type) => {
        toast(message, { type: type, autoClose: 3000 });
    };

    const handleRegister = async (e) => {
        e.preventDefault();

        const user = {
            user_name: username,
            email: email,
            password: password,
        };
        try {
            const response = await fetch('http://localhost:8001/auth/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(user),
            });

            if (response.ok) {
                showToast("User registered successfully", 'success');
                navigate('/login'); 
            } else {
                const data = await response.json();
                showToast(data.detail, 'error')
            }
        } catch (error) {
            console.log (error);
            showToast('Error during registration', 'error');
        }
    };



    return (
        <>
            <div className="container mt-5 pt-5">
                <div className="row">
                    <div className="col-md-6 offset-md-3 ">
                        <h2 className='mb-5'>Register</h2>
                        <form onSubmit={handleRegister}>
                            <div className="form-group">
                                <label className='mb-2'>Username</label>
                                <input type="text" className="form-control" value={username} onChange={e => setUsername(e.target.value)} />
                            </div>
                            <div className="form-group">
                                <label className='mb-2 mt-2'>Email</label>
                                <input type="email" className="form-control" value={email} onChange={e => setEmail(e.target.value)} />
                            </div>
                            <div className="form-group">
                                <label className='mb-2 mt-2'>Password</label>
                                <input type="password" className="form-control" value={password} onChange={e => setPassword(e.target.value)} />
                            </div>
                            <button type="submit" className="btn btn-primary mt-2">Register</button>
                        </form>
                        <br/>
                        <a href="/login">Already have an account </a>
                    </div>
                </div>
            </div>

        </>
    )
}
