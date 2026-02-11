/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#059669', // Emerald green - safety/cycling
          dark: '#047857',
          light: '#10b981',
        },
        secondary: {
          DEFAULT: '#fbbf24', // Amber - visibility/safety vest
          dark: '#f59e0b',
          light: '#fcd34d',
        },
        accent: {
          DEFAULT: '#0ea5e9', // Sky blue - clear skies
          dark: '#0284c7',
        },
      },
      fontFamily: {
        heading: ['system-ui', 'sans-serif'],
        body: ['system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
