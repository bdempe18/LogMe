/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../template/**/*.html',
    './node_modules/flowbite/**/*.js'

  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
