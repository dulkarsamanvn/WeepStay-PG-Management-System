import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import LoginPage from './pages/Auth/LoginPage'

function App() {
  return (
    <Router>
      <Toaster
        position="top-right"
        toastOptions={{
          success: {
            style: {
              background: 'linear-gradient(to right, #777C6D, #B7B89F)',
              color: 'white',
            },
          },
          error: {
            style: {
              background: 'linear-gradient(to right, #dc2626, #db2777)',
              color: 'white',
            },
          },
        }}
      />
      <Routes>
        <Route path='/login' element = {<LoginPage/>} />
      </Routes>
    </Router>
  )
}

export default App
