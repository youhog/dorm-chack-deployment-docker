<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <!-- Stat Cards -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-100 dark:border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">本月巡視次數</h3>
        <div class="p-2 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
          <Icon name="heroicons:clipboard-document-check" class="w-6 h-6 text-blue-600 dark:text-blue-400" />
        </div>
      </div>
      <div class="flex items-baseline">
        <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalPatrols }}</span>
        <span class="ml-2 text-sm text-green-600 dark:text-green-400 flex items-center">
          <Icon name="heroicons:arrow-trending-up" class="w-4 h-4 mr-1" />
          {{ stats.patrolsGrowth }}%
        </span>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-100 dark:border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">未關閉電源總數</h3>
        <div class="p-2 bg-amber-50 dark:bg-amber-900/30 rounded-lg">
          <Icon name="heroicons:light-bulb" class="w-6 h-6 text-amber-600 dark:text-amber-400" />
        </div>
      </div>
      <div class="flex items-baseline">
        <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalIssues }}</span>
        <span class="ml-2 text-sm text-red-600 dark:text-red-400 flex items-center">
          <Icon name="heroicons:arrow-trending-up" class="w-4 h-4 mr-1" />
          {{ stats.issuesGrowth }}%
        </span>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-100 dark:border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">異常率</h3>
        <div class="p-2 bg-red-50 dark:bg-red-900/30 rounded-lg">
          <Icon name="heroicons:exclamation-triangle" class="w-6 h-6 text-red-600 dark:text-red-400" />
        </div>
      </div>
      <div class="flex items-baseline">
        <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.abnormalRate }}%</span>
        <span class="ml-2 text-sm text-gray-500 dark:text-gray-400">
          平均
        </span>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-100 dark:border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">巡視涵蓋率</h3>
        <div class="p-2 bg-green-50 dark:bg-green-900/30 rounded-lg">
          <Icon name="heroicons:map" class="w-6 h-6 text-green-600 dark:text-green-400" />
        </div>
      </div>
      <div class="flex items-baseline">
        <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.coverageRate }}%</span>
        <span class="ml-2 text-sm text-green-600 dark:text-green-400">
          良好
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  stats: {
    totalPatrols: number;
    patrolsGrowth: number;
    totalIssues: number;
    issuesGrowth: number;
    abnormalRate: number;
    coverageRate: number;
  }
}>();
</script>
