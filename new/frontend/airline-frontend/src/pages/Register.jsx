import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import API from '../services/api'

function Register() {

  const navigate = useNavigate()

  const [formData, setFormData] = useState({

    name: '',
    email: '',
    phone: '',
    password: ''
  })

  const registerUser = async () => {

    try {

      await API.post(
        '/register',
        formData
      )

      alert('Registration Successful')

      navigate('/')

    } catch (error) {

      alert('Registration Failed')
    }
  }

  return (

    <div className='min-h-screen flex items-center justify-center bg-gray-100'>

      <div className='bg-white p-10 rounded-xl shadow-xl w-[450px]'>

        <h1 className='text-3xl font-bold text-center mb-8'>
          Register
        </h1>

        <input
          type='text'
          placeholder='Name'
          className='w-full border p-3 rounded-lg mb-4'
          onChange={(e) =>
            setFormData({
              ...formData,
              name: e.target.value
            })
          }
        />

        <input
          type='email'
          placeholder='Email'
          className='w-full border p-3 rounded-lg mb-4'
          onChange={(e) =>
            setFormData({
              ...formData,
              email: e.target.value
            })
          }
        />

        <input
          type='text'
          placeholder='Phone'
          className='w-full border p-3 rounded-lg mb-4'
          onChange={(e) =>
            setFormData({
              ...formData,
              phone: e.target.value
            })
          }
        />

        <input
          type='password'
          placeholder='Password'
          className='w-full border p-3 rounded-lg mb-4'
          onChange={(e) =>
            setFormData({
              ...formData,
              password: e.target.value
            })
          }
        />

        <button
          onClick={registerUser}
          className='w-full bg-blue-700 text-white p-3 rounded-lg'
        >
          Register
        </button>

      </div>

    </div>
  )
}

export default Register