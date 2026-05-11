<template>
  <div class="app">
    <!-- Left Sidebar Navigation -->
    <aside class="leftbar">
      <!-- Logo -->
      <div class="logo">Logo</div>

      <!-- Navigation Buttons -->
      <nav class="nav">
        <button class="nav-btn" @click="currentPage = 'home'">{{ $t('nav.home') }}</button>
        <button class="nav-btn" @click="currentPage = 'essayList'">{{ $t('nav.essayList') }}</button>
        <button class="nav-btn" @click="currentPage = 'teacherUpload'">{{ $t('nav.teacherUpload') }}</button>
        <button class="nav-btn" @click="currentPage = 'studentUpload'">{{ $t('nav.studentUpload') }}</button>
      </nav>

      <!-- Settings and Logout Buttons -->
      <div class="left-actions">
        <button class="circle">{{ $t('buttons.setting') }}</button>
        <button class="circle">{{ $t('buttons.logout') }}</button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main">
      <!-- Top Greeting -->
      <header class="top">
        <div class="greeting">
          <div>
            <h1>{{ $t('greeting') }}</h1>
            <p>{{ $t('navigate') }}</p>
          </div>

          <!-- Language Buttons -->
          <div class="lang-switcher">
            <button @click="changeLanguage('en')">{{ $t('buttons.lang_en') }}</button>
            <button @click="changeLanguage('zh')">{{ $t('buttons.lang_zh') }}</button>
          </div>
        </div>
      </header>

      <!-- Dynamic Page Rendering -->
      <section class="page-container">
        <Home v-if="currentPage === 'home'" />
        <EssayList v-if="currentPage === 'essayList'" />
        <TeacherUpload v-if="currentPage === 'teacherUpload'" />
        <StudentUpload v-if="currentPage === 'studentUpload'" />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

import Home from './components/Home.vue'
import EssayList from './components/EssayList.vue'
import TeacherUpload from './components/TeacherUpload.vue'
import StudentUpload from './components/StudentUpload.vue'

const currentPage = ref('essayList')

// i18n
const { locale } = useI18n()
const changeLanguage = (lang: string) => {
  locale.value = lang
}
</script>

<style scoped>
:root {
  --border: #cfcfcf;
  --muted: #f7f7f7;
  --accent: #7aa;
  --font-size: 1rem; /* base 16px */
}

* {
  box-sizing: border-box;
}

:global(body), :global(html), :global(#app) {
  height: 100%;
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, Segoe UI, Roboto, 'Helvetica Neue', Arial;
  font-size: var(--font-size); /* base 16px */
}

/* second largest card, covers all the other cards */
.app {
  display: flex;
  background: #eeeff2;
  min-height: 100vh; /* ensures app fills viewport */
}

.leftbar {
  width: 120px; /* increased from 100px */
  height: 100vh; /* <-- make sidebar full height */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px; /* increased from 20px */
  padding: 10px 0; /* increased from 8px */
  background: #2a2f33;
  position: fixed;   /* <-- stick to the left edge */
  top: 0;
  left: 0;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 24px;
  margin-left: 120px; /* offset matches new sidebar width */
}

.logo {
  width: 68px; /* increased from 56px */
  height: 68px; /* increased from 56px */
  border-radius: 12px; /* increased from 10px */
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 1.2rem; /* increased from 1rem */
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 16px; /* increased from 14px */
  margin-top: 10px; /* increased from 8px */
}

.nav-btn {
  width: 76px; /* increased from 64px */
  min-height: 76px; /* increased from 64px */
  border-radius: 16px; /* increased from 14px */
  border: 2px solid var(--border);
  background: #fff;
  font-size: 1rem;
  padding: 6px; /* increased from 4px */
  text-align: center;
  white-space: normal;
  word-break: break-word;
}

.left-actions {
  display: flex;
  flex-direction: column;
  gap: 14px; /* increased from 12px */
  margin-top: auto;
}

.circle {
  width: 76px; /* increased from 64px */
  min-height: 46px; /* increased from 38px */
  border-radius: 22px; /* increased from 18px */
  border: 2px solid var(--border);
  background: #fff;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 6px; /* increased from 4px */
  text-align: center;
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

/* greeting card, top horizontal card */
.greeting {
  flex: 1;
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 14px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
}

.greeting h1 {
  margin: 0;
  font-size: 1.375rem; /* 22px */
}

.greeting p {
  margin: 6px 0 0;
  font-size: 1rem; /* 16px */
  color: #666;
}

.lang-switcher {
  display: flex;
  gap: 10px;
}

.lang-switcher button {
  padding: 8px 12px; /* increased from 6px 10px */
  border-radius: 12px;
  border: 1px solid var(--border);
  background: white;
  font-size: 1rem; /* unchanged: still 16px */
  cursor: pointer;
}
</style>
