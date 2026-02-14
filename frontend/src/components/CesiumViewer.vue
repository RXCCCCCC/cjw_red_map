<template>
  <div class="relative w-full h-full">
    <!-- Cesium 容器 -->
    <div ref="cesiumContainer" class="cesium-container"></div>

    <!-- ════════ 编辑模式控制栏 (左上角) ════════ -->
    <div class="absolute top-3 left-3 z-30 flex flex-col gap-2">
      <!-- 进入编辑模式按钮 -->
      <button
        v-if="!editMode"
        class="px-3 py-1.5 text-xs bg-white/90 rounded-lg shadow-lg hover:bg-white transition"
        @click="showPasswordDialog = true"
      >🔧 编辑模式</button>

      <!-- 编辑模式状态栏 -->
      <template v-if="editMode">
        <div class="bg-amber-500 text-white px-3 py-1.5 rounded-lg shadow-lg text-xs font-bold flex items-center gap-2">
          ⚠️ 编辑模式
          <button class="ml-2 underline" @click="exitEditMode">退出</button>
        </div>
        <div class="flex gap-1.5">
          <button
            class="px-2 py-1 text-[11px] rounded-md shadow"
            :class="editAction === 'add' ? 'bg-green-600 text-white' : 'bg-white/90 hover:bg-white'"
            @click="editAction = editAction === 'add' ? null : 'add'"
          >📍 添加地标</button>
          <button
            class="px-2 py-1 text-[11px] rounded-md shadow"
            :class="editAction === 'drag' ? 'bg-blue-600 text-white' : 'bg-white/90 hover:bg-white'"
            @click="editAction = editAction === 'drag' ? null : 'drag'"
          >✋ 拖动调整</button>
          <button
            class="px-2 py-1 text-[11px] rounded-md shadow"
            :class="isDrawingPath ? 'bg-purple-600 text-white' : 'bg-white/90 hover:bg-white'"
            @click="toggleDrawingMode"
          >✏️ 绘制路径</button>
          <button
            class="px-2 py-1 text-[11px] bg-white/90 hover:bg-white rounded-md shadow"
            @click="showRoutesList = true"
          >📋 路径列表</button>
        </div>
        <div v-if="editAction === 'add'" class="bg-green-100 text-green-800 px-2 py-1 rounded text-[10px]">
          点击地图任意位置添加新地标点
        </div>
        <div v-if="editAction === 'drag'" class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-[10px]">
          按住左键拖动地标标注点移动位置
        </div>
        <div v-if="isDrawingPath" class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-[10px] flex items-center justify-between gap-2">
          <span>已绘制 {{ currentPathPoints.length }} 个点 (点击地图添加)</span>
          <div class="flex gap-1">
            <button class="bg-white border px-1 rounded hover:bg-gray-50" @click="undoLastPoint" v-if="currentPathPoints.length > 0">撤销</button>
            <button class="bg-purple-600 text-white px-2 rounded hover:bg-purple-700" @click="finishDrawing" v-if="currentPathPoints.length >= 2">完成</button>
            <button class="bg-gray-400 text-white px-1 rounded hover:bg-gray-500" @click="cancelDrawing">取消</button>
          </div>
        </div>
      </template>
    </div>

    <!-- ════════ 保存路径对话框 ════════ -->
    <Transition name="popup-fade">
      <div v-if="showSavePathDialog" class="absolute inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="bg-white rounded-xl shadow-2xl p-5 w-80">
          <h3 class="text-sm font-bold text-gray-800 mb-3">💾 保存游览路径</h3>
          <div class="space-y-3">
            <div>
              <label class="block text-xs text-gray-500 mb-1">路径名称 *</label>
              <input v-model="pathForm.name" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="如：红色之旅路线A" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">描述</label>
              <textarea v-model="pathForm.description" rows="3" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="路径简介..." />
            </div>
          </div>
          <div class="flex gap-2 mt-4">
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-gray-200 rounded-lg hover:bg-gray-300"
              @click="showSavePathDialog = false"
            >取消</button>
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-purple-600 text-white rounded-lg hover:bg-purple-700"
              @click="savePath"
              :disabled="!pathForm.name"
            >保存</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ════════ 路径列表对话框 ════════ -->
    <Transition name="popup-fade">
      <div v-if="showRoutesList" class="absolute inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="bg-white rounded-xl shadow-2xl p-5 w-96 max-h-[80vh] flex flex-col">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-sm font-bold text-gray-800">📋 已保存的路径</h3>
            <button @click="showRoutesList = false" class="text-gray-400 hover:text-gray-600">✕</button>
          </div>
          <div class="flex-1 overflow-y-auto min-h-[200px]">
            <div v-if="savedRoutes.length === 0" class="text-center text-gray-400 py-8 text-xs">暂无保存的路径</div>
            <div v-else class="space-y-2">
              <div v-for="route in savedRoutes" :key="route.id" class="border rounded p-2 hover:bg-gray-50 flex justify-between items-center group">
                <div>
                  <div class="font-bold text-xs text-gray-800">{{ route.name }}</div>
                  <div class="text-[10px] text-gray-500 truncate max-w-[180px]">{{ route.description || '无描述' }}</div>
                </div>
                <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition">
                  <button class="text-green-600 text-[10px] hover:underline" @click="copyRoute(route)">复制</button>
                  <button class="text-red-500 text-[10px] hover:underline" @click="confirmDeleteRoute(route.id)">删除</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ════════ 路径导航对话框 ════════ -->
    <Transition name="popup-fade">
      <div v-if="showNavigationDialog" class="absolute inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="bg-white rounded-xl shadow-2xl p-5 w-96 max-h-[80vh] flex flex-col">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-sm font-bold text-gray-800">🧭 选择导航路径</h3>
            <button @click="closeNavigation" class="text-gray-400 hover:text-gray-600">✕</button>
          </div>
          <div class="flex-1 overflow-y-auto min-h-[200px]">
            <div v-if="savedRoutes.length === 0" class="text-center text-gray-400 py-8 text-xs">暂无可用路径</div>
            <div v-else class="space-y-2">
              <div 
                v-for="route in savedRoutes" 
                :key="route.id" 
                class="border rounded p-3 cursor-pointer transition"
                :class="activeNavigationRoute?.id === route.id ? 'bg-blue-50 border-blue-500' : 'hover:bg-gray-50 border-gray-200'"
                @click="startNavigation(route)"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="font-bold text-sm text-gray-800 flex items-center gap-2">
                      {{ route.name }}
                      <span v-if="activeNavigationRoute?.id === route.id" class="text-blue-600 text-xs">✓ 已选择</span>
                    </div>
                    <div class="text-[10px] text-gray-500 mt-0.5">{{ route.description || '无描述' }}</div>
                  </div>
                  <div v-if="activeNavigationRoute?.id === route.id" class="text-blue-600">
                    🧭
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="activeNavigationRoute" class="mt-3 pt-3 border-t">
            <button 
              class="w-full px-3 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
              @click="stopNavigation"
            >
              停止导航
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ════════ 密码对话框 ════════ -->
    <Transition name="popup-fade">
      <div v-if="showPasswordDialog" class="absolute inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="bg-white rounded-xl shadow-2xl p-5 w-72">
          <h3 class="text-sm font-bold text-gray-800 mb-3">🔑 输入编辑密码</h3>
          <input
            v-model="passwordInput"
            type="password"
            placeholder="请输入密码"
            class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-400"
            @keyup.enter="verifyPassword"
          />
          <div v-if="passwordError" class="text-red-500 text-xs mt-1">密码错误</div>
          <div class="flex gap-2 mt-3">
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-gray-200 rounded-lg hover:bg-gray-300"
              @click="showPasswordDialog = false; passwordInput = ''; passwordError = false"
            >取消</button>
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-red-600 text-white rounded-lg hover:bg-red-700"
              @click="verifyPassword"
            >确认</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ════════ 新增地标表单对话框 ════════ -->
    <Transition name="popup-fade">
      <div v-if="showAddForm" class="absolute inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="bg-white rounded-xl shadow-2xl p-5 w-80 max-h-[80vh] overflow-y-auto">
          <h3 class="text-sm font-bold text-gray-800 mb-3">📍 新增地标</h3>
          <div class="space-y-2 text-xs">
            <div>
              <label class="block text-gray-500 mb-0.5">名称 *</label>
              <input v-model="addForm.name" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="地标名称" />
            </div>
            <div>
              <label class="block text-gray-500 mb-0.5">分类</label>
              <input v-model="addForm.category" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="如：纪念设施、战场..." />
            </div>
            <div>
              <label class="block text-gray-500 mb-0.5">描述</label>
              <textarea v-model="addForm.description" rows="3" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="地标简介..." />
            </div>
            <div class="grid grid-cols-3 gap-1">
              <div>
                <label class="block text-gray-500 mb-0.5">经度</label>
                <input v-model.number="addForm.longitude" type="number" step="0.00001" class="w-full border rounded px-1 py-1 text-[11px]" />
              </div>
              <div>
                <label class="block text-gray-500 mb-0.5">纬度</label>
                <input v-model.number="addForm.latitude" type="number" step="0.00001" class="w-full border rounded px-1 py-1 text-[11px]" />
              </div>
              <div>
                <label class="block text-gray-500 mb-0.5">高度(m)</label>
                <input v-model.number="addForm.height" type="number" step="0.1" class="w-full border rounded px-1 py-1 text-[11px]" />
              </div>
            </div>
          </div>
          <div class="flex gap-2 mt-4">
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-gray-200 rounded-lg hover:bg-gray-300"
              @click="showAddForm = false"
            >取消</button>
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-green-600 text-white rounded-lg hover:bg-green-700"
              @click="submitNewSite"
              :disabled="!addForm.name"
            >保存到数据库</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ════════ 编辑地标信息表单对话框 ════════ -->
    <Transition name="popup-fade">
      <div v-if="showEditForm" class="absolute inset-0 z-50 flex items-center justify-center bg-black/40">
        <div class="bg-white rounded-xl shadow-2xl p-5 w-80 max-h-[80vh] overflow-y-auto">
          <h3 class="text-sm font-bold text-gray-800 mb-3">✏️ 编辑地标信息</h3>
          <div class="space-y-2 text-xs">
            <div>
              <label class="block text-gray-500 mb-0.5">名称 *</label>
              <input v-model="editForm.name" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="地标名称" />
            </div>
            <div>
              <label class="block text-gray-500 mb-0.5">分类</label>
              <input v-model="editForm.category" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="如：纪念设施、战场..." />
            </div>
            <div>
              <label class="block text-gray-500 mb-0.5">描述</label>
              <textarea v-model="editForm.description" rows="4" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="地标简介..." />
            </div>
            <div class="grid grid-cols-3 gap-1">
              <div>
                <label class="block text-gray-500 mb-0.5">经度</label>
                <input v-model.number="editForm.longitude" type="number" step="0.00001" class="w-full border rounded px-1 py-1 text-[11px]" />
              </div>
              <div>
                <label class="block text-gray-500 mb-0.5">纬度</label>
                <input v-model.number="editForm.latitude" type="number" step="0.00001" class="w-full border rounded px-1 py-1 text-[11px]" />
              </div>
              <div>
                <label class="block text-gray-500 mb-0.5">高度(m)</label>
                <input v-model.number="editForm.height" type="number" step="0.1" class="w-full border rounded px-1 py-1 text-[11px]" />
              </div>
            </div>
            <div>
              <label class="block text-gray-500 mb-0.5">排序权重</label>
              <input v-model.number="editForm.sort_order" type="number" class="w-full border rounded px-2 py-1.5 text-sm" placeholder="数字越小越靠前" />
            </div>
          </div>
          <div class="flex gap-2 mt-4">
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-gray-200 rounded-lg hover:bg-gray-300"
              @click="showEditForm = false"
            >取消</button>
            <button
              class="flex-1 px-3 py-1.5 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              @click="submitEditSite"
              :disabled="!editForm.name || editSaving"
            >{{ editSaving ? '保存中...' : '保存修改' }}</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ════════ 地标信息弹窗（查看+编辑+媒体管理） ════════ -->
    <Transition name="popup-fade">
      <div
        v-if="selectedSite"
        class="absolute bottom-20 left-1/2 -translate-x-1/2 z-20 w-80 bg-white rounded-xl shadow-2xl overflow-hidden max-h-[70vh] overflow-y-auto"
      >
        <!-- 关闭按钮 -->
        <button
          class="absolute top-2 right-2 w-6 h-6 rounded-full bg-black/20 text-white text-xs flex items-center justify-center z-10"
          @click="selectedSite = null"
        >✕</button>

        <!-- 封面 / 占位 -->
        <div class="h-28 bg-red-800 flex items-center justify-center overflow-hidden relative">
          <img
            v-if="selectedSite.cover_image"
            :src="selectedSite.cover_image"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-white/40 text-5xl">🏛️</span>
          <!-- 编辑模式：上传封面 -->
          <label v-if="editMode" class="absolute bottom-1 right-1 bg-black/50 text-white text-[10px] px-2 py-0.5 rounded cursor-pointer hover:bg-black/70">
            📷 更换封面
            <input type="file" accept="image/*" class="hidden" @change="uploadCoverImage" />
          </label>
        </div>

        <!-- 内容 -->
        <div class="p-3">
          <span class="inline-block px-2 py-0.5 bg-amber-500 text-white text-[10px] rounded-full mb-1">
            {{ selectedSite.category }}
          </span>
          <h4 class="text-red-800 font-bold text-sm">{{ selectedSite.name }}</h4>
          <p class="text-gray-400 text-[10px] mt-0.5">
            经:{{ selectedSite.longitude?.toFixed(5) }} 纬:{{ selectedSite.latitude?.toFixed(5) }} 高:{{ (selectedSite.height || 0).toFixed(1) }}m
          </p>
          <p class="text-gray-500 text-xs mt-1 leading-relaxed line-clamp-3">
            {{ selectedSite.description }}
          </p>

          <!-- 查看模式按钮 -->
          <button
            v-if="!editMode"
            class="mt-2 w-full text-xs text-white bg-red-700 hover:bg-red-800 rounded-full px-3 py-1.5 transition"
            @click="goDetail(selectedSite.id)"
          >
            查看详情 →
          </button>

          <!-- ── 编辑模式：媒体上传区域 ── -->
          <template v-if="editMode">
            <div class="border-t mt-3 pt-3">
              <h5 class="text-xs font-bold text-gray-700 mb-2">📁 媒体管理</h5>

              <!-- 已有媒体列表 -->
              <div v-if="siteMediaList.length" class="space-y-1 mb-2">
                <div
                  v-for="m in siteMediaList" :key="m.id"
                  class="flex items-center gap-1.5 bg-gray-50 rounded px-2 py-1"
                >
                  <span class="text-[10px]">{{ m.type === 'image' ? '🖼️' : m.type === 'audio' ? '🎵' : '🎬' }}</span>
                  <span class="text-[11px] text-gray-600 flex-1 truncate">{{ m.title || m.url }}</span>
                  <button class="text-red-400 text-[10px] hover:text-red-600" @click="removeMedia(m.id)">删除</button>
                </div>
              </div>
              <div v-else class="text-gray-400 text-[10px] mb-2">暂无媒体文件</div>

              <!-- 上传新媒体 -->
              <label class="block w-full text-center px-3 py-2 bg-blue-50 text-blue-600 text-xs rounded-lg cursor-pointer hover:bg-blue-100 transition">
                📤 上传图片/音频/视频
                <input type="file" accept="image/*,audio/*,video/*" multiple class="hidden" @change="uploadMediaFiles" />
              </label>
              <div v-if="uploading" class="text-center text-[10px] text-gray-400 mt-1">上传中...</div>
            </div>

            <!-- 编辑模式：编辑信息按钮 -->
            <button
              class="mt-3 w-full text-xs text-white bg-blue-600 rounded-full px-3 py-1.5 hover:bg-blue-700 transition"
              @click="openEditForm"
            >✏️ 编辑地标信息</button>

            <!-- 编辑模式：删除地标 -->
            <button
              class="mt-2 w-full text-xs text-red-500 border border-red-300 rounded-full px-3 py-1.5 hover:bg-red-50 transition"
              @click="deleteSiteConfirm"
            >🗑️ 删除此地标</button>
          </template>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, inject, watch } from 'vue'
import { useRouter } from 'vue-router'
import * as Cesium from 'cesium'
import { getSites, getSite, createSite, updateSite, deleteSite as apiDeleteSite, getSiteMedia, createMedia, deleteMedia, uploadFile, getRoutes, createRoute, deleteRoute } from '@/api'

const cesiumContainer = ref(null)
const selectedSite = ref(null)
const router = useRouter()

let viewer = null
let tileset = null
let clickHandler = null
let dragHandler = null

const registerResetView = inject('registerResetView', null)
const registerShowNavigation = inject('registerShowNavigation', null)

/* ══════ 编辑模式状态 ══════ */
const EDIT_PASSWORD = '114514'
const editMode = ref(false)
const editAction = ref(null)      // 'add' | 'drag' | null
const showPasswordDialog = ref(false)
const passwordInput = ref('')
const passwordError = ref(false)
const showAddForm = ref(false)
const uploading = ref(false)
const siteMediaList = ref([])
const showEditForm = ref(false)   // 编辑地标信息表单是否显示
const editSaving = ref(false)     // 编辑保存中

// 编辑地标信息表单（回填当前值）
const editForm = ref({
  id: null,
  name: '',
  description: '',
  longitude: 0,
  latitude: 0,
  height: 0,
  category: '',
  sort_order: 0,
})

// 新增地标表单
const addForm = ref({
  name: '',
  description: '',
  longitude: 0,
  latitude: 0,
  height: 0,
  category: '',
})

/* ── 验证密码 ── */
function verifyPassword() {
  if (passwordInput.value === EDIT_PASSWORD) {
    editMode.value = true
    showPasswordDialog.value = false
    passwordInput.value = ''
    passwordError.value = false
  } else {
    passwordError.value = true
  }
}

/* ── 退出编辑模式 ── */
function exitEditMode() {
  editMode.value = false
  editAction.value = null
  cleanupDrag()
}

/* ══════ 拖动相关变量 ══════ */
let draggingEntity = null
let dragStartPosition = null
let lastDragCartesian = null   // 缓存拖动过程中最新的 Cartesian3 位置

/* ── 初始化拖动事件 ── */
function setupDragHandler() {
  if (dragHandler) dragHandler.destroy()
  dragHandler = new Cesium.ScreenSpaceEventHandler(viewer.canvas)

  // 按下 → 检测是否选中了地标标注
  dragHandler.setInputAction((click) => {
    if (!editMode.value || editAction.value !== 'drag') return
    const picked = viewer.scene.pick(click.position)
    if (Cesium.defined(picked) && picked.id && String(picked.id.id || picked.id._id || '').startsWith('site-')) {
      draggingEntity = picked.id
      lastDragCartesian = null
      // 安全读取当前位置作为回滚备份
      try {
        const pos = draggingEntity.position
        dragStartPosition = (typeof pos.getValue === 'function')
          ? pos.getValue(Cesium.JulianDate.now())
          : pos
      } catch (_) {
        dragStartPosition = null
      }
      // 拖动期间禁止地图旋转/平移
      viewer.scene.screenSpaceCameraController.enableRotate = false
      viewer.scene.screenSpaceCameraController.enableTranslate = false
    }
  }, Cesium.ScreenSpaceEventType.LEFT_DOWN)

  // 移动 → 更新实体位置
  dragHandler.setInputAction((movement) => {
    if (!draggingEntity) return
    const cartesian = pickPosition(movement.endPosition)
    if (cartesian) {
      lastDragCartesian = cartesian           // 缓存最新位置
      draggingEntity.position = cartesian
      // 实时更新标签坐标文本
      const carto = Cesium.Cartographic.fromCartesian(cartesian)
      const lon = Cesium.Math.toDegrees(carto.longitude)
      const lat = Cesium.Math.toDegrees(carto.latitude)
      const h = carto.height
      // 安全读取 siteData，不再更新 label.text（已移除）
    }
  }, Cesium.ScreenSpaceEventType.MOUSE_MOVE)

  // 松开 → 保存新位置到数据库
  dragHandler.setInputAction(async () => {
    if (!draggingEntity) return

    // 使用缓存的最新位置（最可靠），不再依赖 entity.position.getValue()
    const cartesian = lastDragCartesian
    if (!cartesian) {
      // 没有拖动过（原地点击+松开），直接退出
      viewer.scene.screenSpaceCameraController.enableRotate = true
      viewer.scene.screenSpaceCameraController.enableTranslate = true
      draggingEntity = null
      return
    }

    const carto = Cesium.Cartographic.fromCartesian(cartesian)
    const lon = Cesium.Math.toDegrees(carto.longitude)
    const lat = Cesium.Math.toDegrees(carto.latitude)
    const h = carto.height

    // 从 entity id 提取 site id（兼容 .id 和 ._id）
    const entityId = String(draggingEntity.id || draggingEntity._id || '')
    const siteId = parseInt(entityId.replace('site-', ''))

    try {
      const resp = await updateSite(siteId, { longitude: lon, latitude: lat, height: h })
      console.log(`✅ 地标 ${siteId} 位置已保存: ${lon.toFixed(5)}, ${lat.toFixed(5)}, ${h.toFixed(1)}m`, resp.data)
      // 更新 properties 中缓存的数据
      try {
        const siteData = draggingEntity.properties?.siteData?.getValue(Cesium.JulianDate.now())
        if (siteData) {
          siteData.longitude = lon
          siteData.latitude = lat
          siteData.height = h
          draggingEntity.properties.siteData = siteData
        }
      } catch (_) { /* properties 更新失败不影响持久化 */ }
    } catch (e) {
      console.error('❌ 保存位置失败:', e)
      alert('保存位置失败，请检查网络或后端是否运行')
      // 恢复原位
      if (dragStartPosition) draggingEntity.position = dragStartPosition
    }

    // 恢复地图交互
    viewer.scene.screenSpaceCameraController.enableRotate = true
    viewer.scene.screenSpaceCameraController.enableTranslate = true
    draggingEntity = null
    dragStartPosition = null
    lastDragCartesian = null
  }, Cesium.ScreenSpaceEventType.LEFT_UP)
}

function cleanupDrag() {
  if (dragHandler) {
    dragHandler.destroy()
    dragHandler = null
  }
  if (viewer) {
    viewer.scene.screenSpaceCameraController.enableRotate = true
    viewer.scene.screenSpaceCameraController.enableTranslate = true
  }
  draggingEntity = null
  lastDragCartesian = null
}

/* ══════ 工具函数：拾取地面位置 ══════ */
function pickPosition(screenPos) {
  let cartesian = null
  try { cartesian = viewer.scene.pickPosition(screenPos) } catch (e) { /* ignore */ }
  if (!cartesian) {
    cartesian = viewer.camera.pickEllipsoid(screenPos, viewer.scene.globe.ellipsoid)
  }
  return cartesian || null
}

/* ══════ 生成圆角标签图片的 Canvas ══════ */
function createSiteLabelCanvas(text) {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  // 样式配置：基于之前的优化，继续加大内边距并圆角化
  const fontSize = 32 // 内部绘制分辨率更高，保证缩放清晰
  const font = '900 32px "Microsoft YaHei", "PingFang SC", sans-serif'
  const padding = { x: 32, y: 16 } // 边框改大：水平 32，垂直 16
  const radius = 20 // 大圆角
  const bgColor = 'rgba(185, 28, 28, 0.95)' // #B91C1C 更深一点
  
  // 1. 计算尺寸
  ctx.font = font
  const metrics = ctx.measureText(text)
  const textWidth = metrics.width
  const w = textWidth + padding.x * 2
  const h = fontSize * 1.5 + padding.y * 2 // 高度估算
  
  canvas.width = w
  canvas.height = h
  
  // 2. 重置上下文并绘制背景
  ctx.font = font
  ctx.textBaseline = 'middle'
  ctx.textAlign = 'center'
  
  // 绘制圆角矩形
  ctx.fillStyle = bgColor
  ctx.beginPath()
  ctx.moveTo(radius, 0)
  ctx.lineTo(w - radius, 0)
  ctx.quadraticCurveTo(w, 0, w, radius)
  ctx.lineTo(w, h - radius)
  ctx.quadraticCurveTo(w, h, w - radius, h)
  ctx.lineTo(radius, h)
  ctx.quadraticCurveTo(0, h, 0, h - radius)
  ctx.lineTo(0, radius)
  ctx.quadraticCurveTo(0, 0, radius, 0)
  ctx.closePath()
  ctx.fill()
  
  // 绘制边框（可选，如果需要外发光或描边）
  // ctx.lineWidth = 2;
  // ctx.strokeStyle = 'white';
  // ctx.stroke();

  // 3. 绘制文字
  const centerX = w / 2
  const centerY = h / 2
  
  // 文字描边（黑色半透明）
  ctx.lineWidth = 6
  ctx.lineJoin = 'round'
  ctx.strokeStyle = 'rgba(0, 0, 0, 0.6)'
  ctx.strokeText(text, centerX, centerY)
  
  // 文字填充（白色）
  ctx.fillStyle = 'white'
  ctx.fillText(text, centerX, centerY)
  
  return canvas
}

/* ══════ 导航到地标详情页 ══════ */
function goDetail(id) {
  selectedSite.value = null
  router.push(`/site/${id}`)
}

/* ══════ 在 3D 地图上添加地标标注 ══════ */
function addSiteMarker(site) {
  if (!viewer || site.longitude == null || site.latitude == null) return
  // 如果已存在则先移除
  const existingId = `site-${site.id}`
  const existing = viewer.entities.getById(existingId)
  if (existing) viewer.entities.remove(existing)

  viewer.entities.add({
    id: existingId,
    name: site.name,
    properties: { siteData: site },
    position: Cesium.Cartesian3.fromDegrees(site.longitude, site.latitude, site.height || 0),
    // 外圈光晕（半透明大圆）
    ellipse: {
      semiMajorAxis: 8.0,
      semiMinorAxis: 8.0,
      material: Cesium.Color.fromCssColorString('#C41E24').withAlpha(0.25),
      heightReference: Cesium.HeightReference.NONE,
    },
    point: {
      pixelSize: 10,
      color: Cesium.Color.fromCssColorString('#C41E24'),
      outlineColor: Cesium.Color.WHITE,
      outlineWidth: 3,
      heightReference: Cesium.HeightReference.NONE,
      disableDepthTestDistance: Number.POSITIVE_INFINITY,
      scaleByDistance: new Cesium.NearFarScalar(100, 1.4, 5000, 0.6),
    },
    // 将 label 替换为 billboard 以支持圆角背景
    billboard: {
      image: createSiteLabelCanvas(site.name),
      horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
      verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
      pixelOffset: new Cesium.Cartesian2(0, -20), // 保持和点有一定的距离
      scale: 0.5, // Canvas 画得很大（防糊），这里缩放显示
      disableDepthTestDistance: Number.POSITIVE_INFINITY,
      scaleByDistance: new Cesium.NearFarScalar(100, 1.0, 5000, 0.6),
    },
    // label: { ... } // 已移除
  })
}

function addSiteMarkers(sites) {
  if (!viewer) return
  sites.forEach(addSiteMarker)
}

/* ══════ 处理点击事件 ══════ */
function setupClickHandler() {
  clickHandler = new Cesium.ScreenSpaceEventHandler(viewer.canvas)
  clickHandler.setInputAction(async (movement) => {
    // ── 编辑模式：添加新地标 ──
    if (editMode.value && editAction.value === 'add') {
      const cartesian = pickPosition(movement.position)
      if (!cartesian) return
      const carto = Cesium.Cartographic.fromCartesian(cartesian)
      addForm.value.longitude = parseFloat(Cesium.Math.toDegrees(carto.longitude).toFixed(5))
      addForm.value.latitude = parseFloat(Cesium.Math.toDegrees(carto.latitude).toFixed(5))
      addForm.value.height = parseFloat(carto.height.toFixed(1))
      addForm.value.name = ''
      addForm.value.description = ''
      addForm.value.category = ''
      showAddForm.value = true
      return
    }

    // ── 编辑模式：拖动时不处理普通点击 ──
    if (editMode.value && editAction.value === 'drag') return

    // ── 普通模式 & 编辑模式无工具：查看地标信息 ──
    const picked = viewer.scene.pick(movement.position)
    if (Cesium.defined(picked) && picked.id && String(picked.id.id || picked.id._id || '').startsWith('site-')) {
      // 安全取出绑定在 entity.properties 上的地标数据
      let siteData = null
      try {
        siteData = picked.id.properties?.siteData?.getValue(Cesium.JulianDate.now())
      } catch (_) { /* ignore */ }
      if (siteData) {
        selectedSite.value = { ...siteData }
        // 编辑模式下也加载该地标的媒体列表
        if (editMode.value) {
          loadSiteMedia(siteData.id)
        }
      }
    } else {
      selectedSite.value = null
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)
}

/* ══════ 提交新地标 ══════ */
async function submitNewSite() {
  if (!addForm.value.name) return
  try {
    const { data } = await createSite({
      name: addForm.value.name,
      description: addForm.value.description,
      longitude: addForm.value.longitude,
      latitude: addForm.value.latitude,
      height: addForm.value.height,
      category: addForm.value.category,
      sort_order: 0,
    })
    const newSite = data.data
    addSiteMarker(newSite)
    showAddForm.value = false
    console.log(`✅ 新地标已添加: ${newSite.name} (id=${newSite.id})`)
  } catch (e) {
    console.error('添加地标失败:', e)
    alert('添加失败，请检查控制台')
  }
}

/* ══════ 编辑地标信息 ══════ */
function openEditForm() {
  if (!selectedSite.value) return
  const s = selectedSite.value
  // 将弹窗中当前地标数据回填到编辑表单
  editForm.value = {
    id: s.id,
    name: s.name || '',
    description: s.description || '',
    longitude: s.longitude ?? 0,
    latitude: s.latitude ?? 0,
    height: s.height ?? 0,
    category: s.category || '',
    sort_order: s.sort_order ?? 0,
  }
  showEditForm.value = true
}

async function submitEditSite() {
  if (!editForm.value.name || !editForm.value.id) return
  editSaving.value = true
  try {
    const payload = {
      name: editForm.value.name,
      description: editForm.value.description,
      longitude: editForm.value.longitude,
      latitude: editForm.value.latitude,
      height: editForm.value.height,
      category: editForm.value.category,
      sort_order: editForm.value.sort_order,
    }
    const { data } = await updateSite(editForm.value.id, payload)
    const updated = data.data

    // 同步更新弹窗中的 selectedSite
    selectedSite.value = { ...selectedSite.value, ...updated }

    // 同步更新 Cesium entity 的位置和标签
    const entity = viewer.entities.getById(`site-${updated.id}`)
    if (entity) {
      entity.position = Cesium.Cartesian3.fromDegrees(updated.longitude, updated.latitude, updated.height || 0)
      entity.name = updated.name
      // 更新 Billboard 图片
      if (entity.billboard) {
        entity.billboard.image = createSiteLabelCanvas(updated.name)
      }
      // 更新 properties 缓存
      entity.properties.siteData = updated
    }

    showEditForm.value = false
    console.log(`✅ 地标「${updated.name}」信息已更新`)
  } catch (e) {
    console.error('❌ 更新地标信息失败:', e)
    alert('保存失败，请检查网络或后端是否运行')
  } finally {
    editSaving.value = false
  }
}

/* ══════ 媒体管理 ══════ */
async function loadSiteMedia(siteId) {
  try {
    const { data } = await getSiteMedia(siteId)
    siteMediaList.value = data.data || []
  } catch (e) {
    siteMediaList.value = []
  }
}

async function uploadMediaFiles(event) {
  const files = event.target.files
  if (!files?.length || !selectedSite.value) return
  uploading.value = true
  try {
    for (const file of files) {
      // 1) 上传文件到服务器
      const { data: uploadRes } = await uploadFile(file)
      const info = uploadRes.data
      // 2) 创建媒体记录关联到地标
      await createMedia({
        site_id: selectedSite.value.id,
        type: info.type,
        url: info.url,
        title: info.original_name || info.title,
        description: '',
        sort_order: siteMediaList.value.length,
      })
    }
    // 刷新媒体列表
    await loadSiteMedia(selectedSite.value.id)
  } catch (e) {
    console.error('上传媒体失败:', e)
    alert('上传失败，请检查控制台')
  } finally {
    uploading.value = false
    event.target.value = '' // 重置 input
  }
}

async function uploadCoverImage(event) {
  const file = event.target.files?.[0]
  if (!file || !selectedSite.value) return
  uploading.value = true
  try {
    const { data: uploadRes } = await uploadFile(file)
    const url = uploadRes.data.url
    await updateSite(selectedSite.value.id, { cover_image: url })
    selectedSite.value.cover_image = url
    // 刷新 entity 的 properties
    const entity = viewer.entities.getById(`site-${selectedSite.value.id}`)
    if (entity) {
      const sd = entity.properties?.siteData?.getValue(Cesium.JulianDate.now())
      if (sd) { sd.cover_image = url; entity.properties.siteData = sd }
    }
  } catch (e) {
    console.error('上传封面失败:', e)
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

async function removeMedia(mediaId) {
  if (!confirm('确定删除此媒体？')) return
  try {
    await deleteMedia(mediaId)
    siteMediaList.value = siteMediaList.value.filter((m) => m.id !== mediaId)
  } catch (e) {
    console.error('删除媒体失败:', e)
  }
}

/* ══════ 删除地标 ══════ */
async function deleteSiteConfirm() {
  if (!selectedSite.value) return
  if (!confirm(`确定删除地标「${selectedSite.value.name}」？此操作不可撤销！`)) return
  try {
    await apiDeleteSite(selectedSite.value.id)
    viewer.entities.removeById(`site-${selectedSite.value.id}`)
    selectedSite.value = null
    console.log('✅ 地标已删除')
  } catch (e) {
    console.error('删除地标失败:', e)
  }
}

/* ══════ 监听编辑工具切换 ══════ */
watch(editAction, (action) => {
  if (action === 'drag') {
    setupDragHandler()
  } else {
    cleanupDrag()
  }
})

/* ══════ 生命周期 ══════ */
onMounted(async () => {
  Cesium.Ion.defaultAccessToken = ''

  // 创建 Cesium Viewer：不要设置默认底图（保持 imageryProvider undefined），
  // 我们稍后隐藏 globe 和天空盒，只显示 3D Tiles
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
    creditContainer: document.createElement('div'),
    imageryProvider: undefined,
    skyBox: false,
    skyAtmosphere: false,
  })

  // 加载 3D Tiles
  try {
    tileset = await Cesium.Cesium3DTileset.fromUrl('/tiles/tileset.json', {
      maximumScreenSpaceError: 16,
      maximumMemoryUsage: 512,
    })
    viewer.scene.primitives.add(tileset)
    await viewer.zoomTo(tileset)
    if (registerResetView) {
      registerResetView(() => viewer.zoomTo(tileset))
    }
    // 隐藏默认地球表面与天空，使画面只显示 3D Tiles
    try {
      if (viewer && viewer.scene) {
        if (viewer.scene.globe) viewer.scene.globe.show = false
        if (viewer.scene.skyBox) viewer.scene.skyBox.show = false
        if (viewer.scene.skyAtmosphere) viewer.scene.skyAtmosphere.show = false
        // 设置背景颜色为黑色（更适合展示 3D Tiles）
        viewer.scene.backgroundColor = Cesium.Color.BLACK
      }
    } catch (e) {
      console.warn('无法隐藏 globe/sky（可忽略）:', e)
    }
  } catch (e) {
    console.error('加载 3D Tiles 失败:', e)
  }

  // 加载地标列表并在地图上标注
  try {
    const { data } = await getSites()
    addSiteMarkers(data.data || [])
  } catch (e) {
    console.error('加载地标数据失败:', e)
  }

  setupClickHandler()
})

onBeforeUnmount(() => {
  cleanupDrag()
  if (clickHandler) { clickHandler.destroy(); clickHandler = null }
  if (viewer) { viewer.destroy(); viewer = null }
})

/* ══════ 路径绘制相关 ══════ */
const isDrawingPath = ref(false)
const currentPathPoints = ref([]) // cartesian3
const tempPolylineEntity = ref(null)
const showSavePathDialog = ref(false)
const pathForm = ref({ name: '', description: '' })
const showRoutesList = ref(false)
const savedRoutes = ref([])
const floatingPoint = ref(null) // 鼠标悬停的实时点
let drawingHandler = null

/* ══════ 路径导航相关 ══════ */
const showNavigationDialog = ref(false)
const activeNavigationRoute = ref(null)
const navigationPolylineEntity = ref(null)

// 注册导航功能到父组件
if (registerShowNavigation) {
    registerShowNavigation(() => {
        showNavigationDialog.value = true
    })
}

function startNavigation(route) {
    // 清除之前的导航路径高亮
    if (navigationPolylineEntity.value) {
        try {
            viewer.entities.remove(navigationPolylineEntity.value)
        } catch(e) {
            // 如果实体不存在，忽略错误
            console.warn('清除旧路径实体失败:', e)
        }
        navigationPolylineEntity.value = null
    }
    
    // 设置当前活动路径
    activeNavigationRoute.value = route
    
    // 解析路径点位
    let points = route.points
    if (typeof points === 'string') {
        try { points = JSON.parse(points) } catch(e){}
    }
    if (!Array.isArray(points)) return
    
    // 创建高亮路径（使用不同颜色区分）
    const positions = points.map(p => Cesium.Cartesian3.fromDegrees(p[0], p[1], p[2] + 1))
    
    navigationPolylineEntity.value = viewer.entities.add({
        id: 'navigation-active-route',
        name: `导航: ${route.name}`,
        polyline: {
            positions: positions,
            width: 8,
            material: new Cesium.PolylineGlowMaterialProperty({
                glowPower: 0.25,
                color: Cesium.Color.CYAN
            }),
            clampToGround: true
        }
    })
    
    // 飞向路径
    viewer.flyTo(navigationPolylineEntity.value, {
        duration: 2,
        offset: new Cesium.HeadingPitchRange(0, Cesium.Math.toRadians(-45), positions.length > 5 ? 500 : 200)
    })
}

function stopNavigation() {
    // 清除导航高亮
    if (navigationPolylineEntity.value) {
        try {
            viewer.entities.remove(navigationPolylineEntity.value)
        } catch(e) {
            console.warn('清除导航路径失败:', e)
        }
        navigationPolylineEntity.value = null
    }
    activeNavigationRoute.value = null
}

function closeNavigation() {
    showNavigationDialog.value = false
}

// 加载已有路径（仅加载数据，不自动渲染到地图）
onMounted(async () => {
    try {
        const res = await getRoutes()
        if (res.data.code === 0) {
            savedRoutes.value = res.data.data
            // 不再自动渲染所有路径，只有导航时才显示
        }
    } catch (e) { console.error('Failed to load routes', e) }
})

/* ── 切换绘制模式 ── */
function toggleDrawingMode() {
  if (isDrawingPath.value) {
    cancelDrawing()
  } else {
    isDrawingPath.value = true
    editAction.value = null
    currentPathPoints.value = []
    
    if (tempPolylineEntity.value) {
        viewer.entities.remove(tempPolylineEntity.value)
    }
    // 创建临时线
    tempPolylineEntity.value = viewer.entities.add({
      polyline: {
        positions: new Cesium.CallbackProperty(() => {
            // 如果正在鼠标移动中有临时点，组合展示
            if (floatingPoint.value && currentPathPoints.value.length > 0) {
                return [...currentPathPoints.value, floatingPoint.value]
            }
            return currentPathPoints.value
        }, false),
        width: 5,
        material: Cesium.Color.YELLOW.withAlpha(0.8),
        clampToGround: true
      }
    })
    
    setupDrawingHandler()
  }
}

function setupDrawingHandler() {
  if (drawingHandler) drawingHandler.destroy()
  drawingHandler = new Cesium.ScreenSpaceEventHandler(viewer.canvas)

  // 左键点击：添加固定点
  drawingHandler.setInputAction((click) => {
    // 忽略点击起止位置距离过大的操作（这是拖动，不是点击）- Cesium 内部通常已处理 click vs drag，但防止误触
    // 下面直接获取点击位置
    const cartesian = pickPosition(click.position)
    if (cartesian) {
      currentPathPoints.value.push(cartesian)
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)
  
  // 鼠标移动：更新浮动点（橡皮筋效果）
  drawingHandler.setInputAction((movement) => {
      if (currentPathPoints.value.length > 0) {
          const cartesian = pickPosition(movement.endPosition)
          if (cartesian) {
              floatingPoint.value = cartesian
          }
      }
  }, Cesium.ScreenSpaceEventType.MOUSE_MOVE)
  
  // 右键点击：结束绘制
  drawingHandler.setInputAction(() => {
    if (currentPathPoints.value.length >= 2) finishDrawing()
  }, Cesium.ScreenSpaceEventType.RIGHT_CLICK)
}

function undoLastPoint() {
  if (currentPathPoints.value.length > 0) currentPathPoints.value.pop()
}

function finishDrawing() {
  if (currentPathPoints.value.length < 2) return alert('请至少绘制2个点')
  
  // 暂停监听
  if (drawingHandler) {
      drawingHandler.destroy()
      drawingHandler = null
  }
  floatingPoint.value = null // 清除浮动点
  showSavePathDialog.value = true
}

function cancelDrawing() {
  isDrawingPath.value = false
  currentPathPoints.value = []
  floatingPoint.value = null
  if (tempPolylineEntity.value) {
    viewer.entities.remove(tempPolylineEntity.value)
    tempPolylineEntity.value = null
  }
  if (drawingHandler) {
    drawingHandler.destroy()
    drawingHandler = null
  }
  showSavePathDialog.value = false
}

async function savePath() {
   if (!pathForm.value.name) return
   
   // 转换坐标为 [lon, lat, height] 数组
   const pointsData = currentPathPoints.value.map(c => {
       const carto = Cesium.Cartographic.fromCartesian(c)
       return [
           Cesium.Math.toDegrees(carto.longitude),
           Cesium.Math.toDegrees(carto.latitude),
           carto.height
       ]
   })

   try {
       const res = await createRoute({
           name: pathForm.value.name,
           description: pathForm.value.description,
           points: pointsData,
           line_color: '#FFFF00',
           width: 5
       })
       if (res.data.code === 0) {
           const newRoute = res.data.data
           savedRoutes.value.unshift(newRoute)
           // 不自动渲染新保存的路径，用户可通过导航查看
           alert('路径保存成功')
           cancelDrawing()
           pathForm.value = { name: '', description: '' }
       }
   } catch (e) {
       console.error(e)
       alert('保存失败: ' + (e.response?.data?.msg || e.message))
   }
}

function renderRoute(route) {
    if (!viewer) return
    // 解析 points
    let points = route.points
    if (typeof points === 'string') {
        try { points = JSON.parse(points) } catch(e){}
    }
    
    if (!Array.isArray(points)) return

    const positions = points.map(p => Cesium.Cartesian3.fromDegrees(p[0], p[1], p[2] + 0.5))
    
    viewer.entities.add({
        id: 'route-' + route.id,
        name: route.name,
        description: route.description,
        polyline: {
            positions: positions,
            width: route.width || 5,
            material: Cesium.Color.fromCssColorString(route.line_color || '#FFFF00').withAlpha(0.8),
            clampToGround: true
        }
    })
}

function copyRoute(route) {
    if (!confirm(`确定要复制路径「${route.name}」并开始编辑吗？`)) return
    
    // 1. 关闭列表，退出其他模式
    showRoutesList.value = false
    if (isDrawingPath.value) cancelDrawing()
    
    // 2. 解析点位数据
    let points = route.points
    if (typeof points === 'string') {
        try { points = JSON.parse(points) } catch(e){}
    }
    if (!Array.isArray(points)) return alert('无法解析路径数据')

    // 3. 转换为 Cartesian3 并初始化绘制状态
    isDrawingPath.value = true
    editAction.value = null
    currentPathPoints.value = points.map(p => Cesium.Cartesian3.fromDegrees(p[0], p[1], p[2] + 0.5))
    
    // 预填名称
    pathForm.value.name = route.name + ' (副本)'
    pathForm.value.description = route.description
    
    // 4. 创建临时线实体（与 toggleDrawingMode 逻辑一致）
    if (tempPolylineEntity.value) {
        viewer.entities.remove(tempPolylineEntity.value)
    }
    tempPolylineEntity.value = viewer.entities.add({
      polyline: {
        positions: new Cesium.CallbackProperty(() => {
            if (floatingPoint.value && currentPathPoints.value.length > 0) {
                return [...currentPathPoints.value, floatingPoint.value]
            }
            return currentPathPoints.value
        }, false),
        width: 5,
        material: Cesium.Color.YELLOW.withAlpha(0.8),
        clampToGround: true
      }
    })
    
    // 5. 启动交互处理器
    setupDrawingHandler()
    
    // 6. 视角飞向新路径起点
    if (currentPathPoints.value.length > 0) {
        viewer.camera.flyTo({
            destination: currentPathPoints.value[0],
            duration: 1.5
        })
    }
}

async function confirmDeleteRoute(id) {
    if (!confirm('确定删除该路径吗？')) return
    try {
        const res = await deleteRoute(id)
        if (res.data.code === 0) {
            savedRoutes.value = savedRoutes.value.filter(r => r.id !== id)
            // 如果删除的是当前导航路径，清除导航
            if (activeNavigationRoute.value?.id === id) {
                stopNavigation()
            }
        }
    } catch (e) { console.error(e) }
}

// flyToRoute 不再需要，因为路径不会预先渲染
// function flyToRoute(route) {
//     const entity = viewer.entities.getById('route-' + route.id)
//     if (entity) viewer.flyTo(entity)
// }

</script>

<style scoped>
.popup-fade-enter-active,
.popup-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.popup-fade-enter-from,
.popup-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 8px);
}
</style>
