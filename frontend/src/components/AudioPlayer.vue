<template>
  <div class="audio-player bg-white rounded-xl border border-gray-100 p-3 shadow-sm">
    <div class="flex items-center gap-3">
      <!-- 播放/暂停按钮 -->
      <button
        class="w-10 h-10 rounded-full bg-red-primary flex items-center justify-center text-white shadow shrink-0"
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
        <div class="font-medium text-sm text-gray-800 truncate">{{ guide.title }}</div>
        <div class="text-xs text-gray-400 mt-0.5">
          {{ formatTime(isCurrentPlaying ? audioStore.currentTime : 0) }} / {{ formatTime(guide.duration) }}
        </div>
        <!-- 进度条 -->
        <div class="w-full h-1 bg-gray-200 rounded-full mt-1.5 overflow-hidden">
          <div
            class="h-full bg-red-primary rounded-full transition-all"
            :style="{ width: isCurrentPlaying ? audioStore.progress + '%' : '0%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- 文字稿（可展开） -->
    <div v-if="guide.transcript" class="mt-2">
      <button class="text-xs text-red-primary" @click="showTranscript = !showTranscript">
        {{ showTranscript ? '收起文字稿 ▲' : '查看文字稿 ▼' }}
      </button>
      <p v-if="showTranscript" class="text-xs text-gray-500 leading-relaxed mt-1 bg-gray-50 rounded p-2">
        {{ guide.transcript }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAudioStore } from '@/stores/audio'

const props = defineProps({
  guide: { type: Object, required: true },
})

const audioStore = useAudioStore()
const showTranscript = ref(false)

const isCurrentPlaying = computed(() => {
  return audioStore.isPlaying && audioStore.currentGuide?.id === props.guide.id
})

function formatTime(seconds) {
  const s = Math.floor(seconds || 0)
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}
</script>
