<template>
  <div class="card upload-card">
    <div class="card-header">
      <h2 class="card-title">
        <i class="fas fa-upload"></i> {{ t('upload.title') }}
      </h2>
      <span class="badge">{{ t('upload.aiBadge') }}</span>
    </div>

    <!-- Feedback View -->
    <div v-if="feedbackData">
      <h3>{{ t('upload.feedbackReceived') }}</h3>

      <div class="feedback-item">
        <strong>{{ t('upload.essayTitle') }}:</strong> {{ feedbackData.title }}
      </div>
      <div class="feedback-item">
        <strong>{{ t('home.essayScore') }}:</strong> {{ feedbackData.score }}
      </div>
      <div class="feedback-item">
        <strong>{{ t('home.strengths') }}:</strong>
        <p style="white-space: pre-wrap; word-wrap: break-word;">{{ feedbackData.strengths }}</p>
      </div>

      <button class="btn btn-secondary" @click="resetFeedback">
        ← {{ t('upload.backToUpload') }}
      </button>
    </div>


    <!-- Form View -->
    <form v-else @submit.prevent="handleSubmit">
      <div class="form-container">

        <!-- Left Box -->
        <div class="form-box form-left">
          <!-- Essay Title -->
          <div class="form-group">
            <label for="title">{{ t('upload.essayTitle') }}</label>
            <select v-model="form.title" @change="onTitleSelect">
              <option value="">{{ t('upload.selectTitle') }}</option>
              <option v-for="t in essayTitles" :key="t.id" :value="t.title">
                {{ t.title }}
              </option>
            </select>
            <input
              id="title"
              v-model="form.title"
              required
              :placeholder="t('upload.typeNewTitle')"
              style="margin-top: 10px;box-sizing: border-box;"
            />
          </div>

          <!-- Essay Content -->
          <div class="form-group">
            <label for="content">{{ t('upload.essayContent') }}</label>
            <div class="input-group">
              <textarea
                id="content"
                v-model="form.content"
                class="essay-textarea"
                :placeholder="t('upload.pasteEssay')"
                required
                style="box-sizing: border-box;"
              ></textarea>

              <div class="ocr-button">
                <input
                  type="file"
                  ref="fileInput"
                  accept="application/pdf,image/*"
                  @change="handleImageUpload"
                  style="display: none;box-sizing: border-box;"
                />
                <button
                  type="button"
                  @click="triggerFileInput"
                  class="btn btn-secondary"
                  :disabled="isUploading"
                >
                  {{ t('upload.uploadOCR') }}
                </button>
              </div>
            </div>
            <p class="hint-text">{{ t('upload.essayHint') }}</p>
          </div>
        </div>

        <!-- Right Box -->
        <div class="form-box form-right">
          <!-- Essay Type -->
          <div class="form-group">
            <label for="type">{{ t('upload.essayType') }}</label>
            <select id="type" v-model="form.type">
              <option value="argumentative">{{ t('upload.argumentative') }}</option>
              <option value="narrative">{{ t('upload.narrative') }}</option>
            </select>
          </div>

          <!-- Rubric -->
          <div class="form-group">
            <label for="rubric">{{ t('upload.rubric') }}</label>
            <select v-model="form.rubric" @change="onTitleSelect">
              <option value="">{{ t('upload.selectRubric') }}</option>
              <option v-for="t in essayTitles" :key="t.id" :value="t.rubric">
                {{ t.rubric }}
              </option>
            </select>
            <textarea
              id="rubric"
              v-model="form.rubric"
              required
              class="rubric-textarea"
              :placeholder="t('upload.typeNewRubric')"
              style="margin-top: 10px;box-sizing: border-box;"
            ></textarea>
          </div>

          <!-- Model Selection -->
          <div class="form-group">
            <label for="model">{{ t('upload.model') }}</label>
            <select id="model" v-model="form.model">
              <option value="gpt-4">GPT-4</option>
              <option value="claude-4">Claude 4</option>
              <option value="qwen-3">Qwen 3</option>
            </select>
          </div>

          <!-- Buttons -->
          <div class="button-group">
            <button type="button" class="btn btn-secondary" @click="resetForm">
              <i class="fas fa-undo"></i> {{ t('upload.reset') }}
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="isUploading"
            >
              <i class="fas fa-paper-plane"></i> {{ t('upload.submit') }}
            </button>
          </div>

          <div v-if="isUploading" class="loading-overlay">
            <div class="loading-popup">
              <span class="spinner"></span>
              <p>{{ t('upload.processingImage') }}</p>
            </div>
          </div>
        </div>

      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createClient } from '@supabase/supabase-js'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Props and Emits
const props = defineProps<{ role: string }>()
const emit = defineEmits<{
  (e: 'feedback', data: any): void
}>()

// Form State
const form = ref({
  title: '',
  content: '',
  type: 'argumentative',
  rubric: '',
  model: 'gpt-4',
  detail: 'high'
})

// Reset
function resetForm() {
  form.value = {
    title: '',
    content: '',
    type: 'argumentative',
    rubric: '',
    model: 'gpt-4',
    detail: 'high'
  }
}


// Submit
async function handleSubmit() {
  try {
    const response = await fetch('http://localhost:5051/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })

    const data = await response.json()
    feedbackData.value = data
  } catch (error) {
    console.error("Fetch error:", error)
    alert("Something went wrong. Check server logs.")
  }
}

const feedbackData = ref<any | null>(null)
function resetFeedback() {
  feedbackData.value = null
  resetForm()
}


// Supabase: Fetch essay titles
// Supabase keys here
const supabase = createClient(
  //URL, key
)

const essayTitles = ref<{ id: string; title: string; type: string }[]>([])

onMounted(async () => {
  const { data, error } = await supabase
    .from('essay_titles')
    .select('*')
    .order('id', { ascending: false })

  if (error) {
    console.error('Failed to fetch titles:', error)
  } else {
    essayTitles.value = data ?? []
  }
})

// Match type from title
function onTitleSelect() {
  const selected = essayTitles.value.find(t => t.title === form.value.title)
  if (selected?.type) {
    form.value.type = selected.type
    form.value.rubric = selected.rubric
  }
}

//Upload handling
const isUploading = ref(false)

// OCR
const fileInput = ref<HTMLInputElement | null>(null)

function triggerFileInput() {
  fileInput.value?.click()
}

async function handleImageUpload(event: Event) {
  const file = (event.target as HTMLInputElement)?.files?.[0]
  if (!file) return

  isUploading.value = true

  const reader = new FileReader()
  reader.onload = async (e) => {
    const base64Image = e.target?.result
    if (!base64Image) {
      isUploading.value = false
      return
    }

    try {
      const response = await fetch('http://localhost:5051/api/ocr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image })
      })

      const data = await response.json()
      if (data.text) {
        form.value.content = data.text
      } else {
        alert('OCR failed: ' + (data.error || 'Unknown error'))
      }
    } catch (error) {
      console.error("OCR failed:", error)
      alert('OCR request failed. Try again.')
    } finally {
      isUploading.value = false
    }
  }

  reader.readAsDataURL(file)
}

</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.form-box {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex: 1 1 350px;
  min-width: 300px;
}

.form-left {
  flex: 2;
}

.form-right {
  flex: 1;
}

.upload-card {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 24px;
}


.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/*AI powered text badge*/
.badge {
  background-color: #007bff;
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

/* Dropdown selector text*/
textarea,
input[type="text"],
select {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.essay-textarea {
  min-height: 140px;
  resize: vertical;
  font-size: 1.25rem;
}

.rubric-textarea {
  min-height: 140px;
  resize: vertical;
  font-size: 1.25rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ocr-button {
  display: flex;
  justify-content: flex-end;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-popup {
  background: white;
  border-radius: 10px;
  padding: 20px 30px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  font-size: 16px;
  color: #333;
}

.spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 4px solid #007bff;
  border-top: 4px solid transparent;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

</style>
