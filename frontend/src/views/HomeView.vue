<template>
  <div class="home-page min-h-screen flex flex-col bg-gradient-to-b from-red-dark to-red-primary relative overflow-hidden">
    <!-- 装饰粒子 -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="star star-1"></div>
      <div class="star star-2"></div>
      <div class="star star-3"></div>
    </div>

    <!-- 顶部标题区域 -->
    <header class="flex-1 flex flex-col items-center justify-center text-center px-6 relative z-10">
      <div class="mb-4">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-white/15 backdrop-blur mb-4">
          <svg class="w-10 h-10 text-gold" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
          </svg>
        </div>
      </div>
      <h1 class="text-3xl font-bold text-white mb-2 tracking-wider">程家湾</h1>
      <h2 class="text-xl text-gold font-semibold mb-4">红色资源数字地图</h2>
      <p class="text-white/70 text-sm max-w-xs leading-relaxed">
        走访红军医院、炮台、红军路<br/>
        数字化呈现闽浙赣革命根据地红色记忆
      </p>
    </header>

    <!-- 功能入口 -->
    <nav class="relative z-10 px-6 pb-10">
      <div class="grid grid-cols-2 gap-4">
        <router-link
          to="/map"
          class="entry-card bg-white/15 backdrop-blur-md rounded-2xl p-5 text-center text-white hover:bg-white/25 transition"
        >
          <div class="text-3xl mb-2">🗺️</div>
          <div class="font-semibold">红色地图</div>
          <div class="text-xs text-white/60 mt-1">地标标注 · 导览</div>
        </router-link>

        <router-link
          to="/model3d"
          class="entry-card bg-white/15 backdrop-blur-md rounded-2xl p-5 text-center text-white hover:bg-white/25 transition"
        >
          <div class="text-3xl mb-2">🏔️</div>
          <div class="font-semibold">三维模型</div>
          <div class="text-xs text-white/60 mt-1">航拍实景 · 3D</div>
        </router-link>

        <router-link
          to="/site/1"
          class="entry-card bg-white/15 backdrop-blur-md rounded-2xl p-5 text-center text-white hover:bg-white/25 transition"
        >
          <div class="text-3xl mb-2">🏥</div>
          <div class="font-semibold">地标详情</div>
          <div class="text-xs text-white/60 mt-1">图文 · 语音</div>
        </router-link>

        <router-link
          to="/about"
          class="entry-card bg-white/15 backdrop-blur-md rounded-2xl p-5 text-center text-white hover:bg-white/25 transition"
        >
          <div class="text-3xl mb-2">📖</div>
          <div class="font-semibold">关于项目</div>
          <div class="text-xs text-white/60 mt-1">项目介绍</div>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
// 首页 — 无需额外逻辑
</script>

<style scoped>
.home-page {
  background: linear-gradient(160deg, #8B0000 0%, #C41E24 60%, #b71c1c 100%);
}

.entry-card {
  text-decoration: none;
  border: 1px solid rgba(255,255,255,0.15);
}

/* 装饰粒子 */
.star {
  position: absolute;
  border-radius: 50%;
  background: rgba(212, 168, 67, 0.2);
}
.star-1 { width: 200px; height: 200px; top: -60px; right: -60px; }
.star-2 { width: 120px; height: 120px; bottom: 30%; left: -40px; }
.star-3 { width: 80px; height: 80px; top: 40%; right: 20px; }
</style>
