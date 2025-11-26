<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gray-900 text-white"
  >
    <p>Redirecting...</p>
  </div>
</template>

<script setup lang="ts">
const router = useRouter();
onMounted(() => {
  router.push("/login");
});
</script>
