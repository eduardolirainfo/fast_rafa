/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './fast_rafa/templates/*.html',
    './fast_rafa/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'custom-blue': '#007bff',
      },
      fontFamily: {
        'custom': ['Montserrat', 'sans-serif'],
      },
      spacing: {
        'custom': '36rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
   daisyui: {
    themes: true,
    darkTheme: "dark",
    base: true, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
    prefix: "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
    logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
    themeRoot: ":root", // The element that receives theme color CSS variables
	  }
}

