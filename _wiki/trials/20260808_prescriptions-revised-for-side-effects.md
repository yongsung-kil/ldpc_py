---
summary: 방향은 맞았지만 그대로 적용하면 다른 것을 깨뜨려 형태나 위치가 바뀐 리뷰 처방 다섯 건과, 처방 채택 전 점검 항목 넷
result: partial
tags: [review, prescription, side-effect]
date: 2026-08-08
source:
  - _pm/tasks/20260808_review/r3_round3_lv2_verification/report.md
  - _pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md
  - _pm/done/20260806_review/r3_round3_lv2_verification/team_a_verification.md
adopted_as: assets/20260808_deep-review-operating-rules
---

## 시도 내용

- ㉮ permuted를 공유 함수 안에 (2026-08-06 F1 원안): `_rand_positions`가 뽑은 위치를 행별 셔플(`rng.permuted`)해 구간 슬라이스 편향을 없애자
- ㉯ 에러 집계를 column 루프 뒤 전 column 재계산으로 (C1-F1 나): `_column_order` 재정의로 일부 column만 방문할 때의 성공 오판정을 막자
- ㉰ 균일 레벨 [top..1] 원문 (P1): 원본에 없는 크기 0 레벨을 없애자
- ㉱ generate_message 호출 제거 (B-1 P1): 배치마다 버려지는 난수 소비를 없애 배치 크기 의존을 줄이자
- ㉲ signbit 부호 판정(P2)과 O(1) 등가식(P3) 동시 적용: -0.0 부호 소실을 막고 균일 양자화를 상수 시간으로 만들자

## 결과

- ㉮ permuted 공유: 셔플이 rng 상태를 소비해 같은 함수를 쓰는 fixed_error의 배치 1 이후 비트 재현성이 깨진다. strong_error 안에서만 적용하는 2단계 추출로 변경
- ㉯ 루프 뒤 재계산: 본체 수치(avg_iter, BER)가 바뀌고 비용 +7.8%, 미방문 column에 판정을 새로 만들어 스케줄 아이디어의 실제 동작을 감춘다. 판정비트 배열 지속과 루프 밖 집계로 변경 (본체 수치 보존, 오판정 0)
- ㉰ [top..1]: 로더 제약(레벨 수 = th 수 + 1)에 걸려 즉시 ValueError. 포화형 [top..2,1,1]로 변경
- ㉱ generate_message 제거: strong_error의 소비자 둘 섞임은 미해결이고 실물 인코더가 들어오면 재발. 프레임 단위 파생을 권고했으나 최종은 코드 수리 없이 문언 교정 (사용자 지적: 통계 결론이 바뀌지 않는다)
- ㉲ P2와 P3 동시 적용: raw==0에서 두 처방이 조용히 갈린다. P1(레벨 최소 1) 채택으로 -0.0 문제가 원천 소멸해 P2 불필요, P3는 `sgn * max(min(|raw|, top), 1)` 형태로 확정
- 교훈 (처방을 "유효"로 올리기 전 점검 넷):
  - ㉠ 같은 함수를 쓰는 다른 소비자가 있는가 (난수 상태, 공유 헬퍼)
  - ㉡ 로더와 파일 포맷 제약에 걸리는가
  - ㉢ 본체 수치를 보존하는가 (회계 수리가 디코더 동작을 바꾸면 안 된다)
  - ㉣ 다른 처방과 상호작용하는가. 각각 유효해도 함께 넣으면 갈릴 수 있으니 결정 순서를 정한다

## 대안 선택 (있을 경우)

- ㉮ 다섯 건 모두 방향은 유지하고 형태나 위치를 바꿔 채택했다. 위 "결과"의 변경 내용이 최종 형태다
- 관련 문서
  - ㉠ [20260808_deep-review-operating-rules.md](../assets/20260808_deep-review-operating-rules.md)
  - ㉡ [20260806_set-uniform-vs-order-uniform.md](../assets/20260806_set-uniform-vs-order-uniform.md)
  - ㉢ [20260808_decision-bit-array-count-outside-loop.md](../assets/20260808_decision-bit-array-count-outside-loop.md)
  - ㉣ [20260809_uniform-min-level-one.md](../decisions/20260809_uniform-min-level-one.md)
  - ㉤ [20260807_single-seed-derived-streams.md](../decisions/20260807_single-seed-derived-streams.md)
