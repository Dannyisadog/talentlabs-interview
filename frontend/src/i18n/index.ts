import { createI18n } from 'vue-i18n'
import en from './locales/en'
import zh from './locales/zh'

export type MessageSchema = typeof en

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    zh
  }
})

export default i18n 