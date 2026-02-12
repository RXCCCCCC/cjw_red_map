import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAudioStore = defineStore('audio', () => {
  const audioEl = ref(null)
  const isPlaying = ref(false)
  const currentTime = ref(0)
  const duration = ref(0)
  const currentGuide = ref(null)

  function play(guide) {
    if (!audioEl.value) {
      audioEl.value = new Audio()
      audioEl.value.addEventListener('timeupdate', () => {
        currentTime.value = audioEl.value.currentTime
      })
      audioEl.value.addEventListener('loadedmetadata', () => {
        duration.value = audioEl.value.duration
      })
      audioEl.value.addEventListener('ended', () => {
        isPlaying.value = false
      })
    }

    if (currentGuide.value?.id !== guide.id) {
      audioEl.value.src = guide.audio_url
      currentGuide.value = guide
    }

    audioEl.value.play()
    isPlaying.value = true
  }

  function pause() {
    audioEl.value?.pause()
    isPlaying.value = false
  }

  function toggle(guide) {
    if (isPlaying.value && currentGuide.value?.id === guide.id) {
      pause()
    } else {
      play(guide)
    }
  }

  function seek(time) {
    if (audioEl.value) {
      audioEl.value.currentTime = time
    }
  }

  const progress = computed(() => {
    if (!duration.value) return 0
    return (currentTime.value / duration.value) * 100
  })

  return { isPlaying, currentTime, duration, currentGuide, progress, play, pause, toggle, seek }
})
