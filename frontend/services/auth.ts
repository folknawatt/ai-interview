import axios from 'axios'
import type { ApiResponse } from '~/types/services'
import type { LoginResponse } from '~/types/services/login'

export const refreshToken = (token: string): ApiResponse<LoginResponse> => {
    const {
        public: { apiBaseUrl },
    } = useRuntimeConfig()

    return axios.post(`${apiBaseUrl}/auth/refresh-token`, {
        refreshToken: token,
    })
}
