import type { MapUnit, TrackInfo, TrackStage } from '../api'

export type MapTab = 'python' | 'sql'

export interface Station {
  key: string
  track: TrackInfo
  stage: TrackStage
  unit: MapUnit
}

export interface Branch {
  track: TrackInfo
  stations: Station[]
  children: Branch[]
}

export function mapTree(tracks: TrackInfo[], tab: MapTab) {
  const visible = tracks.filter((t) => t.language === tab || t.language === 'none')
  const branches = new Map<string, Branch>()
  for (const track of visible) {
    const stations = track.stages.flatMap((stage) => {
      const units: MapUnit[] = track.status === 'planned'
        ? [{ id: stage.id, name: stage.name, solved: 0, total: 0, assisted: 0, attempted: 0, mastered: 0, skills: [], next: null }]
        : stage.units
      return units.map((unit) => ({ key: JSON.stringify([track.id, stage.id, unit.id]), track, stage, unit }))
    })
    branches.set(track.id, { track, stations, children: [] })
  }
  const shared = visible.find((t) => t.language === 'none' && !t.requires.length)
  const root = shared ?? visible.find((t) => !branches.has(t.requires[0]))
  const roots: Branch[] = []
  for (const branch of branches.values()) {
    const first = branch.track.requires[0]
    const parent = branches.get(first) ?? (root && branches.get(root.id))
    if (parent && parent !== branch) parent.children.push(branch)
    else roots.push(branch)
  }
  const stations = Array.from(branches.values()).flatMap((b) => b.stations)
  const upcoming = stations.filter(s => s.track.next && s.unit.next?.id === s.track.next.id &&
    s.unit.next.source === s.track.next.source)
  const next = upcoming.filter(s => s.unit.next?.due).sort((a, b) =>
    a.unit.next!.due!.localeCompare(b.unit.next!.due!))[0] ?? upcoming[0]
  return { roots, stations, next }
}
