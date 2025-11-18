import React from "react";
import { Link } from "react-router-dom";

function AuthLayout({ children, title, footerLink, footerText }) {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-gray-50 flex flex-col justify-center items-center py-12 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white shadow-xl rounded-lg px-8 pt-10 pb-8 mb-4">
          <h2 className="text-center text-3xl font-bold text-dark-900 mb-8">
            {title}
          </h2>

          {/* Form content goes here */}
          {children}
        </div>
        <p className="text-center text-gray-500 text-sm">
          {footerText}
          <Link
            to={footerLink}
            className="font-medium text-ocean-blue hover:text-royal-purple ml-1"
          >
            {footerLink === "/login" ? "Sign in" : "Sign up"}
          </Link>
        </p>
      </div>
    </div>
  );
}

export default AuthLayout;
