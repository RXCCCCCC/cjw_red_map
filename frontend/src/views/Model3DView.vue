<template>
  <div class="model3d-page h-screen flex flex-col">
    <NavBar title="三维模型" />
    <div class="flex-1 relative">
      <CesiumViewer />
      <!-- 右下角按钮组 -->
      <div class="absolute bottom-6 right-4 z-10 flex flex-col gap-3">
        <button
          class="w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center text-red-primary"
          @click="showNavigation"
          title="路径导航"
        >
          🧭
        </button>
        <button
          class="w-10 h-10 rounded-full bg-white shadow-lg flex items-center justify-center text-red-primary"
          @click="resetView"
          title="重置视角"
        >
          🔄
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { provide, ref } from 'vue'
import NavBar from '@/components/NavBar.vue'
import CesiumViewer from '@/components/CesiumViewer.vue'

const resetViewFn = ref(null)
const showNavigationFn = ref(null)

provide('registerResetView', (fn) => { resetViewFn.value = fn })
provide('registerShowNavigation', (fn) => { showNavigationFn.value = fn })

function resetView() {
  resetViewFn.value?.()
}

function showNavigation() {
  showNavigationFn.value?.()
}
</script>
