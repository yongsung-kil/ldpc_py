# 시도 (trials) 목록

시도했지만 반영하지 않은 것. 무엇을 해 봤고 왜 접었는지.

문서 7편. 마지막 갱신 2026-09-30 (wiki 스킬 첫 실행).

| 문서 | 요약 | 결과 |
|---|---|---|
| [20260803_three-bit-precision-tuning-trial](20260803_three-bit-precision-tuning-trial.md) | 구 코드(2026-08-03 시점)에서 3-bit 내부 정밀도의 th와 ch 조합을 추정으로 튜닝해 6-bit 기준선과의 갭을 줄이려 했다 | partial |
| [20260806_rejected-unification-and-relaxation](20260806_rejected-unification-and-relaxation.md) | 2026-08-06 딥 리뷰의 처방 셋(genie 동점 규칙 통일, 비단조 th 거부, `_validate` 제약 완화)이 원본 C++와의 관계를 잘못 잡아 기각됐다 | failed |
| [20260807_deferred-log-items](20260807_deferred-log-items.md) | 구현하지 않고 미룬 분석 로그 항목 7종과 VNU in/out 전체 덤프의 미구현 사유와 재개 자료 (시도한 것이 아니라 미룬 것) | partial |
| [20260808_prescriptions-revised-for-side-effects](20260808_prescriptions-revised-for-side-effects.md) | 방향은 맞았지만 그대로 적용하면 다른 것을 깨뜨려 형태나 위치가 바뀐 리뷰 처방 다섯 건과, 처방 채택 전 점검 항목 넷 | partial |
| [20260809_toy-sd-values-source-lost](20260809_toy-sd-values-source-lost.md) | toy 2SD/3SD LLR 파일의 ch와 th 값을 C++ 원본의 하드코딩 기본 테이블에서 가져오려 했으나 초기화식이 소실되어 추정값을 썼다 | failed |
| [20260813_minsum-dual-clip-trial](20260813_minsum-dual-clip-trial.md) | 논문 ieee:9496601의 min1/min2 이중 상한 클리핑을 `_c2v_reconstruct` 하나만 재정의해 붙이고 toy 환경에서 (P,Q) 쌍을 스캔했다 | partial |
| [20260818_matrix-sel-1-hd-probe](20260818_matrix-sel-1-hd-probe.md) | matrix_sel_1 H-matrix와 짝 LLR 파일의 HD(hard decision) 정정 한계를 fixed_error 채널로 탐침했으나 본 측정은 결과표가 비어 있다 | partial |
