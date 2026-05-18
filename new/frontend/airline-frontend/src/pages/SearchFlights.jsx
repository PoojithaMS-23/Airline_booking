import { useState, useEffect } from 'react'

import Navbar from '../components/Navbar'
import API from '../services/api'

function SearchFlights() {

  const [source, setSource] = useState('')
  const [destination, setDestination] = useState('')

  const [flights, setFlights] = useState([])

  const [message, setMessage] = useState('')

  // AUTO REFRESH EVERY 2 SECONDS
  useEffect(() => {

    if (!source || !destination)
      return

    const interval =
      setInterval(async () => {

        try {

          const response =
            await API.get(

              `/search?source=${source}&destination=${destination}`
            )

          // UPDATE UI
          setFlights([
            ...response.data
          ])

        } catch (error) {

          console.log(error)
        }

      }, 2000)

    return () =>
      clearInterval(interval)

  }, [source, destination])

  // SEARCH FLIGHTS
  const searchFlights = async () => {

    try {

      const response = await API.get(

        `/search?source=${source}&destination=${destination}`
      )

      setFlights([
        ...response.data
      ])

      if (response.data.length === 0) {

        setMessage('No Flights Found')

      } else {

        setMessage('')
      }

    } catch (error) {

      console.log(error)

      setMessage('Search Failed')
    }
  }

  // BOOK TICKET
  const bookTicket = async (
    scheduleId,
    travelClass
  ) => {

    const seats =
      prompt('Enter Number Of Seats')

    if (!seats) return

    try {

      const response =
        await API.post(

          '/book',

          {
            userId:
              localStorage.getItem('userId'),

            scheduleId,

            travelClass,

            seatsRequired:
              Number(seats)
          }
        )

      alert(
        response.data.message
      )

      // FETCH UPDATED FLIGHTS
      const updatedFlights =
        await API.get(

          `/search?source=${source}&destination=${destination}`
        )

      // UPDATE UI
      setFlights([
        ...updatedFlights.data
      ])

    } catch (error) {

      console.log(error)

      if (
        error.response &&
        error.response.data
      ) {

        alert(
          error.response.data.message
        )

      } else {

        alert('Booking Failed')
      }
    }
  }

  return (

    <div className='min-h-screen bg-gray-100'>

      <Navbar />

      <div className='max-w-7xl mx-auto p-6'>

        {/* HEADER */}
        <div className='mb-6'>

          <h1 className='text-4xl font-bold text-gray-800'>
            Explore Flights
          </h1>

          <p className='text-gray-600 mt-1'>
            Search available flights instantly
          </p>

        </div>

        {/* SEARCH BAR */}
        <div className='bg-white rounded-2xl shadow-md p-4 mb-6'>

          <div className='flex flex-col md:flex-row gap-4 items-center'>

            {/* SOURCE */}
            <input
              type='text'
              placeholder='Enter Source'
              value={source}
              onChange={(e) =>
                setSource(e.target.value)
              }
              className='flex-1 border border-gray-300 rounded-xl p-3 outline-none focus:ring-2 focus:ring-blue-300'
            />

            {/* DESTINATION */}
            <input
              type='text'
              placeholder='Enter Destination'
              value={destination}
              onChange={(e) =>
                setDestination(e.target.value)
              }
              className='flex-1 border border-gray-300 rounded-xl p-3 outline-none focus:ring-2 focus:ring-purple-300'
            />

            {/* SEARCH BUTTON */}
            <button
              onClick={searchFlights}
              className='bg-blue-700 hover:bg-blue-800 text-white px-8 py-3 rounded-xl font-semibold'
            >
              Search
            </button>

          </div>

        </div>

        {/* MESSAGE */}
        {
          message && (

            <div className='bg-red-100 text-red-700 p-3 rounded-xl mb-4'>

              {message}

            </div>
          )
        }

        {/* FLIGHTS */}
        <div className='space-y-4'>

          {
            flights.map((flight) => (

              <div
                key={flight.schedule_id}
                className='bg-white rounded-2xl shadow-md p-5'
              >

                {/* TOP */}
                <div className='flex flex-col md:flex-row justify-between items-start md:items-center mb-5'>

                  <div>

                    <h2 className='text-2xl font-bold text-blue-800'>

                      {flight.flight_name}

                    </h2>

                    <p className='text-gray-600 mt-1'>

                      {flight.source}
                      {' → '}
                      {flight.destination}

                    </p>

                  </div>

                  <div className='mt-3 md:mt-0 bg-gray-100 px-4 py-2 rounded-xl'>

                    <p className='text-xs text-gray-500'>
                      Departure
                    </p>

                    <p className='font-semibold'>
                      {flight.departure_time}
                    </p>

                  </div>

                </div>

                {/* HORIZONTAL SEAT CARDS */}
                <div className='overflow-x-auto'>

                  <div className='flex gap-4 min-w-max'>

                    {/* ECONOMY */}
                    <div className='w-64 bg-blue-50 rounded-2xl p-4 flex-shrink-0'>

                      <h3 className='text-lg font-bold text-blue-800'>
                        Economy
                      </h3>

                      <p className='mt-3 text-gray-700'>

                        Available Seats:
                        {' '}
                        <span className='font-bold'>
                          {flight.available_economy}
                        </span>

                      </p>

                      <button
                        onClick={() =>
                          bookTicket(
                            flight.schedule_id,
                            'Economy'
                          )
                        }
                        className='w-full mt-4 bg-blue-700 hover:bg-blue-800 text-white py-2 rounded-xl'
                      >
                        Book Now
                      </button>

                    </div>

                    {/* BUSINESS */}
                    <div className='w-64 bg-green-50 rounded-2xl p-4 flex-shrink-0'>

                      <h3 className='text-lg font-bold text-green-800'>
                        Business
                      </h3>

                      <p className='mt-3 text-gray-700'>

                        Available Seats:
                        {' '}
                        <span className='font-bold'>
                          {flight.available_business}
                        </span>

                      </p>

                      <button
                        onClick={() =>
                          bookTicket(
                            flight.schedule_id,
                            'Business'
                          )
                        }
                        className='w-full mt-4 bg-green-700 hover:bg-green-800 text-white py-2 rounded-xl'
                      >
                        Book Now
                      </button>

                    </div>

                    {/* FIRST CLASS */}
                    <div className='w-64 bg-purple-50 rounded-2xl p-4 flex-shrink-0'>

                      <h3 className='text-lg font-bold text-purple-800'>
                        First Class
                      </h3>

                      <p className='mt-3 text-gray-700'>

                        Available Seats:
                        {' '}
                        <span className='font-bold'>
                          {flight.available_first_class}
                        </span>

                      </p>

                      <button
                        onClick={() =>
                          bookTicket(
                            flight.schedule_id,
                            'First Class'
                          )
                        }
                        className='w-full mt-4 bg-purple-700 hover:bg-purple-800 text-white py-2 rounded-xl'
                      >
                        Book Now
                      </button>

                    </div>

                  </div>

                </div>

              </div>
            ))
          }

        </div>

      </div>

    </div>
  )
}

export default SearchFlights