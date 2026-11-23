import { useRouteLoaderData } from 'react-router-dom'
import type { TrackInfo } from './api'

// 根路由加载一次地图；提交题目后由路由刷新进度。
export function useTracks(): TrackInfo[] {
  return (useRouteLoaderData('map') as { tracks: TrackInfo[] }).tracks
}
