---
summary: 원본 C++ 디코더 대비 Python의 차이 10행 (번호 1~9와 6b)과 등가 확인 14행 (정본 번호는 13까지, 10번이 둘) 요지, 리뷰에서 확정한 원본 C++ 구조 사실 7개
tags: [cpp-original, difference, equivalence, reference]
sources: [docs/차이.md:1-50, src/decoder.py:17-36, src/decoder.py:137-144, src/decoder.py:159-162, src/decoder.py:197-220, src/llr_matrix.py:51-57, src/llr_matrix.py:136-142, src/llr_matrix.py:347-357, docs/profile/techniques.md:44-59, _pm/done/20260730_review/r2_round2_lv1_analysis/report.md:11-22, _pm/done/20260806_review/r3_round3_lv2_verification/report.md:29, _pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md:206-210]
last_verified: 2026-09-30
---

## 무엇을 하는가

정본 `docs/차이.md`(2026-08-06 작성, SD는 2026-08-09 반영)의 요지다. 비교 대상은 원본 C++의 DAO 연동 빌드(`__AUTO_LLR_OPT__`)이고, dual update, 파이프라인 2~3 column store 지연, CRC, HCU, 펑처링, 쇼트닝은 비교 제외다 (`docs/차이.md:8-9`). Python은 on/off 상대 비교 전용이라 절대 FER(frame error rate) 일치는 목표가 아니다.

## 어떻게 도는가

- ㉮ 차이 10행 (번호 1~9와 6b, `docs/차이.md:15-26`)

| # | 항목 | 원본 | Python | 비고 |
|---|---|---|---|---|
| 1 | 디코딩 모드 | HD, 2SD, 3SD, 1.5SD | HD, 2SD, 3SD | 1.5SD와 Jump_Iter 계획 없음 |
| 2 | BF(hard bit flipping) 구간 | 비 AUTO 빌드만 | 미구현 | AUTO 빌드는 비활성이라 차이 없음 |
| 3 | error floor 감지 상태머신 | `Adjust_HD_Floor_Type` | 미구현 | AUTO 그룹 선택에 영향 없음 |
| 4 | 테이블 세트 전환 | 하드코딩 그룹과 파일 경로 둘 | 파일 경로만 | DAO 운용 기준 동일 |
| 5 | power stopping | 채널 LLR을 CH_LLR_MAX로 교체 | 미구현 | 전력 시뮬 기능 |
| 6 | iteration 0 | 메시지 전달로 syndrome 계산 | `H*read_bit` 직접 계산 | 등가. py iteration 1 = 원본 iter 1 |
| 6b | HD iteration 1 edge clear | 함 (Ref-C와 RTL 보정) | 안 함 (`src/decoder.py:137-144`) | 사용자 결정 2026-08-09, 산술 동일 |
| 7 | 성공 판정 | CRC 검출 | genie (정보 구간을 정답과 비교) | CRC 조기종료의 이상화, 2026-07-30 |
| 8 | dv 미매칭 | 조용히 첫 구간 사용 | 에러 (`src/llr_matrix.py:347-357`) | 2026-08-06 |
| 9 | LLR 정밀도 | 3-bit와 4-bit 빌드 | 사람이 만든 파일은 3-bit 전용 (`:136-142`), 균일 생성물만 n-bit | 2026-08-06 |

- ㉯ 등가 확인 14행 (정본 번호는 13까지, 10번이 둘, `docs/차이.md:30-45`): 메시지 도메인(read bit 기준 상대값, `src/decoder.py:17-36`), VN 판정 `sum_t <= 0` 동점 반전 (`:159-162`), C2V sign = syndrome ⊕ check_sum ⊕ edge_sgn, edge clear에서 syndrome 유지, restart row의 -1 값 그대로 산술, CNU 갱신(min1 교체 시 min2 = RESET, `<=` 비교, `:197-220`), VNU 캐스케이드, CSW = Σ(check_sum ⊕ syndrome), 테이블 row 선택, SD Pre 단계, max_iter = 마지막 iter_end, 수치 표현(원본은 V 코드 {3,2,1,0} 저장 후 EDGE 변환, py는 EDGE 값 직접 저장), min1_pos 초기값 -1, 성공 프레임 마스킹(py 전용 속도 최적화, 결과 불변)
- ㉰ 디코더 밖 (`docs/차이.md:49-50`): 난수는 원본 XOR25 대 numpy Generator (2026-07-29), 프레임 배치 벡터화는 구현 형태
- ㉱ 리뷰에서 확정한 원본 C++ 구조 사실 (계획 문서의 오해를 바로잡은 것)
  - ㉠ 디코더는 signed LLR이 아니라 flip/magnitude 도메인. 채널 LLR은 비음수이고 부호 정보는 HD bit와 syndrome에 있다. 채널 코드는 read bit와 region까지만 만들고 LLR 값은 VN 단계 테이블이 준다 (`_pm/done/20260730_review/r2_round2_lv1_analysis/report.md:16`)
  - ㉡ CN 상태는 5필드(min1_pos, min1, min2, check_sum, syndrome). "old/new 2세트"는 없고 edge별 sign 메모리가 따로 있다 (`report.md:15`)
  - ㉢ 파이프라인은 알고리즘 무관이 아니다. V2C store가 C2V보다 지연되어 stage별로 다른 column을 동시에 처리한다 (`report.md:19`). Python은 미재현 (`docs/profile/techniques.md:58`)
  - ㉣ iteration별 LLR 테이블 인덱스 함수 `Get_VNU_Table_Idx`는 `return 0` 스텁이라 하드코딩 경로는 단일 세트. 테이블 전환은 파일 경로만 (`report.md:14`)
  - ㉤ C2V 크기 도메인이 둘이다. min1/min2는 압축 V 도메인(0이 정상 상태), C2V 출력은 EDGE 도메인으로 복원되어 최소 1. C++에 C2V 크기 0은 없다 (`team_a_verification.md:206-210`). Python 균일 레벨의 최소 1이 같은 방향이다 (`src/llr_matrix.py:51-57`)
  - ㉥ 저장소 현 상태로는 AUTO 빌드가 만들어지지 않는다 (헤더 주석 처리와 MSVC 빌드 스크립트, `_pm/done/20260806_review/r3_round3_lv2_verification/report.md:29`). 그래서 등가 확인은 정적 독해로 한다
  - ㉦ 실물 치수는 N_b=147, M_b=18, 정보 129 블록. 계획 문서의 N_b=129는 정보부 오기 (`_pm/done/20260730_review/r2_round2_lv1_analysis/report.md:13`)

## 쓰는 법

- ㉮ 새 차이가 생기면 `docs/차이.md` 표에 먼저 적고 이 문서는 요지만 갱신한다. 코드 docstring에는 C++ 함수 이름과 줄 번호를 괄호에 적는다
- ㉯ 등가 여부를 따질 때 C++ 함수와 Python 메서드의 대응은 교체 지점 문서의 표와 SD 문서의 대응 사슬을 쓴다
- ㉰ 주의: 상대 비교 결과를 C++ 절대값과 대조하는 문구를 문서에 쓰지 않는다. 남은 근사(파이프라인 지연, BF 구간)는 on과 off 양쪽에 똑같이 걸려 상쇄된다
- ㉱ "원본 로더에 검사가 없다"는 "제약이 없다"가 아니다. LLR 파일 검증 규칙의 정본은 DAO 규칙이다

## 관련 문서

- 정본 `../../docs/차이.md`
- decisions [20260729_scope-relative-comparison-simplified-form.md](../decisions/20260729_scope-relative-comparison-simplified-form.md), [20260730_genie-check-and-all-zero-codeword.md](../decisions/20260730_genie-check-and-all-zero-codeword.md), [20260807_llr-file-interpretation-rules.md](../decisions/20260807_llr-file-interpretation-rules.md)
- asset [20260808_zero-level-not-in-original.md](../assets/20260808_zero-level-not-in-original.md)
- tech [20260930_sd-region-and-pre-stage.md](20260930_sd-region-and-pre-stage.md), [20260930_replacement-points-six.md](20260930_replacement-points-six.md), [20260930_cnu-min1-min2-update.md](20260930_cnu-min1-min2-update.md), [20260930_table-row-select-and-restart.md](20260930_table-row-select-and-restart.md)
- profile `../../docs/profile/techniques.md`
