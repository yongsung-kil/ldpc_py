---
summary: max_iter 120을 기준으로 잡고, 가속은 numpy 프레임 배치 벡터화만 쓰며(numba 미사용), 병렬화는 mpi4py로 코어당 시뮬레이션 1개를 띄운다. mpi_runner는 새 구조 기준으로 재설계 대기 중이다
status: Accepted
tags: [simulation, performance, parallel]
date: 2026-07-30
commit: 0394b81 (시험장 사본에 포함)
source: README.md "확정 결정 기록" 절 (:221), _pm/DONE.md 2026-07-30 항목 (측정과 결정 사항)과 2026-08-07 "개정본 본체 반영" ㉮, _pm/TODO.md:32-33, 41, docs/profile/constraints.md:45, docs/profile/overview.md:26
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 2026-07-30 뼈대 구현 뒤 측정에서 1000 frames를 120 iteration으로 돌리면 코어당 60초에서 133초였다
  - ㉡ LLR 테이블이 iteration 구간을 정의하므로 max_iter의 기준값이 필요했다
- ㉯ 거부한 대안
  - ㉠ numba JIT 가속
  - ㉡ 프로세스 안 멀티스레딩
- ㉰ 이유
  - ㉠ 프레임 배치 벡터화만으로 속도가 충분했다. 의존성과 디버깅 부담을 줄인다 (이력 기록에는 "numba 안 함"만 있고 상세 이유 문장은 없다. 이 줄은 추정이다)
  - ㉡ 코어당 시뮬레이션 1개면 프로세스 사이에 공유 상태가 없어 단순하다
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ 서드파티 의존은 numpy(필수)와 matplotlib(그림 저장에만)뿐이다 (docs/profile/overview.md:26)
  - ㉡ 배열 축은 (B, N_b, z)로 고정된다. B는 `frames_per_batch`
  - ㉢ max_iter 120은 기준값일 뿐이다. LLR 파일 로드 경로에서는 파일의 마지막 iter_end가 max_iter를 정하므로 파일 값이 우선한다
  - ㉣ 구 mpi_runner는 2026-08-07 본체 반영 때 삭제됐고 `src.run` 기준으로 새로 설계하기로 했다 (사용자 확정 2026-08-07, 나중에 진행). 현재 병렬 import는 0건이다. 슈퍼컴 이관은 재설계 완료 뒤다
- 날짜: 2026-07-30 (방침), 2026-08-07 (mpi_runner 재설계 보류)

## 하위 링크

- [../../README.md](../../README.md): "확정 결정 기록" 절의 "시뮬 방침" 행
- [../../docs/profile/overview.md](../../docs/profile/overview.md): 실행 환경 표 (언어, 의존 패키지, 실행 방법)
- [../../docs/profile/constraints.md](../../docs/profile/constraints.md): 변경 금지 대상 표의 "시뮬 방침" 행과 "기준 치수와 max_iter" 행
- [20260807_llr-file-interpretation-rules.md](20260807_llr-file-interpretation-rules.md): max_iter를 파일의 마지막 iter_end가 정하는 규칙
