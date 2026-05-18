import { useEffect, useState } from 'react'

import Navbar from '../components/Navbar'

import API from '../services/api'

function Reservations() {

  const [reservations, setReservations] =
    useState([])

  const fetchReservations = async () => {

    try {

      const response = await API.get(

        `/reservations/${
          localStorage.getItem('userId')
        }`
      )

      setReservations(response.data)

    } catch (error) {

      console.log(error)
    }
  }

  useEffect(() => {

    fetchReservations()

  }, [])

  const cancelReservation = async (id) => {

    try {

      await API.delete(`/cancel/${id}`)

      alert('Reservation Cancelled')

      fetchReservations()

    } catch (error) {

      alert('Cancellation Failed')
    }
  }

  return (

    <div className='min-h-screen bg-gray-100'>

      <Navbar />

      <div className='p-10'>

        <h1 className='text-4xl font-bold mb-8'>
          My Reservations
        </h1>

        <div className='grid gap-6'>

          {
            reservations.map((reservation) => (

              <div
                key={reservation.reservation_id}
                className='bg-white rounded-xl shadow-lg p-6'
              >

                <h2 className='text-2xl font-bold'>

                  Reservation #
                  {reservation.reservation_id}

                </h2>

                <p>
                  Class:
                  {' '}
                  {reservation.travel_class}
                </p>

                <p>
                  Seats:
                  {' '}
                  {reservation.seats_booked}
                </p>

                <p>
                  Amount:
                  {' '}
                  ₹{reservation.total_amount}
                </p>

                <button
                  onClick={() =>
                    cancelReservation(
                      reservation.reservation_id
                    )
                  }
                  className='bg-red-600 text-white px-5 py-2 rounded-lg mt-4'
                >
                  Cancel Reservation
                </button>

              </div>
            ))
          }

        </div>

      </div>

    </div>
  )
}

export default Reservations