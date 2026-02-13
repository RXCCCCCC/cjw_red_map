<template>
  <div class="site-detail min-h-screen bg-gray-50">
    <NavBar :title="site?.name || '地标详情'" />

    <div v-if="loading" class="flex items-center justify-center h-64">
      <van-loading type="spinner" color="#C41E24" />
    </div>

    <template v-else-if="site">
      <!-- 封面图区域 -->
      <div class="relative h-48 bg-red-dark flex items-center justify-center overflow-hidden">
        <img
          v-if="site.cover_image"
          :src="site.cover_image"
          class="w-full h-full object-cover"
          :alt="site.name"
        />
        <div v-else class="text-white/40 text-6xl">🏛️</div>
        <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
          <span class="inline-block px-2 py-0.5 bg-gold text-white text-xs rounded-full mb-1">
            {{ site.category }}
          </span>
          <h1 class="text-white text-xl font-bold">{{ site.name }}</h1>
        </div>
      </div>

      <!-- 简介 -->
      <section class="px-4 py-4">
        <h3 class="text-red-primary font-semibold text-base mb-2 flex items-center gap-1">
          📜 地标简介
        </h3>
        <p class="text-gray-600 text-sm leading-relaxed">{{ site.description }}</p>
      </section>
      
      <van-divider />

      <!-- 语音导览 -->
      <section class="px-4 pb-3" v-if="site.audio_guides?.length">
        <h3 class="text-red-primary font-semibold text-base mb-3 flex items-center gap-1">
          🎧 语音导览
        </h3>
        <div class="space-y-3">
          <AudioPlayer
            v-for="guide in site.audio_guides"
            :key="guide.id"
            :guide="guide"
          />
        </div>
      </section>

      <van-divider />

      <!-- 地标图片 -->
      <section class="px-4 pb-3" v-if="images.length">
        <h3 class="text-red-primary font-semibold text-base mb-3 flex items-center gap-1">
          🖼️ 地标图片
        </h3>
        <div class="grid grid-cols-2 gap-2">
          <div
            v-for="m in images"
            :key="m.id"
            class="rounded-lg overflow-hidden bg-gray-200 aspect-video flex items-center justify-center"
          >
            <img v-if="m.url" :src="m.url" class="w-full h-full object-cover" :alt="m.title" />
            <span v-else class="text-gray-400 text-xs">暂无图片</span>
          </div>
        </div>
      </section>

      <!-- 底部操作栏 -->
      <div class="sticky bottom-0 bg-white border-t px-4 py-3 flex gap-3 z-10">
        <van-button
          round
          type="primary"
          color="#C41E24"
          class="flex-1"
          @click="$router.push('/map')"
        >
          🗺️ 查看地图
        </van-button>
        <van-button
          round
          type="default"
          class="flex-1"
          @click="$router.push('/model3d')"
        >
          🏔️ 三维模型
        </van-button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSiteStore } from '@/stores/site'
import { storeToRefs } from 'pinia'
import NavBar from '@/components/NavBar.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'

const route = useRoute()
const siteStore = useSiteStore()
const { currentSite: site, loading } = storeToRefs(siteStore)

const images = computed(() => {
  return (site.value?.media || []).filter((m) => m.type === 'image')
})

function loadSite() {
  const id = Number(route.params.id)
  if (id) siteStore.fetchSite(id)
}

onMounted(loadSite)
watch(() => route.params.id, loadSite)
</script>
