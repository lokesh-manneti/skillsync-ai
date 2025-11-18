/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Tells Tailwind to scan all our component files
  ],
  theme: {
    // We extend the theme to add your brand identity
    extend: {
      fontFamily: {
        // As per your guide: 'Inter' family
        sans: ["Inter", "sans-serif"],
      },
      colors: {
        // As per your guide: Primary Colors
        "ocean-blue": "#2563EB",
        "royal-purple": "#7C3AED",

        // As per your guide: Secondary Colors
        "sky-blue": "#38BDF8",
        "mint-green": "#10B981",

        // As per your guide: Neutrals
        "dark-900": "#0F172A",
        "dark-700": "#1E293B",
        "gray-500": "#64748B",
        "gray-300": "#CBD5E1",

        // As per your guide: Status Colors
        "error-red": "#EF4444",
        "warning-amber": "#F59E0B",
      },
    },
  },
  plugins: [],
};
