/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.{vue,js,ts}',
    './pages/**/*.{vue,js,ts}',
    './composables/**/*.{js,ts}',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Urbanist', 'Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        // InterviewPro-style dark theme
        interview: {
          // Backgrounds
          bg: {
            DEFAULT: '#0a0a0f',     // Deep dark background
            secondary: '#12121a',   // Slightly lighter for sections
            gradient: '#1a1a2e',    // Gradient end color
          },
          backgroundImage: {
            'radial-vignette': 'radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.8) 100%)',
          },
          // Card surfaces (glassmorphism)
          surface: {
            DEFAULT: 'rgb(255 255 255 / 0.05)',
            hover: 'rgb(255 255 255 / 0.08)',
            border: 'rgb(255 255 255 / 0.05)',
          },
          // Primary accent - Amber/Orange (InterviewPro signature color)
          primary: {
            DEFAULT: '#FFC428',     // Main amber from palette
            hover: '#E5B024',       // Darker amber for hover
            light: '#FFD93D',       // Light amber for highlights
            glow: ({ opacityValue }) => opacityValue !== undefined ? `rgba(255, 196, 40, ${opacityValue})` : 'rgba(255, 196, 40, 0.3)',  // Glow effect
          },
          // Text colors
          text: {
            primary: '#ffffff',     // White text
            secondary: '#a1a1aa',   // Muted gray
            muted: '#71717a',       // Even more muted
          },
          // Muted accent palette (from InterviewPro reference)
          accent: {
            teal: '#A1D8C1',        // Muted teal
            rose: '#DCACAF',        // Muted rose
            sky: '#ACD7DC',         // Muted sky blue
            olive: '#DCD7AC',       // Muted olive
          },
          // Status colors
          success: '#22c55e',       // Green
          warning: '#ef4444',       // Red
          info: '#3b82f6',          // Blue
        },
        // Keep minimal for backwards compatibility during transition
        minimal: {
          bg: '#0a0a0f',
          card: 'rgba(255, 255, 255, 0.05)',
          border: 'rgba(255, 255, 255, 0.1)',
          text: {
            primary: '#ffffff',
            secondary: '#a1a1aa',
            muted: '#71717a',
          },
          focus: '#FFB128',
          warning: '#ef4444',
          success: '#22c55e',
          info: '#FFB128',
        }
      },
      // Animation keyframes
      keyframes: {
        'fade-in-up': {
          '0%': { 
            opacity: '0', 
            transform: 'translate3d(0, 20px, 0)',
          },
          '100%': { 
            opacity: '1', 
            transform: 'translate3d(0, 0, 0)',
          },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'glow-pulse': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(255, 196, 40, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(255, 196, 40, 0.5)' },
        },
        'float': {
          '0%, 100%': { transform: 'translate3d(0, 0, 0)' },
          '50%': { transform: 'translate3d(0, -10px, 0)' },
        },
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        'fade-in': 'fade-in 0.3s ease-out forwards',
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      // Backdrop blur
      backdropBlur: {
        xs: '2px',
      },
      // Box shadow with glow
      boxShadow: {
        'glow-amber': '0 0 30px rgba(255, 196, 40, 0.2)',
        'glow-amber-lg': '0 0 60px rgba(255, 196, 40, 0.3)',
        'glass': '0 8px 32px rgba(0, 0, 0, 0.3)',
      },
    },
  },
  plugins: [],
}

