export const useApi = () => {
    const { $axios, $externalApi } = useNuxtApp()

    return {
        api: $axios,
        externalApi: $externalApi,
    }
}
