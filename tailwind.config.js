/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/forms.py',  // Add this if you're using form classes
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

