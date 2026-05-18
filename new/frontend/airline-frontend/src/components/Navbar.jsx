import { Link } from 'react-router-dom'

function Navbar() {

  return (

    <div className='sticky top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-white/30 shadow-md'>

      <div className='max-w-7xl mx-auto px-8 py-5 flex justify-between items-center'>

        <h1 className='text-3xl font-extrabold bg-gradient-to-r from-blue-700 to-purple-700 bg-clip-text text-transparent'>

          SkyWay Airlines

        </h1>

        <div className='flex gap-8 text-lg font-semibold text-gray-700'>

          <Link
            to='/dashboard'
            className='hover:text-blue-700 transition-all'
          >
            Home
          </Link>

          <Link
            to='/search'
            className='hover:text-purple-700 transition-all'
          >
            Search Flights
          </Link>

          <Link
            to='/reservations'
            className='hover:text-green-700 transition-all'
          >
            Reservations
          </Link>

        </div>

      </div>

    </div>
  )
}

export default Navbar