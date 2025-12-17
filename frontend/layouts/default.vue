<template>
  <div class="min-h-screen bg-minimal-bg">
    <!-- Simple header for public pages -->
    <header class="bg-minimal-card border-b border-minimal-border">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <NuxtLink to="/" class="text-2xl font-bold text-minimal-text-primary">
            AI Interview
          </NuxtLink>
          
          <nav class="flex items-center gap-4">
            <NuxtLink 
              to="/login" 
              class="text-minimal-text-secondary hover:text-minimal-text-primary transition-colors"
            >
              Login
            </NuxtLink>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="container mx-auto px-4 py-8">
      <slot />
    </main>

    <!-- Simple footer -->
    <footer class="bg-minimal-card border-t border-minimal-border mt-auto">
      <div class="container mx-auto px-4 py-6 text-center text-minimal-text-muted">
        <p>&copy; {{ new Date().getFullYear() }} AI Interview. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Default layout for public and candidate pages
// Minimal design with simple header and footer
</script>
