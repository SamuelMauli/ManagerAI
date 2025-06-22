/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          background: '#0D0C12', 
          primary: '#1A1920',    
          card: 'rgba(26, 25, 32, 0.7)',
          text: '#F0F2F5',
          'text-secondary': '#A0AEC0',
          accent: '#8A4FFF',
          'accent-hover': '#7a45e0',
        },
        light: {
          background: '#F0F2F5',
          primary: '#FFFFFF',
          card: 'rgba(255, 255, 255, 0.8)',
          text: '#1A202C',
          'text-secondary': '#4A5568',
          accent: '#6B46C1',
          'accent-hover': '#553c9a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      backdropBlur: {
        'xl': '24px',
      }
    },
  },
  plugins: [],
};