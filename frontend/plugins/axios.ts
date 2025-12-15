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
    })

    let isRefreshing = false
    let failedQueue: Array<{
        resolve: (value?: unknown) => void
        reject: (reason?: unknown) => void
    }> = []

    function processQueue(error: unknown, token: string | null = null) {
        failedQueue.forEach((prom) => {
            if (error) {
                prom.reject(error)
            } else {
                prom.resolve(token)
            }
        })
        failedQueue = []
    }

    instance.interceptors.request.use(
        function (config) {
            if (auth.bearerToken) {
                config.headers['Authorization'] = auth.bearerToken
            }
            return config
        },
        function (error) {
            return Promise.reject(error)
        }
    )

    instance.interceptors.response.use(
        (response: AxiosResponse) => response,
        async (error) => {
            const originalRequest = error.config

            if (
                error.response &&
                error.response.status === 401 &&
                !originalRequest._retry
            ) {
                if (isRefreshing) {
                    return new Promise((resolve, reject) => {
                        failedQueue.push({ resolve, reject })
                    })
                        .then((token) => {
                            originalRequest.headers['Authorization'] = token
                            return instance(originalRequest)
                        })
                        .catch((err) => {
                            return Promise.reject(err)
                        })
                }

                originalRequest._retry = true
                isRefreshing = true

                try {
                    await auth.handleRefreshToken()

                    instance.defaults.headers.common['Authorization'] =
                        auth.bearerToken
                    processQueue(null, auth.bearerToken)
                    originalRequest.headers['Authorization'] = auth.bearerToken
                    return instance(originalRequest)
                } catch (err) {
                    processQueue(err, null)
                    auth.clearToken()
                    router.push('/login')
                    return Promise.reject(err)
                } finally {
                    isRefreshing = false
                }
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
