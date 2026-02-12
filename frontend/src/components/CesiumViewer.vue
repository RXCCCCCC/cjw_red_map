<template>
  <div ref="cesiumContainer" class="cesium-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, inject } from 'vue'
import * as Cesium from 'cesium'

const cesiumContainer = ref(null)
let viewer = null
let tileset = null

const registerResetView = inject('registerResetView', null)

onMounted(async () => {
  // 隐藏 Cesium 默认 logo & 控件
  Cesium.Ion.defaultAccessToken = ''

  viewer = new Cesium.Viewer(cesiumContainer.value, {
    animation: false,
    baseLayerPicker: false,
    fullscreenButton: false,
    geocoder: false,
    homeButton: false,
    infoBox: false,
    sceneModePicker: false,
    selectionIndicator: false,
    timeline: false,
    navigationHelpButton: false,
    creditContainer: document.createElement('div'), // 隐藏 credit
    // 天地图影像底图
    baseLayer: new Cesium.ImageryLayer(
      new Cesium.UrlTemplateImageryProvider({
        url: 'https://t{s}.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=174705aebfe31b79b3587279e211cb9a',
        subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
        maximumLevel: 18,
      })
    ),
  })

  // 加载 3D Tiles
  try {
    tileset = await Cesium.Cesium3DTileset.fromUrl('/tiles/tileset.json', {
      maximumScreenSpaceError: 16,
      maximumMemoryUsage: 512,
    })
    viewer.scene.primitives.add(tileset)

    // 飞到模型位置
    await viewer.zoomTo(tileset)

    // 注册重置视角回调
    if (registerResetView) {
      registerResetView(() => {
        viewer.zoomTo(tileset)
      })
    }
  } catch (e) {
    console.error('加载 3D Tiles 失败:', e)
  }
})

onBeforeUnmount(() => {
  if (viewer) {
    viewer.destroy()
    viewer = null
  }
})
</script>
