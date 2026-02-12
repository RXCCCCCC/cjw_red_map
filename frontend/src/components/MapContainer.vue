<template>
  <div ref="mapRef" class="w-full h-full"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'

const props = defineProps({
  sites: { type: Array, default: () => [] },
})
const emit = defineEmits(['marker-click'])

const mapRef = ref(null)
let map = null
let markerGroup = null

// 天地图 key（公共测试 key，生产环境需替换）
const TDT_KEY = '174705aebfe31b79b3587279e211cb9a'

// 程家湾中心坐标
const CENTER = [28.8155, 117.895]

onMounted(() => {
  map = L.map(mapRef.value, {
    center: CENTER,
    zoom: 16,
    zoomControl: false,
  })

  // 天地图影像底图
  L.tileLayer(
    `https://t{s}.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=${TDT_KEY}`,
    { subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'], maxZoom: 18 }
  ).addTo(map)

  // 天地图注记
  L.tileLayer(
    `https://t{s}.tianditu.gov.cn/cia_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=${TDT_KEY}`,
    { subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'], maxZoom: 18 }
  ).addTo(map)

  // 缩放控件
  L.control.zoom({ position: 'topright' }).addTo(map)

  markerGroup = L.layerGroup().addTo(map)

  addMarkers()
})

watch(() => props.sites, addMarkers, { deep: true })

function addMarkers() {
  if (!markerGroup) return
  markerGroup.clearLayers()

  props.sites.forEach((site) => {
    if (!site.longitude || !site.latitude) return

    // 自定义红色图标
    const icon = L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        width:32px;height:32px;border-radius:50%;
        background:#C41E24;border:3px solid #fff;
        box-shadow:0 2px 8px rgba(0,0,0,0.3);
        display:flex;align-items:center;justify-content:center;
        color:#fff;font-size:14px;font-weight:bold;
      ">${getCategoryIcon(site.category)}</div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -34],
    })

    const marker = L.marker([site.latitude, site.longitude], { icon })
      .bindPopup(createPopupHtml(site), {
        maxWidth: 220,
        className: 'site-popup',
      })
      .addTo(markerGroup)

    marker.on('click', () => {
      emit('marker-click', site)
    })
  })
}

function getCategoryIcon(category) {
  const map = { '医院': '🏥', '军事设施': '🔫', '道路': '🛤️', '地标': '📍' }
  return map[category] || '📍'
}

function createPopupHtml(site) {
  return `
    <div style="padding:4px 0">
      <strong style="color:#C41E24;font-size:14px">${site.name}</strong>
      <div style="color:#888;font-size:11px;margin-top:2px">${site.category}</div>
      <div style="color:#666;font-size:12px;margin-top:6px;line-height:1.5">
        ${(site.description || '').substring(0, 60)}...
      </div>
    </div>
  `
}
</script>

<style>
.custom-marker {
  background: transparent !important;
  border: none !important;
}
.site-popup .leaflet-popup-content-wrapper {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
</style>
