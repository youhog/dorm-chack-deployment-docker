<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
            <h1 class="text-3xl font-bold text-gray-800 dark:text-white">巡視分析儀表板</h1>
            <p class="text-gray-600 dark:text-gray-400 mt-1">查看公共空間巡視的統計數據與趨勢</p>
        </div>
        
        <!-- Date Range Filter -->
        <div class="bg-white dark:bg-gray-800 p-1 rounded-lg border border-gray-200 dark:border-gray-700 flex shadow-sm">
            <button 
                v-for="range in dateRanges" 
                :key="range.value"
                @click="selectedRange = range.value"
                :class="[
                    'px-4 py-2 text-sm font-medium rounded-md transition-all',
                    selectedRange === range.value
                        ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/50 dark:text-primary-300'
                        : 'text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-700'
                ]"
            >
                {{ range.label }}
            </button>
        </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-20">
      <Icon name="lucide:loader-2" class="w-10 h-10 animate-spin text-primary-500" />
    </div>

    <div v-else class="space-y-8 animate-in fade-in duration-500">
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400 rounded-lg">
              <Icon name="lucide:clipboard-check" class="w-6 h-6" />
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">總巡邏次數</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalPatrols }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 rounded-lg">
              <Icon name="lucide:alert-circle" class="w-6 h-6" />
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">發現異常 (未關燈)</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalViolations }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400 rounded-lg">
              <Icon name="lucide:percent" class="w-6 h-6" />
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">平均每筆異常數</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.violationAvg }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Trend Chart (Simple CSS Bar Chart) -->
      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 class="text-lg font-bold mb-6 text-gray-800 dark:text-white flex items-center gap-2">
              <Icon name="lucide:bar-chart-2" class="w-5 h-5" />
              違規趨勢分析 ({{ trendTitle }})
          </h3>
          
          <div class="flex items-end justify-between h-48 gap-2">
              <div v-if="stats.trend.length === 0" class="w-full h-full flex items-center justify-center text-gray-400">
                  無數據
              </div>
              <div 
                  v-for="(point, idx) in stats.trend" 
                  :key="idx" 
                  class="flex-1 flex flex-col items-center group relative"
              >   
                  <!-- Tooltip -->
                  <div class="absolute bottom-full mb-2 opacity-0 group-hover:opacity-100 transition-opacity bg-gray-900 text-white text-xs px-2 py-1 rounded whitespace-nowrap pointer-events-none z-10">
                      {{ point.label }}: {{ point.value }} 次
                  </div>

                  <!-- Bar -->
                  <div 
                      class="w-full max-w-[20px] bg-primary-200 dark:bg-primary-900/50 rounded-t-sm relative overflow-hidden transition-all duration-500 group-hover:bg-primary-300 dark:group-hover:bg-primary-800"
                      :style="{ height: (point.percent || 1) + '%' }"
                  >
                      <div class="absolute bottom-0 left-0 right-0 bg-primary-500 transition-all duration-500" :style="{ height: point.percent + '%' }"></div>
                  </div>
                  
                  <!-- Label -->
                  <span class="text-[10px] text-gray-400 mt-2 truncate w-full text-center">{{ point.shortLabel }}</span>
              </div>
          </div>
      </div>

      <!-- Detail Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Building Stats -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 class="text-lg font-bold mb-4 text-gray-800 dark:text-white">各建築物異常統計</h3>
          <div class="space-y-4">
            <div v-for="(count, name) in stats.byBuilding" :key="name">
              <div class="flex justify-between text-sm mb-1 text-gray-600 dark:text-gray-300">
                <span>{{ name }}</span>
                <span>{{ count }} 次</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2.5">
                <div 
                  class="bg-red-500 h-2.5 rounded-full transition-all duration-500" 
                  :style="{ width: getBarWidth(count, stats.byBuilding) + '%' }"
                ></div>
              </div>
            </div>
            <div v-if="Object.keys(stats.byBuilding).length === 0" class="text-center text-gray-400 py-4">無數據</div>
          </div>
        </div>

        <!-- Location Stats -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 class="text-lg font-bold mb-4 text-gray-800 dark:text-white">各位置異常統計</h3>
          <div class="space-y-4">
            <div v-for="(count, name) in stats.byLocation" :key="name">
              <div class="flex justify-between text-sm mb-1 text-gray-600 dark:text-gray-300">
                <span>{{ name }}</span>
                <span>{{ count }} 次</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2.5">
                <div 
                  class="bg-amber-500 h-2.5 rounded-full transition-all duration-500" 
                  :style="{ width: getBarWidth(count, stats.byLocation) + '%' }"
                ></div>
              </div>
            </div>
            <div v-if="Object.keys(stats.byLocation).length === 0" class="text-center text-gray-400 py-4">無數據</div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h3 class="text-lg font-bold mb-4 text-gray-800 dark:text-white">近期違規記錄</h3>
          <div class="space-y-3">
            <div 
              v-for="patrol in recentViolations" 
              :key="patrol.id"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-100 dark:border-gray-700"
            >
              <div>
                <p class="font-medium text-gray-800 dark:text-gray-200">{{ patrol.building.name }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(patrol.patrol_time) }}</p>
              </div>
              <div class="flex gap-1">
                  <span class="text-sm font-bold text-red-600 dark:text-red-400">
                    {{ getOnCount(patrol) }} 處異常
                  </span>
              </div>
            </div>
            <div v-if="recentViolations.length === 0" class="text-center text-gray-400 py-4">近期無違規</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useSnackbar } from '~/composables/useSnackbar';

const { apiFetch } = useAuth();
const { showSnackbar } = useSnackbar();

const loading = ref(false);
const rawData = ref([]);
const selectedRange = ref('semester'); // Default to semester

const dateRanges = [
    { label: '本週', value: 'week' },
    { label: '本月', value: 'month' },
    { label: '本學期', value: 'semester' },
    { label: '全部', value: 'all' }
];

const trendTitle = computed(() => {
    switch (selectedRange.value) {
        case 'week': return '每日';
        case 'month': return '每日';
        case 'semester': return '每週';
        default: return '趨勢';
    }
});

// Helper to get date ranges
const getDateParams = () => {
    const now = new Date();
    let start = new Date();
    
    switch (selectedRange.value) {
        case 'week':
            // Start of week (Monday)
            const day = now.getDay();
            const diff = now.getDate() - day + (day === 0 ? -6 : 1);
            start.setDate(diff);
            start.setHours(0,0,0,0);
            break;
        case 'month':
            start.setDate(1);
            start.setHours(0,0,0,0);
            break;
        case 'semester':
            // Simple semester logic: 
            // First: 8/1 - 1/31
            // Second: 2/1 - 7/31
            const month = now.getMonth() + 1; // 1-12
            if (month >= 8 || month <= 1) {
                // First Semester
                if (month <= 1) start.setFullYear(now.getFullYear() - 1);
                start.setMonth(7, 1); // Aug 1st
            } else {
                // Second Semester
                start.setMonth(1, 1); // Feb 1st
            }
            start.setHours(0,0,0,0);
            break;
        case 'all':
            return {};
    }
    
    return { start_date: start.toISOString() };
};

const fetchData = async () => {
    loading.value = true;
    try {
        const params = new URLSearchParams({ limit: '1000' }); // Increase limit for stats
        const dateParams = getDateParams();
        if (dateParams.start_date) params.append('start_date', dateParams.start_date);
        
        const response = await apiFetch(`/api/v1/lights-out/?${params.toString()}`);
        rawData.value = response.records || [];
    } catch (error) {
        showSnackbar({ message: '載入統計數據失敗', type: 'error' });
    } finally {
        loading.value = false;
    }
};

watch(selectedRange, fetchData);

const stats = computed(() => {
  const totalPatrols = rawData.value.length;
  let totalViolations = 0;
  const byBuilding: Record<string, number> = {};
  const byLocation: Record<string, number> = {};
  
  // Trend Data Grouping
  const trendMap: Record<string, number> = {};

  rawData.value.forEach(patrol => {
    const violationCount = getOnCount(patrol);
    totalViolations += violationCount;
    
    // Building Stats
    const bName = patrol.building.name;
    if (!byBuilding[bName]) byBuilding[bName] = 0;
    byBuilding[bName] += violationCount;

    // Location Stats
    patrol.checks.forEach((check: any) => {
        if (check.status === 'on') {
            const locName = check.location.name;
            if (!byLocation[locName]) byLocation[locName] = 0;
            byLocation[locName]++;
        }
    });

    // Trend Stats
    const pDate = new Date(patrol.patrol_time);
    let key = '';
    
    if (selectedRange.value === 'semester') {
        // Group by Week (ISO week number)
        // Simple approx: Month/Day
        const startOfWeek = new Date(pDate);
        startOfWeek.setDate(pDate.getDate() - pDate.getDay() + 1);
        key = `${startOfWeek.getMonth()+1}/${startOfWeek.getDate()} 週`;
    } else {
        // Group by Day
        key = `${pDate.getMonth()+1}/${pDate.getDate()}`;
    }
    
    if (!trendMap[key]) trendMap[key] = 0;
    trendMap[key] += violationCount;
  });

  const violationAvg = totalPatrols > 0 ? (totalViolations / totalPatrols).toFixed(1) : '0';

  // Process Trend Data for Chart
  // We should ideally fill in missing dates, but for now just sort existing
  // Or sort keys simply
  const trendKeys = Object.keys(trendMap).reverse(); // Reverse because API returns desc? No, we iterate.
  // Actually, rawData is usually sorted by date desc. So iterating creates desc trend.
  // We need to reverse it to be chronological.
  
  // Let's sort rawData by date asc first to build trend
  const sortedRaw = [...rawData.value].sort((a, b) => new Date(a.patrol_time).getTime() - new Date(b.patrol_time).getTime());
  
  const trendMapAsc: Record<string, number> = {};
  sortedRaw.forEach(patrol => {
      const pDate = new Date(patrol.patrol_time);
      const violationCount = getOnCount(patrol);
      let key = '';
      if (selectedRange.value === 'semester') {
        const startOfWeek = new Date(pDate);
        startOfWeek.setDate(pDate.getDate() - (pDate.getDay() || 7) + 1); // Monday
        key = `${startOfWeek.getMonth()+1}/${startOfWeek.getDate()}`;
      } else {
        key = `${pDate.getMonth()+1}/${pDate.getDate()}`;
      }
      if (!trendMapAsc[key]) trendMapAsc[key] = 0;
      trendMapAsc[key] += violationCount;
  });

  const maxVal = Math.max(...Object.values(trendMapAsc), 1);
  const trend = Object.entries(trendMapAsc).map(([label, value]) => ({
      label,
      shortLabel: label,
      value,
      percent: (value / maxVal) * 100
  }));

  return {
    totalPatrols,
    totalViolations,
    violationAvg,
    byBuilding,
    byLocation,
    trend
  };
});

const recentViolations = computed(() => {
    return rawData.value.filter(p => getOnCount(p) > 0).slice(0, 5);
});

onMounted(() => {
    fetchData();
});

function getOnCount(patrol) {
  return patrol.checks.filter(check => check.status === 'on').length;
}

function getBarWidth(count: number, dataset: Record<string, number>) {
  const max = Math.max(...Object.values(dataset), 1);
  return (count / max) * 100;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-TW', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
}
</script>