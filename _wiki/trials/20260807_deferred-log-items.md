---
summary: 구현하지 않고 미룬 분석 로그 항목 7종과 VNU in/out 전체 덤프의 미구현 사유와 재개 자료 (시도한 것이 아니라 미룬 것)
result: partial
tags: [logging, deferred, cpp-mapping]
date: 2026-08-07
source:
  - _pm/done/20260807_출력폴더_로그기능/20260806_출력폴더_로그기능.md
  - _pm/TODO.md (src 후순위 분석 로그 항목)
adopted_as: decisions/20260806_analysis-log-core-set
---

## 시도 내용

- ㉮ 분석 로그 후보 12종 중 [20260806_analysis-log-core-set.md](../decisions/20260806_analysis-log-core-set.md)가 확정한 핵심 5종 밖의 후순위 7종을 구현하지 않고 TODO에 남겼다. 확정, 추가, 제외 목록은 그 결정 문서에 있다

## 결과

- ㉮ 미구현 사유
  - ㉠ 사용자 확정 "핵심 세트 먼저"
  - ㉡ 속도 비용이 큰 항목 (bit_err_by_col, fail_frame_positions)
  - ㉢ fail_frame_positions는 용량 때문에 실패 프레임 한정이 필요
  - ㉣ fail_frame_seed는 재현 방식 미결정 (numpy Generator 상태 저장 대 seed와 카운터 기록)
- ㉯ VNU in/out 전체 덤프 (원본 `__LOG_VNU_IN_OUT__` 대응): 용량이 커서 범위 제외. 필요해지면 별도 등록
- ㉰ 재개 자료 (C++ 로그 대응과 용도)
  - ㉠ bit_err_by_col: `m_log_bit_err_col`. 위치 편중과 특정 블록 진단
  - ㉡ flip_count_per_iter: C++ 대응 없음 (py 고유). 진동과 정체 감지
  - ㉢ table_row_history: `m_log_LLR_idx`. DAO 매트릭스의 row 전환이 의도대로인지 확인
  - ㉣ min_sum_stats: `m_log_min1_sum`, `m_log_min2_sum`. CN 신뢰도 발달 관찰
  - ㉤ fail_frame_positions: uncor vector 저장 대응. trapping set 패턴 식별
  - ㉥ fail_frame_seed: `uncor_seed_*.txt` 대응. 실패 케이스만 재실행
  - ㉦ channel_stats: C++ 대응 없음. 채널 설정 검증
- ㉱ 구현 제약: 배치 마스킹과 공존해야 한다. 성공 프레임이 배치에서 빠지므로 `idx_active`로 원 프레임 번호를 유지한다. 현재 `_record_iteration`이 압축 전에 `idx_active` 위치에 기록하는 방식이 그 예다
- 교훈:
  - ㉠ 후순위로 미룰 때는 C++ 대응과 용도, 미룬 이유를 표로 남긴다. 그래야 재개 비용이 작다
  - ㉡ 로그는 속도를 깎으므로 항목별 선택이 기본이다

## 대안 선택 (있을 경우)

- ㉮ (없음. 재개 시 위 자료로 항목별 등록)
- 관련 문서
  - ㉠ [20260806_analysis-log-core-set.md](../decisions/20260806_analysis-log-core-set.md)
  - ㉡ [20260930_run-dir-and-output-files.md](../tech/20260930_run-dir-and-output-files.md)
  - ㉢ [20260930_genie-check-and-batch-compress.md](../tech/20260930_genie-check-and-batch-compress.md) (배치 압축과 `idx_active`)
