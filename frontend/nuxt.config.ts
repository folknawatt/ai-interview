import { fileURLToPath } from 'url'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    modules: [
        '@nuxtjs/tailwindcss',
        '@pinia/nuxt',
        '@nuxtjs/i18n'
    ],

    // i18n Configuration
    i18n: {
        lazy: true,
        langDir: 'locales',
        locales: [
            { code: 'th', name: 'ภาษาไทย', file: 'th.json' },
            { code: 'en', name: 'English', file: 'en.json' }
        ],
        defaultLocale: 'th',
        strategy: 'no_prefix',
        detectBrowserLanguage: {
            useCookie: true,
            cookieKey: 'i18n_redirected',
            redirectOn: 'root'
        }
    },
    
    // Global CSS
    css: ['~/assets/css/main.css'],

    // Add Google Fonts for premium typography
    app: {
        pageTransition: { name: 'page', mode: 'out-in' },
        layoutTransition: { name: 'layout', mode: 'out-in' },
        head: {
            link: [
                { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
                { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
                { 
                    rel: 'stylesheet', 
                    href: 'https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800&display=swap' 
                }

            ],
            style: [
                { innerHTML: 'body { background-color: #0a0a0f; color: #ffffff; }' }
            ]
        }
    },
    
    // PostCSS configuration (migrated from postcss.config.js)
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    },

    // Path aliases for cleaner imports
    alias: {
        '@': fileURLToPath(new URL('./', import.meta.url)),
        '~': fileURLToPath(new URL('./', import.meta.url)),
        '@components': fileURLToPath(new URL('./components', import.meta.url)),
        '@composables': fileURLToPath(new URL('./composables', import.meta.url)),
        '@types': fileURLToPath(new URL('./types', import.meta.url)),
        '@store': fileURLToPath(new URL('./store', import.meta.url)),
    },

    imports: {
        dirs: ['store']
    },
    
    runtimeConfig: {
        public: {
            apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
        }
    }
})
