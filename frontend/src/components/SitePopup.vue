<template>
  <div class="site-popup-content p-1">
    <h4 class="text-red-primary font-bold text-sm">{{ site.name }}</h4>
    <p class="text-gray-500 text-xs mt-1">{{ site.category }}</p>
    <p class="text-gray-600 text-xs mt-2 leading-relaxed">
      {{ (site.description || '').substring(0, 80) }}...
    </p>
    <button
      class="mt-2 text-xs text-white bg-red-primary rounded-full px-3 py-1"
      @click="$emit('detail', site)"
    >
      查看详情
    </button>
  </div>
</template>

<script setup>
defineProps({
  site: { type: Object, required: true },
})
defineEmits(['detail'])
</script>
