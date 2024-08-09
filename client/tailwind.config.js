module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      keyframes: {
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
      },
    },
    animation: {
      fadeIn: "fadeIn 0.5s ease-in",
    },
  },

  variants: {
    extend: {},
  },
  plugins: [require('@tailwindcss/typography'),],
};
