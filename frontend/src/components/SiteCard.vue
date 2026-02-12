<template>
  <div
    class="site-card flex items-center gap-3 bg-white rounded-xl p-3 shadow-sm border border-gray-100 active:bg-gray-50 cursor-pointer"
    @click="$emit('click', site)"
  >
    <!-- 图标 -->
    <div class="w-11 h-11 rounded-full bg-red-primary/10 flex items-center justify-center text-xl shrink-0">
      {{ icon }}
    </div>
    <!-- 信息 -->
    <div class="flex-1 min-w-0">
      <div class="font-semibold text-sm text-gray-800 truncate">{{ site.name }}</div>
      <div class="text-xs text-gray-400 mt-0.5">{{ site.category }}</div>
    </div>
    <!-- 箭头 -->
    <svg class="w-4 h-4 text-gray-300 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  site: { type: Object, required: true },
})

defineEmits(['click'])

const icon = computed(() => {
  const map = { '医院': '🏥', '军事设施': '🔫', '道路': '🛤️', '地标': '📍' }
  return map[props.site.category] || '📍'
})
</script>
