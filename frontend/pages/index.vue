<template>
  <div
    class="flex items-center justify-center min-h-screen bg-interview-bg text-interview-text-primary"
  >
    <p class="text-interview-text-secondary">Redirecting...</p>
  </div>
</template>

<script setup lang="ts">
const router = useRouter();
onMounted(() => {
  router.push("/login");
});
</script>
