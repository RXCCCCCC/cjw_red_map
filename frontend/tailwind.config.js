/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'red-primary': '#C41E24',
        'red-dark': '#8B0000',
        'gold': '#D4A843',
      },
    },
  },
  plugins: [],
}
