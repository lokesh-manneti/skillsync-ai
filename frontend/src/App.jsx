import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home"; // <-- Import Home
import Navbar from "./components/Navbar"; // <-- Import Navbar
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./components/AuthProvider";

function App() {
  const { isAuthenticated } = useAuth();

  return (
    // We remove the old nav and use the new component
    <div className="min-h-screen bg-white">
      <Navbar /> {/* Navbar is now outside the Routes, so it's on every page */}
      <main>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} /> {/* New Landing Page */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
          {/* Fallback route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
