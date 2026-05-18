import { useState } from 'react'

import { Link, useNavigate } from 'react-router-dom'

import API from '../services/api'

function Login() {

  const navigate = useNavigate()

  const [email, setEmail] =
    useState('')

  const [password, setPassword] =
    useState('')

  const loginUser = async () => {

    try {

      const response =
        await API.post('/login', {

          email,
          password
        })

      if (response.data.success) {

        localStorage.setItem(
          'userId',
          response.data.userId
        )

        navigate('/dashboard')

      } else {

        alert('Invalid Credentials')
      }

    } catch (error) {

      alert('Login Failed')
    }
  }

  return (

    <div className='min-h-screen flex items-center justify-center px-5'>

      <div className='bg-white/70 backdrop-blur-2xl shadow-2xl rounded-3xl p-10 w-full max-w-md border border-white/40'>

        <div className='text-center mb-10'>

          <h1 className='text-5xl font-extrabold bg-gradient-to-r from-blue-700 to-purple-700 bg-clip-text text-transparent mb-3'>

            SkyWay Airlines

          </h1>

          <p className='text-gray-600 text-lg'>

            Welcome Back

          </p>

        </div>

        <div className='space-y-5'>

          <input
            type='email'
            placeholder='Email Address'
            className='w-full p-4 rounded-2xl border border-gray-300 outline-none focus:ring-4 focus:ring-blue-300'
            onChange={(e) =>
              setEmail(e.target.value)
            }
          />

          <input
            type='password'
            placeholder='Password'
            className='w-full p-4 rounded-2xl border border-gray-300 outline-none focus:ring-4 focus:ring-purple-300'
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          <button
            onClick={loginUser}
            className='w-full bg-gradient-to-r from-blue-700 to-purple-700 text-white py-4 rounded-2xl font-bold text-lg hover:scale-105 transition-all duration-300 shadow-xl'
          >
            Login
          </button>

        </div>

        <p className='text-center mt-8 text-gray-700'>

          New User?

          <Link
            to='/register'
            className='ml-2 text-blue-700 font-bold hover:underline'
          >
            Register
          </Link>

        </p>

      </div>

    </div>
  )
}

export default Login