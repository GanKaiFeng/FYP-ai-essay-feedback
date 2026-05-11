<template>
  <div class="home">
    <section class="grid">
      <!-- Left column stacked xlarge cards -->
      <div class="card xlarge left-top">
        <h3 class="card-title">{{ t('home.recentEssay') }}</h3>
        <div v-if="latestEssay">
          <h4>{{ latestEssay.title }}</h4>
          <p style="white-space: pre-wrap;">{{ latestEssay.essay_text }}</p>
          <small class="caption">{{ t('home.uploaded') }}: {{ new Date(latestEssay.created_at).toLocaleString() }}</small>
        </div>
        <div v-else>
          <p>{{ t('home.loadingEssay') }}</p>
        </div>
      </div>

      <div class="card xlarge left-bottom">
        <div class="project-title">
          <h3 class="card-title">{{ t('home.recentFeedback') }}</h3>
        </div>

        <div v-if="latestEssay?.strengths">
          <h4>{{ t('home.strengths') }}</h4>
          <p style="white-space: pre-wrap;">{{ latestEssay.strengths }}</p>
          <h4>{{ t('home.essayScore') }}</h4>
          <p class="score-number">{{ latestEssay.score }}</p>
        </div>
        <div v-else>
          <p>{{ t('home.noStrengths') }}</p>
        </div>
      </div>
    </section>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { createClient } from '@supabase/supabase-js'

const { t } = useI18n()

// Supabase keys here
const supabase = createClient(
  //URL, key
)

const latestEssay = ref<{
  title: string
  content: string
  strengths: string
  score: number
  created_at: string
} | null>(null)


onMounted(async () => {
  const { data, error } = await supabase
    .from('essays')  // Replace with your actual table name
    .select('*')
    .order('id', { ascending: false })
    .limit(1)
    .single()

  if (error) {
    console.error('Error fetching latest essay:', error)
  } else {
    latestEssay.value = data
  }
})

</script>

<style scoped>
.home {
  padding: 20px;
  background: #f9f9f9;
  font-size: 1rem; /* base 16px for the whole page */
}

.grid {
  display: grid;
  gap: 20px;
  height: 100vh; /* Full vertical space */
}

/* Card styling */
.card {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  font-size: 1rem; /* ensure cards use 16px */
}

/* Left stacked cards */
.left-top {
  grid-column: 1;
}

.left-bottom {
  grid-column: 1;
}

/* Right column small card fills vertical space */
.right-card {
  grid-column: 2;
  grid-row: 1 / span 2; /* span both rows */
  display: flex;
  flex-direction: column;
  justify-content: start;
}

/* Chart placeholders */
.chart-placeholder {
  margin-top: 10px;
}

/* Tags and pills */
.tag-row {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

.pill {
  background: #49c2a6;
  color: #fff;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 1rem; /* 16px */
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.pill-inline {
  background: #f2c94c;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 1rem; /* 16px */
}

.legend {
  margin-top: 5px;
}

.badge {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 1rem; /* 16px */
  color: #fff;
}

.badge.blue {
  background: #49c2a6;
}

.badge.green {
  background: #27ae60;
}

.caption {
  margin-top: 10px;
  font-size: 1rem; /* 16px */
}

.score-number {
  font-size: 2rem; /* keep larger for emphasis */
  font-weight: bold;
  color: #007bff;
  margin-top: 10px;
}

/* Headings inside cards */
.card-title {
  font-size: 1.5rem; /* 16px */
  margin-bottom: 0.5em;
}

h3, h4, p {
  font-size: 1.25rem; /* 16px */
  margin: 0 0 0.5em 0;
}
</style>

