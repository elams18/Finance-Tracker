/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')
module.exports = {
  content: ["./blueprints/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      }
    },
  },
  plugins: [
      require('@tailwindcss/forms'),
      require('tailwindcss')(path.resolve(__dirname, 'tailwind.config.js')),
      require('autoprefixer'),
      process.env.FLASK_PROD === 'production' && require('@fullhuman/postcss-purgecss')({
      content: [
        path.resolve(__dirname, 'templates/**/*.html')
      ],
      defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
    })
  ],
}