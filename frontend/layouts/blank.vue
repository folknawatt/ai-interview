<template>
  <div class="min-h-screen w-full overflow-x-hidden relative bg-interview-bg text-interview-text-primary">
    <!-- 2026 Trend: Cinematic Grain Overlay -->
    <!-- 2026 Trend: Cinematic Grain Overlay - Optimized -->
    <div class="fixed inset-0 z-50 pointer-events-none opacity-[0.02]" :style="{ backgroundImage: 'url(\'data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.8\' numOctaves=\'1\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E\')' }"></div>
    
    <!-- 2026 Trend: Vignette Focus -->
    <div class="fixed inset-0 z-40 pointer-events-none bg-radial-vignette opacity-40"></div>

    <slot />
  </div>
</template>

<script setup lang="ts">
// Blank layout for full-screen pages (Login, Interview, etc.)
</script>
