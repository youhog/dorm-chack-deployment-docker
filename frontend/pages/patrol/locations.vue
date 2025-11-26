<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">公共空間管理</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">管理各建築物的公共空間配置</p>

    <!-- Building Selector -->
    <div class="mb-6">
      <label class="block text-sm font-medium mb-2">選擇建築物</label>
      <select 
        v-model="selectedBuilding" 
        @change="loadLocations"
        class="w-full md:w-1/3 px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
      >
        <option :value="null">請選擇建築物</option>
        <option v-for="building in buildings" :key="building.id" :value="building.id">
          {{ building.name }}
        </option>
      </select>
    </div>

    <!-- Locations List -->
    <div v-if="selectedBuilding" class="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div class="p-6 border-b dark:border-gray-700 flex justify-between items-center">
        <h2 class="text-xl font-semibold">公共空間列表</h2>
        <button 
          @click="showCreateModal = true"
          class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg"
        >
          新增公共空間
        </button>
      </div>

      <div class="p-6">
        <div v-if="loading" class="text-center py-8">載入中...</div>
        <div v-else-if="locations.length === 0" class="text-center py-8 text-gray-500">
          尚未設定公共空間
        </div>
        <div v-else class="space-y-3">
          <div 
            v-for="location in locations" 
            :key="location.id"
            class="flex items-center justify-between p-4 border dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <div>
              <h3 class="font-medium">{{ location.name }}</h3>
              <p class="text-sm text-gray-500" v-if="location.household">
                戶別：{{ location.household }}
              </p>
            </div>
            <div class="flex gap-2">
              <button 
                @click="editLocation(location)"
                class="text-blue-600 hover:text-blue-800 px-3 py-1"
              >
                編輯
              </button>
              <button 
                @click="deleteLocation(location.id)"
                class="text-red-600 hover:text-red-800 px-3 py-1"
              >
                刪除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || editingLocation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">
          {{ editingLocation ? '編輯公共空間' : '新增公共空間' }}
        </h2>
        
        <form @submit.prevent="saveLocation">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">空間名稱</label>
            <input 
              v-model="formData.name"
              type="text"
              required
              placeholder="例如：一樓大廳、曬衣間"
              class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">戶別（選填）</label>
            <input 
              v-model="formData.household"
              type="text"
              placeholder="例如：A1201（若為整棟公共空間可留空）"
              class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
            />
          </div>

          <div class="flex justify-end gap-3">
            <button 
              type="button"
              @click="closeModal"
              class="px-4 py-2 border rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              取消
            </button>
            <button 
              type="submit"
              class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg"
            >
              儲存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useSnackbar } from '~/composables/useSnackbar';

const { apiFetch } = useAuth();
const { showSnackbar } = useSnackbar();

const buildings = ref([]);
const selectedBuilding = ref(null);
const locations = ref([]);
const loading = ref(false);
const showCreateModal = ref(false);
const editingLocation = ref(null);

const formData = ref({
  name: '',
  household: '',
  building_id: null
});

onMounted(async () => {
  try {
    const response = await apiFetch('/api/v1/buildings/');
    buildings.value = response;
  } catch (error) {
    showSnackbar({ message: '載入建築物列表失敗', type: 'error' });
  }
});

async function loadLocations() {
  if (!selectedBuilding.value) return;
  
  loading.value = true;
  try {
    const response = await apiFetch(`/api/v1/patrol-locations/?building_id=${selectedBuilding.value}`);
    locations.value = response.records || [];
  } catch (error) {
    showSnackbar({ message: '載入巡邏地點失敗', type: 'error' });
  } finally {
    loading.value = false;
  }
}

function editLocation(location) {
  editingLocation.value = location;
  formData.value = {
    name: location.name,
    household: location.household || '',
    building_id: location.building_id
  };
}

function closeModal() {
  showCreateModal.value = false;
  editingLocation.value = null;
  formData.value = { name: '', household: '', building_id: null };
}

async function saveLocation() {
  formData.value.building_id = selectedBuilding.value;
  
  try {
    if (editingLocation.value) {
      await apiFetch(`/api/v1/patrol-locations/${editingLocation.value.id}`, {
        method: 'PUT',
        body: formData.value
      });
      showSnackbar({ message: '公共空間更新成功', type: 'success' });
    } else {
      await apiFetch('/api/v1/patrol-locations/', {
        method: 'POST',
        body: formData.value
      });
      showSnackbar({ message: '公共空間新增成功', type: 'success' });
    }
    closeModal();
    loadLocations();
  } catch (error) {
    showSnackbar({ message: '儲存失敗', type: 'error' });
  }
}

async function deleteLocation(id) {
  if (!confirm('確定要刪除此公共空間嗎？')) return;
  
  try {
    await apiFetch(`/api/v1/patrol-locations/${id}`, { method: 'DELETE' });
    showSnackbar({ message: '刪除成功', type: 'success' });
    loadLocations();
  } catch (error) {
    showSnackbar({ message: '刪除失敗', type: 'error' });
  }
}
</script>
