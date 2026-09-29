---
summary: 분석 로그는 항목별 on/off에 상위 스위치 `log.enabled`를 두고, 핵심 5종을 먼저 구현하며, C++에 없는 표준 지표 3종을 더하고 3종은 뺐다
status: Accepted
tags: [logging, metrics, output]
date: 2026-08-06
commit: 0394b81 (시험장 사본에 포함)
source: _pm/done/20260807_출력폴더_로그기능/20260806_출력폴더_로그기능.md:31-46, 65-74; _pm/DONE.md:157-165; src/run.py:107-114; src/decoder.py:51
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 실행 결과가 서로 덮어쓰고, iteration별 CSW와 bit error 같은 중간 로그가 없었다
  - ㉡ 로그 수집은 iteration 루프 안에서 일어나 속도를 깎는다
  - ㉢ 원본 C++ 로그와 대응하는 후보 12종을 표로 정리했다 (항목, C++ 대응 변수, 용도)
- ㉯ 거부한 대안
  - ㉠ 로그 단순 on/off 하나
  - ㉡ 후보 12종 전부 구현
  - ㉢ fer_confidence(신뢰구간), miscorrection_count(undetected error 분리), injected_err_histogram 추가
- ㉰ 이유
  - ㉠ 필요한 것만 켜야 측정 속도를 지킨다. 항목별 선택이 기본이다
  - ㉡ 핵심 세트 먼저 (사용자 확정 2026-08-06). 후순위는 필요해질 때 재개한다
  - ㉢ C++에 없는 항목은 논문과 스펙 비교에 쓰이는 3개만 더한다. post_fec_ber는 FER와 BER 둘 다 요구되는 비교용, fer_vs_iter는 프레임별 성공 iteration으로 "max_iter를 k로 줄였다면"의 FER를 한 실행에서 산출하며 수집 비용이 거의 0, fer_curve_png는 기존 plot 재사용
  - ㉣ 제외 3종의 이유는 기록에 없다 (사용자 코멘트로 확정)
- ㉱ 결과로 생긴 규칙
  - ㉠ 핵심 5종: csw_per_iter, bit_err_per_iter, bit_err_by_dv, iter_histogram, fail_frame_detail (2026-08-07 구현)
  - ㉡ 추가 3종: post_fec_ber(로그와 무관하게 항상 CSV 열), fer_vs_iter, fer_curve_png
  - ㉢ 후순위 7종(bit_err_by_col, flip_count_per_iter, table_row_history, min_sum_stats, fail_frame_positions, fail_frame_seed, channel_stats)은 TODO에 남긴다
  - ㉣ JSON log 키와 디코더 항목 이름의 대응은 `_LOG_TO_ITEM` (`src/run.py:113-114`), 디코더는 `LOG_ITEMS` 밖 항목을 에러로 막는다 (`src/decoder.py:51`)
  - ㉤ 상위 스위치 `log.enabled` (2026-08-10 추가): false면 items 전부 off. 스키마는 `{enabled, items}` 두 키
- ㉲ 비용
  - ㉠ 로그를 켜면 iteration 루프에서 활성 프레임별 합산 비용이 든다
  - ㉡ 후순위 항목은 배치 마스킹과 공존해야 한다 (프레임 제거 시 원 프레임 번호 유지)

## 하위 링크

- [../trials/20260807_deferred-log-items](../trials/20260807_deferred-log-items.md): 후순위 7종과 VNU 덤프의 미구현 사유와 재개 자료
- [../tech/20260930_run-dir-and-output-files](../tech/20260930_run-dir-and-output-files.md): 로그 CSV 4종의 열 정의와 C++ 대응표
- [20260810_avg-iteration-and-realtime-summary](20260810_avg-iteration-and-realtime-summary.md): 같은 출력 체계의 지표와 summary 기록 시점
