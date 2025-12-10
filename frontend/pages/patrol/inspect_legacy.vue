<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">執行巡視</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">記錄公共空間電燈狀況</p>

    <!-- Building Selector -->
    <div class="mb-6">
      <label class="block text-sm font-medium mb-2">選擇建築物 *</label>
      <select 
        v-model="selectedBuilding" 
        @change="loadLocations"
        class="w-full md:w-1/2 px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
        :disabled="submitted"
      >
        <option :value="null">請選擇建築物</option>
        <option v-for="building in buildings" :key="building.id" :value="building.id">
          {{ building.name }}
        </option>
      </select>
    </div>

    <!-- Inspection Form -->
    <div v-if="selectedBuilding && locations.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">巡視檢查</h2>
      
      <div v-if="loading" class="text-center py-8">載入中...</div>
      
      <form v-else @submit.prevent="submitPatrol" class="space-y-4">
        <div 
          v-for="location in locations" 
          :key="location.id"
          class="p-4 border dark:border-gray-700 rounded-lg"
        >
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="font-medium text-lg">{{ location.name }}</h3>
              <p class="text-sm text-gray-500" v-if="location.household">
                戶別：{{ location.household }}
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium mb-2">電燈狀態 *</label>
              <div class="flex gap-4">
                <label class="flex items-center">
                  <input 
                    type="radio" 
                    :name="`status-${location.id}`"
                    :value="'off'"
                    v-model="inspectionData[location.id].status"
                    class="mr-2"
                    required
                  />
                  <span>已關閉</span>
                </label>
                <label class="flex items-center">
                  <input 
                    type="radio" 
                    :name="`status-${location.id}`"
                    :value="'on'"
                    v-model="inspectionData[location.id].status"
                    class="mr-2"
                    required
                  />
                  <span class="text-amber-600">未關閉</span>
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">備註（選填）</label>
              <input 
                type="text"
                v-model="inspectionData[location.id].notes"
                placeholder="例如：燈泡故障、開關損壞"
                class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              />
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-4">
          <button 
            type="button"
            @click="resetForm"
            class="px-6 py-2 border rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            :disabled="submitting"
          >
            重置
          </button>
          <button 
            type="submit"
            class="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg disabled:opacity-50"
            :disabled="submitting"
          >
            {{ submitting ? '提交中...' : '提交巡視記錄' }}
          </button>
        </div>
      </form>
    </div>

    <!-- No Locations Message -->
    <div v-else-if="selectedBuilding && locations.length === 0 && !loading" class="text-center py-8 text-gray-500">
      此建築物尚未設定公共空間，請先到「公共空間管理」頁面進行設定。
    </div>

    <!-- Success Message -->
    <div v-if="submitted" class="mt-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 text-center">
      <svg class="w-16 h-16 mx-auto mb-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <h3 class="text-xl font-semibold text-green-800 dark:text-green-200 mb-2">巡視記錄已提交</h3>
      <p class="text-green-700 dark:text-green-300 mb-4">感謝您完成巡視工作</p>
      <button 
        @click="startNewPatrol"
        class="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg"
      >
        開始新的巡視
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useSnackbar } from '~/composables/useSnackbar';

const { apiFetch } = useAuth();
const { showSnackbar } = useSnackbar();

const buildings = ref([]);
const selectedBuilding = ref(null);
const locations = ref([]);
const loading = ref(false);
const submitting = ref(false);
const submitted = ref(false);

const inspectionData = ref({});

onMounted(async () => {
  try {
    const response = await apiFetch('/api/v1/buildings/');
    buildings.value = response;
  } catch (error) {
    showSnackbar({ message: '載入建築物列表失敗', type: 'error' });
  }
});

watch(locations, (newLocations) => {
  // Initialize inspection data for each location
  newLocations.forEach(location => {
    if (!inspectionData.value[location.id]) {
      inspectionData.value[location.id] = {
        patrol_location_id: location.id,
        status: null,
        notes: ''
      };
    }
  });
});

async function loadLocations() {
  if (!selectedBuilding.value) return;
  
  loading.value = true;
  try {
    const response = await apiFetch(`/api/v1/patrol-locations/?building_id=${selectedBuilding.value}`);
    locations.value = response.records || [];
  } catch (error) {
    showSnackbar({ message: '載入巡視地點失敗', type: 'error' });
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  Object.keys(inspectionData.value).forEach(key => {
    inspectionData.value[key] = {
      patrol_location_id: key,
      status: null,
      notes: ''
    };
  });
}

async function submitPatrol() {
  // Validate all locations have status
  const allChecked = locations.value.every(loc => 
    inspectionData.value[loc.id]?.status
  );
  
  if (!allChecked) {
    showSnackbar({ message: '請為所有公共空間選擇電燈狀態', type: 'error' });
    return;
  }

  submitting.value = true;
  
  try {
    // Prepare patrol data
    const checks = Object.values(inspectionData.value).map(data => ({
      patrol_location_id: data.patrol_location_id,
      status: data.status,
      notes: data.notes || null
    }));

    await apiFetch('/api/v1/lights-out/', {
      method: 'POST',
      body: {
        building_id: selectedBuilding.value,
        checks
      }
    });

    showSnackbar({ message: '巡視記錄提交成功', type: 'success' });
    submitted.value = true;
  } catch (error) {
    showSnackbar({ message: '提交失敗，請重試', type: 'error' });
  } finally {
    submitting.value = false;
  }
}

function startNewPatrol() {
  submitted.value = false;
  selectedBuilding.value = null;
  locations.value = [];
  inspectionData.value = {};
}
</script>
