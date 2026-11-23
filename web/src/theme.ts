import { useCallback, useEffect, useState } from 'react'

export type Theme = 'dark' | 'light'

function readTheme(): Theme {
  return document.documentElement.dataset.theme === 'light' ? 'light' : 'dark'
}

/** 主题：默认深色，切换是硬切（不做过渡动画），记在 localStorage。 */
export function useTheme(): [Theme, () => void] {
  const [theme, setTheme] = useState<Theme>(readTheme)
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('dojo-theme', theme)
  }, [theme])
  const toggle = useCallback(() => setTheme((t) => (t === 'dark' ? 'light' : 'dark')), [])
  return [theme, toggle]
}

export function readPref(key: string, fallback: string): string {
  return localStorage.getItem(key) ?? fallback
}

export function writePref(key: string, value: string | null): void {
  if (value === null) localStorage.removeItem(key)
  else localStorage.setItem(key, value)
}
