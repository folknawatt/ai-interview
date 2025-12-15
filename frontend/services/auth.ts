import axios from 'axios'
import type { ApiResponse, LoginResponse } from '../types/api'
import { useRuntimeConfig } from '#app'

export const refreshToken = (token: string): ApiResponse<LoginResponse> => {
    const {
        public: { apiBaseUrl },
    } = useRuntimeConfig()

    return axios.post(`${apiBaseUrl}/auth/refresh-token`, {
        refreshToken: token,
    })
}
