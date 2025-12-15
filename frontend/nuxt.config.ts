// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
    
    // Path aliases for cleaner imports
    alias: {
        '@': '/<rootDir>',
        '~': '/<rootDir>',
        '@components': '/<rootDir>/components',
        '@composables': '/<rootDir>/composables',
        '@services': '/<rootDir>/services',
        '@types': '/<rootDir>/types',
        '@store': '/<rootDir>/store',
    },
    
    runtimeConfig: {
        public: {
            apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
        }
    }
})
