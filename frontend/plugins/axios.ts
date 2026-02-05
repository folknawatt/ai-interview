import axios from 'axios'
import type { AxiosResponse } from 'axios'
import { useAuth } from '../store/auth'

export default defineNuxtPlugin(() => {
    const {
        public: { apiBaseUrl },
    } = useRuntimeConfig()

    const auth = useAuth()
    const router = useRouter()
    const instance = axios.create({
        baseURL: apiBaseUrl as string,
        withCredentials: true, // Important for HttpOnly cookies
    })

    // Response interceptor for handling 401 errors
    instance.interceptors.response.use(
        (response: AxiosResponse) => response,
        async (error) => {
            // If we get 401, session expired - logout user
            if (error.response && error.response.status === 401) {
                // Clear user data and redirect to login
                await auth.logout()
                return Promise.reject(error)
            }

            return Promise.reject(error)
        }
    )

    return {
        provide: {
            axios: instance,
        },
    }
})
