function isSupportLS() {
  try {
    localStorage.setItem('__test-key__', 'hi')
    localStorage.getItem('__test-key__')
    localStorage.removeItem('__test-key__')
    return true
  } catch (e) {
    return false
  }
}

class Memory {
  cache: Record<string, any>
  constructor() {
    this.cache = {}
  }
  setItem(cacheKey: string, data: any) {
    this.cache[cacheKey] = data
  }
  getItem(cacheKey: string) {
    return this.cache[cacheKey]
  }
  removeItem(cacheKey: string) {
    delete this.cache[cacheKey]
  }
}

// if not support localStorage, fallback to memory
export const storage = isSupportLS() ? window.localStorage : new Memory();