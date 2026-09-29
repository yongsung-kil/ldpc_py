---
summary: Python 시뮬레이터는 후보 기법의 on/off 상대 비교만 맡고, 단순화 형태(쇼트닝, 펑처링, HCU, CRC 조기종료, timing, SRAM, PMU, TV, GT, Dual-Update 제거)는 Python에만 둔다. C++와의 절대 FER 일치는 보장하지 않고 C++ vanilla 파생본도 만들지 않는다
status: Accepted
tags: [scope, comparison, simplification]
date: 2026-07-29
commit: 0394b81 (시험장 사본에 포함)
source: README.md "확정 결정 기록" 절 (:215-217, 220)과 :4, src/__init__.py:3-4, _pm/DONE.md 2026-07-30 항목 "결정 사항", docs/차이.md:8-9, src/channel.py:15, workspace/base_run/README.md:5, docs/profile/constraints.md:15-16, 33
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 원본 C++ 시뮬레이터(Ref-C)를 Python으로 재현하되, 파이프라인 store 지연이나 BF(hard bit flipping) 구간처럼 남는 근사가 있다. 절대값 일치를 목표로 두면 끝이 없다
  - ㉡ 원본에는 하드웨어 모델 부속 기능(timing, SRAM, PMU, TV)이 많다. 논문 아이디어 스크리닝에는 복호 산술만 필요하다
- ㉯ 거부한 대안
  - ㉠ C++ vanilla 파생본을 따로 만들어 Python과 절대 FER를 맞추는 것 (2026-07-30 "만들지 않음")
  - ㉡ Python이 절대 FER를 보고하는 것
  - ㉢ 부속 기능까지 전부 포팅하는 것, Dual-Update를 켠 실제 적용 형태로 시뮬레이션하는 것
- ㉰ 이유
  - ㉠ 상대 비교면 같은 근사가 on과 off 양쪽에 똑같이 걸려 상쇄된다. 최종 검증은 유효한 기법을 실제 형태의 C++에 이식해 재비교하는 것으로 한다
  - ㉡ 복호 산술 밖의 요소는 비교를 흐린다. GT(Graph Thinning)는 edge 라우팅 테이블일 뿐이라 FER 영향 0을 코드로 확인한 뒤 제거했다 (2026-07-30)
  - ㉢ Dual-Update를 끈 형태와 실제 적용 형태의 격차는 최종 C++ 검증에서 흡수한다 (2026-07-30)
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ on/off 비교는 같은 config, seed, `frames_per_batch`로 돌린다
  - ㉡ 절대 수치를 외부 결과와 대조하는 문구를 문서에 쓰지 않는다. 대상 영역은 FER 1e-2 ~ 1e-4
  - ㉢ 비교 제외 목록이 고정된다: dual update, 파이프라인 store 지연, CRC, HCU, 펑처링, 쇼트닝 (docs/차이.md:8-9)
  - ㉣ 채널은 쇼트닝과 펑처링 없음을 전제해 `len_noPS = N`이다 (src/channel.py:15)
  - ㉤ 기준선 실험 `workspace/base_run/`이 곧 "단순화 형태의 원본 대응"이다. 남은 근사(README "남은 근사/제한" 절)를 없애는 작업은 우선순위가 낮다
- 날짜: 2026-07-29 (상대 비교, 단순화 형태, 제거 항목), 2026-07-30 (GT 제거, Dual-Update off, C++ 파생본 없음)

## 하위 링크

- [../tech/20260930_diff-from-cpp-original.md](../tech/20260930_diff-from-cpp-original.md): C++ 원본 대비 차이 10행과 등가 확인 14행. 이 결정이 정한 비교 제외 목록의 상세
- [20260730_sim-policy-max-iter-120-no-numba.md](20260730_sim-policy-max-iter-120-no-numba.md): 같은 시기에 정한 시뮬 방침 (max_iter 120 기준, numba 미사용, 병렬은 mpi4py)
- [../../README.md](../../README.md): "확정 결정 기록" 절과 "남은 근사/제한" 절
- [../../docs/profile/constraints.md](../../docs/profile/constraints.md): 변경 금지 대상 표의 "상대 비교 전용", "단순화 형태는 Python에만", "비교 제외 항목" 행
