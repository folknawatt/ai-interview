export const useApi = () => {
  const { $api, $externalApi } = useNuxtApp()

  return {
    api: $api,
    externalApi: $externalApi,
  }
}
