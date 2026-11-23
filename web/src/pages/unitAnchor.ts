import { useLayoutEffect } from 'react'
import { useLocation } from 'react-router-dom'

export function unitAnchor(stage: string, unit: string) {
  return `u-${stage}-${unit}`
}

/** 路由的数据加载完、锚点进入文档后再定位。 */
export function useUnitAnchor() {
  const { hash, key } = useLocation()
  useLayoutEffect(() => {
    if (hash) document.getElementById(decodeURIComponent(hash.slice(1)))?.scrollIntoView()
  }, [hash, key])
}
