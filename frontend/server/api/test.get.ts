// File: server/api/test.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  
  return { 
    message: 'Server API berfungsi dengan baik!',
    timestamp: new Date().toISOString(),
    hasGeminiKey: !!config.GEMINI_API_KEY,
    environment: process.env.NODE_ENV || 'development'
  }
})