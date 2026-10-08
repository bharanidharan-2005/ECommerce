/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        // Inter everywhere — the design system's single typeface
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        // Design tokens from the spec
        surface: "#F9FAFB", // off-white app background (gray-50)
        card: "#FFFFFF",    // pure white product cards
      },
      boxShadow: {
        // Resting / hover elevation for the "floating" bento cards
        float: "0 1px 3px rgba(16,24,40,.06), 0 1px 2px rgba(16,24,40,.04)",
        "float-lg": "0 12px 32px -8px rgba(16,24,40,.14), 0 4px 8px rgba(16,24,40,.04)",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: 0, transform: "translateY(8px)" },
          to: { opacity: 1, transform: "translateY(0)" },
        },
      },
      animation: { fadeIn: "fadeIn .35s ease-out" },
    },
  },
  plugins: [],
};
