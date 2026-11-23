import type { Format, Verdict, CaseStatus } from './api'

// 题型用一个字表示，列表里省地方
export const FORMAT_GLYPH: Record<Format, string> = {
  inspect: '看',
  predict: '读',
  complete: '补',
  fix: '改',
  write: '写',
  variant: '变',
  combine: '合',
}

export const FORMAT_NAME: Record<Format, string> = {
  inspect: '看数据作答',
  predict: '预测输出',
  complete: '补全',
  fix: '改错',
  write: '编写',
  variant: '变式',
  combine: '组合',
}

export const VERDICT_NAME: Record<Verdict, string> = {
  accepted: '通过',
  passed: '通过',
  wrong_answer: '答案错误',
  runtime_error: '运行错误',
  timeout: '超时',
  skipped: '未运行',
  compile_error: '语法错误',
  constraint_error: '写法不符',
  system_error: '判题出错',
}

export function verdictTone(v: Verdict | CaseStatus): 'pass' | 'fail' | 'muted' {
  if (v === 'accepted' || v === 'passed') return 'pass'
  if (v === 'skipped') return 'muted'
  return 'fail'
}
