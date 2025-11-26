<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">巡視記錄</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">查看公共空間巡視歷史</p>

    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6">
      <h2 class="text-lg font-semibold mb-4">篩選條件</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2">建築物</label>
          <select 
            v-model="filters.building_id"
            @change="loadPatrols"
            class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
          >
            <option :value="null">全部建築物</option>
            <option v-for="building in buildings" :key="building.id" :value="building.id">
              {{ building.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Patrols List -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div class="p-6 border-b dark:border-gray-700">
        <h2 class="text-xl font-semibold">巡視記錄列表</h2>
      </div>

      <div class="p-6">
        <div v-if="loading" class="text-center py-8">載入中...</div>
        <div v-else-if="patrols.length === 0" class="text-center py-8 text-gray-500">
          尚無巡視記錄
        </div>
        <div v-else class="space-y-4">
          <div 
            v-for="patrol in patrols" 
            :key="patrol.id"
            class="border dark:border-gray-700 rounded-lg overflow-hidden"
          >
            <!-- Patrol Header -->
            <div 
              class="p-4 bg-gray-50 dark:bg-gray-700 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 flex justify-between items-center"
              @click="toggleDetails(patrol.id)"
            >
              <div>
                <h3 class="font-medium text-lg">{{ patrol.building.name }}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  巡視員：{{ patrol.patroller.username }} | 
                  時間：{{ formatDate(patrol.patrol_time) }}
                </p>
                <p class="text-sm mt-1">
                  <span class="text-green-600">已關閉：{{ getOffCount(patrol) }}</span> | 
                  <span class="text-amber-600">未關閉：{{ getOnCount(patrol) }}</span>
                </p>
              </div>
              <svg 
                class="w-6 h-6 transition-transform" 
                :class="{ 'rotate-180': expandedPatrols.includes(patrol.id) }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </div>

            <!-- Patrol Details -->
            <div v-if="expandedPatrols.includes(patrol.id)" class="p-4 space-y-3">
              <div 
                v-for="check in patrol.checks" 
                :key="check.id"
                class="p-3 border dark:border-gray-700 rounded-lg"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h4 class="font-medium">{{ check.location.name }}</h4>
                    <p class="text-sm text-gray-500" v-if="check.location.household">
                      戶別：{{ check.location.household }}
                    </p>
                  </div>
                  <span 
                    :class="{
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': check.status === 'off',
                      'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200': check.status === 'on'
                    }"
                    class="px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {{ check.status === 'off' ? '已關閉' : '未關閉' }}
                  </span>
                </div>
                <p v-if="check.notes" class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  備註：{{ check.notes }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="patrols.length > 0" class="mt-6 flex justify-center gap-2">
          <button 
            @click="previousPage"
            :disabled="currentPage === 1"
            class="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            上一頁
          </button>
          <span class="px-4 py-2">第 {{ currentPage }} 頁</span>
          <button 
            @click="nextPage"
            :disabled="patrols.length < pageSize"
            class="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            下一頁
          </button>
        </div>
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
const patrols = ref([]);
const loading = ref(false);
const expandedPatrols = ref([]);
const currentPage = ref(1);
const pageSize = 10;

const filters = ref({
  building_id: null
});

onMounted(async () => {
  try {
    const response = await apiFetch('/api/v1/buildings/');
    buildings.value = response;
    loadPatrols();
  } catch (error) {
    showSnackbar({ message: '載入建築物列表失敗', type: 'error' });
  }
});

async function loadPatrols() {
  loading.value = true;
  try {
    const params = new URLSearchParams({
      skip: String((currentPage.value - 1) * pageSize),
      limit: String(pageSize)
    });
    
    if (filters.value.building_id) {
      params.append('building_id', String(filters.value.building_id));
    }

    const response = await apiFetch(`/api/v1/lights-out/?${params.toString()}`);
    patrols.value = response.records || [];
  } catch (error) {
    showSnackbar({ message: '載入巡視記錄失敗', type: 'error' });
  } finally {
    loading.value = false;
  }
}

function toggleDetails(patrolId) {
  const index = expandedPatrols.value.indexOf(patrolId);
  if (index > -1) {
    expandedPatrols.value.splice(index, 1);
  } else {
    expandedPatrols.value.push(patrolId);
  }
}

function getOffCount(patrol) {
  return patrol.checks.filter(check => check.status === 'off').length;
}

function getOnCount(patrol) {
  return patrol.checks.filter(check => check.status === 'on').length;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadPatrols();
  }
}

function nextPage() {
  currentPage.value++;
  loadPatrols();
}
</script>
