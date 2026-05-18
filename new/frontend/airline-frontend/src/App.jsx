import { Routes, Route } from 'react-router-dom'

import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import SearchFlights from './pages/SearchFlights'
import Reservations from './pages/Reservations'

function App() {

  return (

    <Routes>

      <Route path='/' element={<Login />} />

      <Route path='/register' element={<Register />} />

      <Route path='/dashboard' element={<Dashboard />} />

      <Route path='/search' element={<SearchFlights />} />

      <Route path='/reservations' element={<Reservations />} />

    </Routes>
  )
}

export default App