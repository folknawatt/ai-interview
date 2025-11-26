<template>
    <div class="container mx-auto p-8">
        <h1 class="text-3xl font-bold mb-6">Fetch API Example</h1>

        <div class="bg-white shadow-md rounded-lg p-6">
            <p class="mb-4 text-gray-600">
                This page demonstrates how to use the configured Axios instance
                via the <code>useApi</code> composable.
            </p>

            <div class="flex gap-4 mb-6">
                <button
                    @click="fetchData"
                    class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                    :disabled="loading"
                >
                    {{ loading ? 'Loading...' : 'Fetch Data' }}
                </button>
            </div>

            <div
                v-if="error"
                class="bg-red-50 text-red-600 p-4 rounded-lg mb-4"
            >
                {{ error }}
            </div>

            <div
                v-if="data"
                class="bg-gray-50 p-4 rounded-lg border border-gray-200"
            >
                <h3 class="font-semibold mb-2">Response Data:</h3>
                <pre class="overflow-auto max-h-96 text-sm">{{
                    JSON.stringify(data, null, 2)
                }}</pre>
            </div>

            <div v-else-if="!loading && !error" class="text-gray-500 italic">
                Click the button to fetch data.
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
const { api } = useApi()

const data = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const fetchData = async () => {
    loading.value = true
    error.value = null
    data.value = null

    try {
        // Replace '/example-endpoint' with your actual API endpoint
        // For demonstration, we'll try to fetch the current user profile or a public resource
        const response = await api.get('/users/me')
        data.value = response.data
    } catch (err: any) {
        console.error('Fetch error:', err)
        error.value =
            err.response?.data?.message ||
            err.message ||
            'An error occurred while fetching data'
    } finally {
        loading.value = false
    }
}
</script>
