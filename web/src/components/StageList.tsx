import type { TrackInfo } from '../api'
import { unitAnchor } from '../pages/unitAnchor'

export function StageList({ track }: { track: TrackInfo }) {
  return <>
    <h1>{track.name}</h1>
    <p className="empty">{track.status === 'planned' ? '规划中' : '本线暂时没有题目'}</p>
    <ol className="stage-outline">
      {track.stages.map((stage) => <li key={stage.id} id={unitAnchor(stage.id, stage.id)}>
        <span>{stage.id}</span>{stage.name}
      </li>)}
    </ol>
  </>
}
