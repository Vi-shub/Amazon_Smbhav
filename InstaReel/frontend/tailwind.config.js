/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'ticker': 'ticker 5s linear infinite',
      },
       keyframes: {
        ticker: {
          '100%':{transform: 'translateX(-100%)'}
        }
      }
    },
  },
  plugins: [],
}

