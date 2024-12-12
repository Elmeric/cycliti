/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_WEBSTORAGE_NAMESPACE: string
  readonly VITE_BACKEND_PROTOCOL: string
  readonly VITE_BACKEND_HOST: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_STRAVA_CLIENT_ID: string
  readonly SECRET_KEY: string
    // more env variables...
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
