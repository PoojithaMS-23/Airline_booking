import { useNavigate } from 'react-router-dom'

import Navbar from '../components/Navbar'

function Dashboard() {

  const navigate = useNavigate()

  return (

    <div className='min-h-screen bg-gray-100'>

      <Navbar />

      <div className='p-10'>

        <h1 className='text-4xl font-bold text-blue-700 mb-8'>

          Airline Reservation Dashboard

        </h1>

        <div className='grid grid-cols-3 gap-6'>

          {/* SEARCH FLIGHTS */}
          <div className='bg-white p-6 rounded-xl shadow-lg'>

            <h2 className='text-2xl font-bold mb-4'>

              Search Flights

            </h2>

            <p className='mb-5 text-gray-600'>

              Search flights based on source and destination.

            </p>

            <button
              onClick={() => navigate('/search')}
              className='bg-blue-700 text-white px-5 py-2 rounded-lg'
            >
              Search
            </button>

          </div>

          {/* RESERVATIONS */}
          <div className='bg-white p-6 rounded-xl shadow-lg'>

            <h2 className='text-2xl font-bold mb-4'>

              My Reservations

            </h2>

            <p className='mb-5 text-gray-600'>

              View and cancel your booked tickets.

            </p>

            <button
              onClick={() => navigate('/reservations')}
              className='bg-green-700 text-white px-5 py-2 rounded-lg'
            >
              View Reservations
            </button>

          </div>

          {/* EXPLORE */}
          <div className='bg-white p-6 rounded-xl shadow-lg'>

            <h2 className='text-2xl font-bold mb-4'>

              Explore Flights

            </h2>

            <p className='mb-5 text-gray-600'>

              Explore all available airline routes.

            </p>

            <button
              onClick={() => navigate('/search')}
              className='bg-purple-700 text-white px-5 py-2 rounded-lg'
            >
              Explore
            </button>

          </div>

        </div>

      </div>

    </div>
  )
}

export default Dashboard