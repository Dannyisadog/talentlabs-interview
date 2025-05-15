<template>
  <div class="language-switcher">
    <v-menu min-width="200px">
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props" variant="text" class="lang-btn">
          <v-icon>mdi-translate</v-icon>
          <span class="ml-2">{{ getCurrentLanguageName() }}</span>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="changeLocale('en')">
          <v-list-item-title>{{ t('common.english') }}</v-list-item-title>
        </v-list-item>
        <v-list-item @click="changeLocale('zh')">
          <v-list-item-title>{{ t('common.chinese') }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

const changeLocale = (newLocale: 'en' | 'zh') => {
  locale.value = newLocale
  // Save user preference to localStorage
  localStorage.setItem('locale', newLocale)
}

const getCurrentLanguageName = () => {
  return locale.value === 'en' ? t('common.english') : t('common.chinese')
}
</script>

<style scoped>
.language-switcher {
  display: inline-block;
}
.lang-btn {
  text-transform: none;
}
</style>
