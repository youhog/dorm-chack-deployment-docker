<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6 text-gray-900 dark:text-white">巡視記錄</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-8">查看公共空間巡視歷史</p>

    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-6 border border-gray-100 dark:border-gray-700">
      <h2 class="text-lg font-semibold mb-4 text-gray-800 dark:text-white">篩選條件</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">建築物</label>
          <select 
            v-model="filters.building_id"
            @change="loadPatrols"
            class="w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 dark:border-gray-600 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 outline-none"
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
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-100 dark:border-gray-700">
      <div class="p-6 border-b border-gray-100 dark:border-gray-700">
        <h2 class="text-xl font-semibold text-gray-800 dark:text-white">巡視記錄列表</h2>
      </div>

      <div class="p-6">
        <div v-if="loading" class="text-center py-8">
            <Icon name="lucide:loader-2" class="w-8 h-8 animate-spin text-primary-500 mx-auto" />
            <p class="mt-2 text-gray-500 dark:text-gray-400">載入中...</p>
        </div>
        <div v-else-if="patrols.length === 0" class="text-center py-12 text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
          <Icon name="lucide:clipboard-x" class="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>尚無巡視記錄</p>
        </div>
        <div v-else class="space-y-4">
          <div 
            v-for="patrol in patrols" 
            :key="patrol.id"
            class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden transition-colors hover:border-gray-300 dark:hover:border-gray-600"
          >
            <!-- Patrol Header -->
            <div 
              class="p-4 bg-gray-50 dark:bg-gray-700/30 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/50 flex justify-between items-center transition-colors"
              @click="toggleDetails(patrol.id)"
            >
              <div>
                <h3 class="font-medium text-lg text-gray-900 dark:text-white">{{ patrol.building.name }}</h3>
                <div class="flex flex-wrap gap-x-4 gap-y-1 mt-1 text-sm text-gray-600 dark:text-gray-400">
                    <span class="flex items-center gap-1"><Icon name="lucide:user" class="w-3.5 h-3.5" /> {{ patrol.patroller.username }}</span>
                    <span class="flex items-center gap-1"><Icon name="lucide:clock" class="w-3.5 h-3.5" /> {{ formatDate(patrol.patrol_time) }}</span>
                </div>
                <div class="text-sm mt-2 flex gap-3">
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                    已關閉：{{ getOffCount(patrol) }}
                  </span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400">
                    未關閉：{{ getOnCount(patrol) }}
                  </span>
                </div>
              </div>
              <Icon 
                name="lucide:chevron-down"
                class="w-5 h-5 text-gray-400 transition-transform duration-200" 
                :class="{ 'rotate-180': expandedPatrols.includes(patrol.id) }"
              />
            </div>

            <!-- Patrol Details -->
            <div v-if="expandedPatrols.includes(patrol.id)" class="p-4 space-y-3 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
              <div 
                v-for="check in patrol.checks" 
                :key="check.id"
                class="p-3 border border-gray-100 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-900 dark:text-white flex items-center gap-2">
                        {{ check.location.name }}
                        <span v-if="check.location.household" class="text-xs px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-gray-500 dark:text-gray-400">
                            {{ check.location.household }}
                        </span>
                    </h4>
                  </div>
                  <span 
                    :class="{
                      'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400': check.status === 'off',
                      'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400': check.status === 'on'
                    }"
                    class="px-2.5 py-1 rounded-md text-xs font-bold flex items-center gap-1"
                  >
                    <Icon :name="check.status === 'off' ? 'lucide:check' : 'lucide:alert-circle'" class="w-3.5 h-3.5" />
                    {{ check.status === 'off' ? '已關閉' : '未關閉' }}
                  </span>
                </div>
                <div v-if="check.notes" class="mt-2 text-sm text-gray-600 dark:text-gray-400 flex items-start gap-1.5 bg-gray-50 dark:bg-gray-900/50 p-2 rounded">
                  <Icon name="lucide:file-text" class="w-3.5 h-3.5 mt-0.5 text-gray-400" />
                  <span>{{ check.notes }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="patrols.length > 0" class="mt-6 flex justify-center gap-2">
          <button 
            @click="previousPage"
            :disabled="currentPage === 1"
            class="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-white"
          >
            上一頁
          </button>
          <span class="px-4 py-2">第 {{ currentPage }} 頁</span>
          <button 
            @click="nextPage"
            :disabled="patrols.length < pageSize"
            class="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700 dark:border-gray-600 dark:bg-gray-800 dark:text-white"
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
