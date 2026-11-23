import type { Status } from '../api'

const names = { solved: '已通过', assisted: 'AI 协助通过', attempted: '做过没通过' }

export function ProblemStatus({ status }: { status: Status }) {
  const name = status ? names[status] : '未做'
  return <span className={`status ${status ?? 'todo'}`} role="img" aria-label={name} title={name}>
    {status === 'attempted' ? '◐' : status ? '●' : '○'}
  </span>
}
