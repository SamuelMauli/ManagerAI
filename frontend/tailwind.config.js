/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          background: '#111827', 
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
        // light: {
        //   background: '#f0f2f5', 
        //   primary: '#ffffff',   
        //   card: '#ffffff',
        //   text: '#1a202c',    
        //   'text-secondary': '#718096', 
        //   accent: '#3b82f6',    
        //   'accent-hover': '#2563eb', 
        //   border: '#e2e8f0',    
        // },
        // dark: {
        //   background: '#111827', 
        //   primary: '#1f2937',   
        //   card: '#1f2937',      
        //   text: '#f9fafb',     
        //   'text-secondary': '#9ca3af',
        //   accent: '#3b82f6',     
        //   'accent-hover': '#60a5fa',
        //   border: '#374151',     
