import React from "react";

function FormInput({ id, label, type = "text", value, onChange, ...props }) {
  return (
    <div className="mb-4">
      <label
        htmlFor={id}
        className="block text-sm font-medium text-gray-500 mb-1"
      >
        {label}
      </label>
      <input
        id={id}
        name={id}
        type={type}
        value={value}
        onChange={onChange}
        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm 
                   placeholder-gray-400 focus:outline-none focus:ring-ocean-blue 
                   focus:border-ocean-blue sm:text-sm"
        {...props}
      />
    </div>
  );
}

export default FormInput;
