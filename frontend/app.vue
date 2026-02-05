<script setup lang="ts">
import { useAuth } from '@/store/auth'

const authStore = useAuth()

onMounted(async () => {
  // Attempt to restore session
  try {
    await authStore.fetchUser()
  } catch (error) {
    // Session expired or invalid, user remains logged out
  }
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
