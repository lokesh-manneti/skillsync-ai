import React from "react";

function FormButton({ children, type = "submit", isLoading = false }) {
  return (
    <button
      type={type}
      disabled={isLoading}
      className={`w-full flex justify-center py-2 px-4 border border-transparent 
                  rounded-md shadow-sm text-sm font-medium text-white 
                  bg-gradient-to-r from-ocean-blue to-royal-purple 
                  hover:from-ocean-blue hover:to-ocean-blue 
                  focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ocean-blue
                  transition duration-300
                  ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      {isLoading ? "Processing..." : children}
    </button>
  );
}

export default FormButton;
