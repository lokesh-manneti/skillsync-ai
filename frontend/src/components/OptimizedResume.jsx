import React, { useState } from "react";

function OptimizedResume({ resume }) {
  const [copySuccess, setCopySuccess] = useState("");

  if (!resume) return null;

  const textToCopy = resume.optimized_resume_text;

  const handleCopy = () => {
    navigator.clipboard.writeText(textToCopy).then(
      () => {
        setCopySuccess("Copied to clipboard!");
        setTimeout(() => setCopySuccess(""), 2000); // Clear message
      },
      () => {
        setCopySuccess("Failed to copy.");
      }
    );
  };

  return (
    <div>
      <h3 className="text-lg font-semibold text-dark-700 mb-2">
        Your ATS-Optimized Resume:
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        Copy this plain text and paste it into your resume template or job
        application fields.
      </p>

      {/* FIX 1: Replaced <textarea> with <pre>.
        This will respect all whitespace from the AI 
        and grow to fit the content, up to a max height.
      */}
      <pre
        className="block w-full max-h-[600px] overflow-auto p-4 border border-gray-300 rounded-md 
                   font-mono text-sm text-dark-700 bg-gray-50 whitespace-pre-wrap"
      >
        {textToCopy}
      </pre>

      <div className="mt-4 flex items-center">
        {/* FIX 2: Replaced <FormButton> with a standard <button type="button">
          so it doesn't try to submit a form.
        */}
        <button
          type="button"
          onClick={handleCopy}
          className="py-2 px-4 border border-transparent rounded-md shadow-sm 
                     text-sm font-medium text-white 
                     bg-gradient-to-r from-ocean-blue to-royal-purple 
                     hover:from-ocean-blue hover:to-ocean-blue 
                     focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ocean-blue
                     transition duration-300"
        >
          Copy to Clipboard
        </button>
        {copySuccess && (
          <span className="ml-4 text-sm font-medium text-mint-green">
            {copySuccess}
          </span>
        )}
      </div>
    </div>
  );
}

export default OptimizedResume;
