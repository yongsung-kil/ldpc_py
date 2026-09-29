---
summary: 성공 판정은 genie(매 iteration 판정 bit를 정답과 정보 구간에서 bitwise 비교)이고 codeword는 all-zero다. encode, genie 정답 참조, BER 집계 셋은 한 묶음이라 하나를 바꾸면 셋을 함께 바꾼다
status: Accepted
tags: [genie, codeword, decoder]
date: 2026-07-30
commit: 0394b81 (시험장 사본에 포함). 정보 구간 한정 변경은 2bd85c9 (원본 저장소)
source: README.md "확정 결정 기록" 절 (:218-219), src/encoder.py:3-8, src/decoder.py:32-34, 316-327, src/sim.py:76, 144, docs/차이.md:24, 45, docs/profile/constraints.md:20, 23, _pm/done/20260730_review/r2_round2_lv1_analysis/report.md:20, _pm/done/20260813_minsum_dual_clip/20260813_minsum_dual_clip.md:40-41
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 원본은 CRC 검출로 복호를 끝내는데 CRC는 비교 제외 대상이다. 종료 기준이 없으면 max_iter까지 돌아 성능 지표가 달라진다
  - ㉡ 실물 인코더 포팅 비용이 크다. 대칭 채널과 대칭 복호기에서는 all-zero 결과가 일반 codeword와 같다
  - ㉢ 계획 리뷰(2026-07-30)가 "genie 판정"과 "고정 iteration 완주"가 문서 안에서 충돌한다고 지적했고, C++ vanilla와 채점을 genie로 통일하기로 정리됐다
- ㉯ 거부한 대안
  - ㉠ 고정 iteration을 완주한 뒤 판정하는 것
  - ㉡ syndrome 0으로 조기 종료하는 것 (미스검출 가능)
  - ㉢ CRC 자체를 포팅하는 것, 실제 인코더를 포팅하는 것
- ㉰ 이유
  - ㉠ genie는 CRC 조기종료의 이상화라 미스검출이 없다
  - ㉡ all-zero면 인코더 포팅이 필요 없고, 정답 참조가 상수가 되어 판정이 단순하다
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ `encode`(all-zero 반환 임시 함수), 디코더의 정답 참조, sim의 BER 집계 셋을 함께 바꿔야 한다. 하나만 바꾸면 조용히 틀린다. "실물 인코더가 필요하면 이 함수만 채우면 된다"는 옛 서술은 거짓이라 2026-08-09에 정정했다
  - ㉡ 판정은 정보 구간(앞쪽 `N_b - M_b`개 column block)만 본다. column block이 DV 내림차순 배치라는 전제가 붙고 코드 검사는 없다 (docs/profile/constraints.md:20)
  - ㉢ 성공 프레임을 배치에서 빼는 마스킹은 속도 최적화이고 결과는 불변이다
  - ㉣ `_column_order` 재정의로 일부 column만 방문해도 오판정이 없도록 판정비트 배열을 지속 상태로 두고 column 루프 밖에서 집계한다 (2026-08-09)
  - ㉤ 정보 구간만 검사하도록 바뀐 뒤(커밋 2bd85c9, 원본 저장소) 이전 실행과 FER 수치가 달라진 것은 의도된 결과다
  - ㉥ `generate_message`는 K bit를 무작위 생성하지만 결과에 영향이 없다. 다만 배치마다 난수를 소비하므로 배치 크기 재현 조건과 얽힌다
- 날짜: 2026-07-30 (판정 방식, all-zero), 2026-08-09 (판정비트 배열), 2026-08-10과 2026-08-13 사이 (정보 구간 한정)

## 하위 링크

- [../tech/20260930_genie-check-and-batch-compress.md](../tech/20260930_genie-check-and-batch-compress.md): 정보 구간 genie 판정과 배치 압축 목록, 결과 버퍼 의미
- [../assets/20260808_decision-bit-array-count-outside-loop.md](../assets/20260808_decision-bit-array-count-outside-loop.md): 에러 집계를 column 루프 밖에서 하는 판정비트 배열 패턴
- [20260807_single-seed-derived-streams.md](20260807_single-seed-derived-streams.md): `generate_message`의 난수 소비가 얽힌 배치 크기 재현 조건
- [../../docs/profile/constraints.md](../../docs/profile/constraints.md): "all-zero codeword, genie 판정, BER 집계 한 묶음" 행과 "column block은 DV 내림차순 배치 전제" 행
