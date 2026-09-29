---
summary: 난수는 numpy Generator를 쓰고, `run.seed` 하나에서 포인트마다 `[seed, 채널 인덱스, int(1e6 * 포인트)]`로 독립 스트림을 파생한다. `frames_per_batch`는 통계 결과가 아니라 같은 seed의 수치 재현 조건이며, 배치 크기 의존은 코드 수리 없이 문서 문언 교정으로 종결했다 (2026-08-09)
status: Accepted
tags: [rng, seed, reproducibility]
date: 2026-08-07
commit: 0394b81 (시험장 사본에 포함)
source: README.md:110-111, 120-121, src/run.py:46-47, 58-59, 586, src/channel.py:16, docs/차이.md:49, _pm/DONE.md 2026-08-07 "가독성 리팩토링 + JSON 개편 2차" ㉯, _pm/tasks/20260808_review/종합보고.md:55-62, 109, _pm/TODO.md:14-15, docs/profile/overview.md:20
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 원본 C++는 XOR25 난수 생성기를 쓴다. 2026-07-29에 numpy Generator로 대체하기로 했다
  - ㉡ JSON 개편 2차(2026-08-07)에서 채널마다 두던 seed를 최상위 `run.seed` 하나로 단일화했다
  - ㉢ 2026-08-09 딥 리뷰가 "같은 seed에서 `frames_per_batch`가 FER를 바꾼다"고 실측으로 지적했다. 원인은 두 겹이다. 배치마다 `generate_message`가 난수를 먼저 소비해 배치 경계가 바뀌면 잡음 난수 위치가 밀리고, `max_frame_errors` 종료 검사가 배치 단위라 종료 프레임 수가 배치 배수로 양자화된다
- ㉯ 거부한 대안
  - ㉠ XOR25를 재현하는 것
  - ㉡ 채널마다 seed를 지정하는 것
  - ㉢ 프레임 단위 난수 파생과 종료 규칙 프레임 단위화로 배치 무관성을 코드로 보장하는 것 (리뷰 권고)
  - ㉣ `generate_message`의 난수 호출을 없애는 것 (실물 인코더가 들어오면 재발한다)
- ㉰ 이유
  - ㉠ 난수는 채널 소관이라 원본 생성기 재현이 불필요하다
  - ㉡ seed 하나에서 파생하면 채널과 포인트마다 독립 스트림이 되고 config가 단순하다. 파생값 `int(1e6 * 포인트)`의 중복은 설정 검증이 미리 막는다
  - ㉢ 두 실행 모두 편향 없는 표본이라 프레임 수가 충분하면 같은 FER로 수렴한다. A/B 비교는 같은 config로 돌리므로 영향이 없다 (사용자 지적 2026-08-09). 통계 결론을 바꾸지 않는 결함은 코드 대신 문언을 고친다
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ on/off 비교와 회귀 비교는 seed와 `frames_per_batch`까지 같아야 수치가 재현된다
  - ㉡ "배치 크기는 결과에 영향 없음"이라는 단언을 문서에 쓰지 않는다. 단언 3곳을 "통계 결과는 프레임 수가 충분하면 같고, 같은 seed의 수치 재현에는 배치 크기까지 같아야 한다"로 고쳤다
  - ㉢ 재현성 결함의 심각도는 "통계 결론을 바꾸는가"로 판정한다. 비트 단위 재현은 계약으로 문서화하면 충분할 수 있다
- 날짜: 2026-07-29 (numpy Generator), 2026-08-07 (seed 하나에서 파생), 2026-08-09 (배치 크기 재판정, 문언 교정)

## 하위 링크

- [../assets/20260808_shared-rng-batch-dependence.md](../assets/20260808_shared-rng-batch-dependence.md): 공유 난수와 배치 단위 종료가 배치 크기 의존을 만드는 antipattern과 점검 항목
- [../tech/20260930_channels-section-and-experiment-loop.md](../tech/20260930_channels-section-and-experiment-loop.md): 채널 x 포인트 루프와 난수 스트림 파생 코드
- [20260730_genie-check-and-all-zero-codeword.md](20260730_genie-check-and-all-zero-codeword.md): `generate_message`와 `encode`가 한 묶음인 사정
- [../../README.md](../../README.md): 설정 스키마 절의 `run.seed`와 `run.frames_per_batch` 설명
