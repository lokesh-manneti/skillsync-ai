import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";

function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between h-16">
          {/* Logo and Brand Name */}
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="text-2xl font-bold">
              {/* Your brand gradient! */}
              <span className="bg-gradient-to-r from-ocean-blue to-royal-purple text-transparent bg-clip-text">
                SkillSync AI
              </span>
            </Link>
          </div>

          {/* Nav Links */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              // Links when LOGGED IN
              <>
                <Link
                  to="/dashboard"
                  className="text-gray-500 hover:text-ocean-blue px-3 py-2 rounded-md text-sm font-medium"
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-500 hover:text-ocean-blue px-3 py-2 rounded-md text-sm font-medium"
                >
                  Logout
                </button>
              </>
            ) : (
              // Links when LOGGED OUT
              <>
                <Link
                  to="/login"
                  className="text-gray-500 hover:text-ocean-blue px-3 py-2 rounded-md text-sm font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="text-white bg-ocean-blue hover:bg-royal-purple px-4 py-2 rounded-md text-sm font-medium shadow"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
