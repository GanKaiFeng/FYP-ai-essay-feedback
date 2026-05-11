<template>
  <div class="essay-list">
    <!-- Conditional Rendering -->
    <div v-if="!selectedEssay">
      <!-- Card wrapper -->
      <div class="card">
        <h2>{{ t('essayList.title') }}</h2>

        <!-- Search Bar -->
        <input
          type="text"
          v-model="searchQuery"
          :placeholder="t('essayList.searchPlaceholder')"
          class="search-bar"
        />

        <table>
          <thead>
            <tr>
              <th>{{ t('essayList.table.title') }}</th>
              <th>{{ t('essayList.table.author') }}</th>
              <th>{{ t('essayList.table.submissionDate') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(essay, index) in paginatedEssays" :key="index">
              <td>
                <a href="#" @click.prevent="openDetail(essay)">{{ essay.title }}</a>
              </td>
              <td>{{ essay.user_id }}</td>
              <td>{{ essay.created_at }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div class="pagination">
          <button :disabled="currentPage === 1" @click="currentPage--">{{ t('essayList.prev') }}</button>
          <span>{{ t('essayList.page') }} {{ currentPage }} {{ t('essayList.of') }} {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++">{{ t('essayList.next') }}</button>
        </div>
      </div>
    </div>

    <!-- Detailed View -->
    <div v-else class="essay-detail">
      <button @click="selectedEssay = null">← {{ t('essayList.back') }}</button>
      <h2>{{ selectedEssay.title }}</h2>

      <div class="detail-columns">
        <div class="box">
          <p><strong>{{ t('essayList.detail.author') }}:</strong> {{ selectedEssay.user_id }}</p>
          <p><strong>{{ t('essayList.detail.submissionDate') }}:</strong> {{ selectedEssay.created_at }}</p>
          <p><strong>{{ t('essayList.detail.content') }}:</strong> {{ selectedEssay.essay_text }}</p>
          <p><strong>{{ t('essayList.detail.rubric') }}:</strong> {{ selectedEssay.rubric }}</p>
        </div>
        <div class="box">
          <p><strong>{{ t('essayList.detail.feedback') }}:</strong> {{ selectedEssay.strengths }}.</p>
          <p><strong>{{ t('essayList.detail.score') }}:</strong> {{ selectedEssay.score }}.</p>
        </div>
      </div>
    </div>
  </div>
</template>




<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { createClient } from '@supabase/supabase-js'

const { t } = useI18n()

// Supabase keys here
const supabase = createClient(
  //URL, key
)

const essays = ref<{ title: string }[]>([])

onMounted(async () => {
  const { data, error } = await supabase
    .from('essays')
    .select('*')
    .order('id', { ascending: false })

  if (error) {
    console.error('Failed to fetch essay titles:', error)
  } else {
    // data is assumed to be an array of { title: string }
    essays.value = data ?? []
  }
})


const selectedEssay = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 10

// Filter essays based on search
const filteredEssays = computed(() => {
  if (!searchQuery.value) return essays.value
  const q = searchQuery.value.toLowerCase()
  return essays.value.filter(
    e =>
      e.title.toLowerCase().includes(q) ||
      e.user_id.toLowerCase().includes(q)
  )
})

watch(searchQuery, () => {
  currentPage.value = 1
})

const totalPages = computed(() => Math.ceil(filteredEssays.value.length / pageSize))

const paginatedEssays = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredEssays.value.slice(start, start + pageSize)
})

// Open detail view
const openDetail = (essay) => {
  selectedEssay.value = essay
}
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-top: 16px;
}


.search-bar {
  margin-bottom: 10px;
  padding: 8px 12px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size:1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ccc;
  font-size:1.25rem;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
}

tr:hover {
  background-color: #f1f1f1;
}

.pagination {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.essay-detail {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.detail-columns {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  font-size:1.25rem;
}

.box {
  flex: 1;
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 8px;
  background-color: #fafafa;
}
</style>
