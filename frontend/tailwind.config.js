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
      colors: {
        minimal: {
          bg: '#f8fafc',        // slate-50 - main background (reduces eye strain vs pure white)
          card: '#ffffff',      // white - card backgrounds
          border: '#e2e8f0',    // slate-200 - soft borders
          text: {
            primary: '#1e293b',   // slate-800 - main text
            secondary: '#64748b', // slate-500 - secondary text
            muted: '#94a3b8',     // slate-400 - muted text
          },
          focus: '#334155',     // slate-700 - focus state for "Start Answer" button
          warning: '#dc2626',   // red-600 - warning/recording state
          success: '#10b981',   // emerald-500 - success states
          info: '#0ea5e9',      // sky-500 - info states
          accent: {
            blue: '#7dd3fc',    // sky-300 - soft blue accent
            green: '#86efac',   // green-300 - soft green accent
            gray: '#cbd5e1',    // slate-300 - soft gray accent
          }
        }
      }
    },
  },
  plugins: [],
}

