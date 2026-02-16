<template>
  <div class="about-page min-h-screen bg-gray-50">
    <NavBar title="关于项目" />

    <div class="px-5 py-6 space-y-6">
      <!-- 项目简介 -->
      <section class="bg-white rounded-2xl p-5 shadow-sm">
        <h2 class="text-red-primary font-bold text-lg mb-3">📖 项目简介</h2>
        <p class="text-gray-600 text-sm leading-relaxed">
          「程家湾红色资源数字地图」是基于无人机倾斜摄影与数字测绘技术，
          对江西省德兴市程家湾红色资源群进行数字化记录和展示的 H5 交互项目。
        </p>
        <p class="text-gray-600 text-sm leading-relaxed mt-2">
          项目涵盖红军旧址、红军炮台、红军路等重要红色地标的坐标标注、
          三维实景模型浏览、语音导览讲解、历史图文资料展示等功能，
          旨在用科技手段传承红色记忆、赓续红色血脉。
        </p>
      </section>

      <!-- 技术说明 -->
      <section class="bg-white rounded-2xl p-5 shadow-sm">
        <h2 class="text-red-primary font-bold text-lg mb-3">🔧 技术栈</h2>
        <ul class="text-gray-600 text-sm space-y-1.5">
          <li>• 前端：Vue 3 + Vite + Pinia + Tailwind CSS + Vant</li>
          <li>• 3D 渲染：CesiumJS（加载 3D Tiles 1.1 倾斜摄影模型）</li>
          <li>• 2D 地图：Leaflet + 天地图底图</li>
          <li>• 后端：Python Flask + SQLAlchemy + PyMySQL</li>
          <li>• 数据库：MySQL</li>
          <li>• 三维建模：GISBox 倾斜摄影处理</li>
        </ul>
      </section>

      <!-- 数据采集 -->
      <section class="bg-white rounded-2xl p-5 shadow-sm">
        <h2 class="text-red-primary font-bold text-lg mb-3">📡 数据采集</h2>
        <p class="text-gray-600 text-sm leading-relaxed">
          利用无人机进行倾斜摄影航拍，采集多角度高精度影像数据；
          结合全景相机拍摄地面细节，经 GISBox 软件处理生成 3D Tiles 1.1 格式的三维实景模型，
          真实还原程家湾红色地标的空间形态与地理环境。
        </p>
      </section>

      <!-- 版权 -->
      <div class="text-center text-gray-400 text-xs py-4">
        © 2026 程家湾红色资源数字地图项目组
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
</script>
