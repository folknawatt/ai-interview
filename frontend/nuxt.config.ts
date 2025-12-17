import { fileURLToPath } from 'url'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
    
    // Path aliases for cleaner imports
    alias: {
        '@': fileURLToPath(new URL('./', import.meta.url)),
        '~': fileURLToPath(new URL('./', import.meta.url)),
        '@components': fileURLToPath(new URL('./components', import.meta.url)),
        '@composables': fileURLToPath(new URL('./composables', import.meta.url)),
        '@services': fileURLToPath(new URL('./services', import.meta.url)),
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
