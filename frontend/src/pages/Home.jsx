import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-100px)] text-center px-4">
      {/* Hero Section */}
      <main>
        <h1 className="text-5xl md:text-6xl font-bold mb-6">
          {/* The brand gradient on the hero text */}
          <span className="bg-gradient-to-r from-ocean-blue to-royal-purple text-transparent bg-clip-text">
            SkillSync AI
          </span>
        </h1>

        {/* Your Tagline */}
        <p className="text-2xl md:text-3xl font-semibold text-dark-700 mb-8">
          Align your skills. Accelerate your career.
        </p>

        <p className="text-lg text-gray-500 max-w-2xl mx-auto mb-10">
          From resume to roadmap—instantly. Our AI-powered navigator analyzes
          your resume against live job roles, finds your skill gaps, and builds
          you a personalized learning path.
        </p>

        {/* Call to Action */}
        <div className="space-x-4">
          <Link
            to="/register"
            className="px-8 py-3 text-white font-semibold rounded-lg shadow-md
                       bg-gradient-to-r from-ocean-blue to-royal-purple 
                       hover:from-ocean-blue hover:to-ocean-blue
                       transition duration-300"
          >
            Get Started for Free
          </Link>
        </div>
      </main>
    </div>
  );
}

export default Home;
