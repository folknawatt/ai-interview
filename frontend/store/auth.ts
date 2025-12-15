import { computed } from 'vue'
import { useStorage } from '@vueuse/core'
import { defineStore } from 'pinia'
import { refreshToken } from '../services/auth'

export const useAuth = defineStore('auth', () => {
    const tokenAuth = useStorage('token', '')
    const refreshTokenAuth = useStorage('refresh-token', '')

    const signInAuth = (token: string, refreshToken: string) => {
        tokenAuth.value = token
        refreshTokenAuth.value = refreshToken
    }

    const clearToken = () => {
        tokenAuth.value = ''
        refreshTokenAuth.value = ''
    }

    const bearerToken = computed(() => {
        if (!tokenAuth.value) {
            return ''
        }
        return `Bearer ${tokenAuth.value}`
    })

    const isLogin = computed(() => {
        return tokenAuth.value !== '' && refreshTokenAuth.value !== ''
    })

    const handleRefreshToken = async () => {
        const res = await refreshToken(refreshTokenAuth.value)

        if (res.data.error) {
            return
        }
        if (res.data.data?.item.accessToken) {
            signInAuth(
                res.data.data.item.accessToken,
                res.data.data.item.refreshToken
            )
        }
    }

    return {
        tokenAuth,
        refreshTokenAuth,
        signInAuth,
        clearToken,
        bearerToken,
        isLogin,
        handleRefreshToken,
    }
})
