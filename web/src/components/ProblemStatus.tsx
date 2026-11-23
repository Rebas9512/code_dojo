import type { Status } from '../api'

export const STATUS_NAME = { solved: '已通过', assisted: 'AI 协助通过', attempted: '做过没通过' }

export function ProblemStatus({ status }: { status: Status }) {
  const name = status ? STATUS_NAME[status] : '未做'
  return <span className={`status ${status ?? 'todo'}`} role="img" aria-label={name} title={name}>
    {status === 'attempted' ? '◐' : status ? '●' : '○'}
  </span>
}
