<template>
  <div class="audio-player bg-white rounded-xl border border-gray-100 p-3 shadow-sm">
    <div class="flex items-start gap-3">
      <!-- 播放/暂停按钮 -->
      <button
        class="w-10 h-10 rounded-full bg-red-primary flex items-center justify-center text-white shadow shrink-0 mt-0.5"
        @click="audioStore.toggle(guide)"
      >
        <svg v-if="isCurrentPlaying" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>
        </svg>
        <svg v-else class="w-4 h-4 ml-0.5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>

      <div class="flex-1 min-w-0">
        <div class="font-medium text-sm text-gray-800">{{ guide.title }}</div>
        <!-- 文字稿一直显示 -->
        <p v-if="guide.transcript" class="text-xs text-gray-500 leading-relaxed mt-2 bg-gray-50 rounded p-2">
          {{ guide.transcript }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAudioStore } from '@/stores/audio'

const props = defineProps({
  guide: { type: Object, required: true },
})

const audioStore = useAudioStore()

const isCurrentPlaying = computed(() => {
  return audioStore.isPlaying && audioStore.currentGuide?.id === props.guide.id
})
</script>
