/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      colors: {
        // Custom CSS variables for dynamic theming
        primary: {
          50: 'rgba(var(--color-primary-50), 0.1)',
          100: 'rgba(var(--color-primary-100), 0.2)',
          200: 'rgba(var(--color-primary), 0.3)',
          300: 'rgba(var(--color-primary), 0.5)',
          400: 'rgba(var(--color-primary), 0.7)',
          500: 'rgba(var(--color-primary), 1)',
          600: 'rgba(var(--color-primary-600), 1)',
          700: 'rgba(var(--color-primary-700), 1)',
          800: 'rgba(var(--color-primary-700), 1)',
          900: 'rgba(var(--color-primary-700), 1)',
        },
        accent: {
          500: 'rgba(var(--color-accent), 1)',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'bounce-subtle': 'bounceSubtle 0.6s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      screens: {
        'xs': '475px',
      },
    },
  },
  plugins: [],
}