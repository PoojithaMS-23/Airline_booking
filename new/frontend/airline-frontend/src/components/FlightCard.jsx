function FlightCard({ flight, onBook }) {

  return (

    <div className='bg-white shadow-lg rounded-xl p-5 border'>

      <h2 className='text-2xl font-bold text-blue-700'>
        {flight.flight_name}
      </h2>

      <p className='mt-2'>
        {flight.source} → {flight.destination}
      </p>

      <p>
        Departure: {flight.departure_time}
      </p>

      <div className='grid grid-cols-3 gap-4 mt-5'>

        <div className='border rounded-lg p-3'>
          <h3 className='font-bold'>Economy</h3>
          <p>Seats: {flight.available_economy}</p>
          <button
            onClick={() => onBook(flight, 'Economy')}
            className='bg-blue-600 text-white px-4 py-2 rounded mt-2'
          >
            Book
          </button>
        </div>

        <div className='border rounded-lg p-3'>
          <h3 className='font-bold'>Business</h3>
          <p>Seats: {flight.available_business}</p>
          <button
            onClick={() => onBook(flight, 'Business')}
            className='bg-green-600 text-white px-4 py-2 rounded mt-2'
          >
            Book
          </button>
        </div>

        <div className='border rounded-lg p-3'>
          <h3 className='font-bold'>First Class</h3>
          <p>Seats: {flight.available_first_class}</p>
          <button
            onClick={() => onBook(flight, 'First Class')}
            className='bg-purple-600 text-white px-4 py-2 rounded mt-2'
          >
            Book
          </button>
        </div>

      </div>
    </div>
  )
}

export default FlightCard