<template>
  <div class="navbar flex items-center h-11 px-4 bg-red-primary text-white sticky top-0 z-50 shadow">
    <button
      v-if="showBack"
      class="mr-2 w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/15 transition"
      @click="goBack"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
    </button>
    <h1 class="text-base font-semibold flex-1 truncate">{{ title }}</h1>
    <router-link to="/" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/15 transition">
      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
        <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
      </svg>
    </router-link>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
})

const router = useRouter()
const route = useRoute()
const showBack = computed(() => route.path !== '/')

function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>
