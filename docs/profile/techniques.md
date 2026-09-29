---
title: 보유 기법
tags: [profile, techniques]
---
# 이미 가진 기법

> onboard 스킬이 채우고 paper-screen 스킬이 "이미 있음" 판정에 쓴다 (최초 2026-09-30). 경로는 저장소 루트 기준이다.

## 1. 핵심 기법

| 기법 | 무엇을 하는지 | 어디에 (파일:줄) | 선택 사항인지 |
|---|---|---|---|
| syndrome-aided flip 도메인 min-sum | read bit를 고정하고 syndrome을 1회 계산해 유지하며, 모든 메시지를 read bit 기준 상대값으로 다룬다. C2V 부호 = syndrome ⊕ check_sum ⊕ edge_sgn | `src/decoder.py:17-31, 150-157` | 아니오 (디코더 기본 구조) |
| 두 최솟값 CN 상태 (min1, min2, min1_pos) | CN마다 최솟값 둘과 위치만 유지. min1 교체 시 기존 min1을 min2로 내리지 않고 RESET (HW 특성 재현), `<=` 비교 | `src/decoder.py:197-220` | 아니오 |
| column 직렬 스케줄과 즉시 CN 갱신 | column block 하나를 처리한 뒤 바로 CN 상태를 갱신해 뒤 column이 갱신값을 본다. flooding(전 노드 동시 갱신)이나 row 단위 layered 경로는 없다 | `src/decoder.py:365-366, 405-413` | 순서는 `_column_order`로 교체 가능 (기본 `range(N_b)` 고정) |
| 테이블 기반 iteration/CSW 적응 파라미터 | iteration이 속한 그룹과 직전 CSW(check-sum weight, 불만족 검사식 수)로 row를 골라 채널 LLR(ch)과 양자화 임계(th)를 프레임별로 바꾼다. 양자화 레벨(edge_mag) 자체는 고정이다 | `src/llr_matrix.py:362-386`, `src/decoder.py:360-363, 116` | 아니오 (LLR 파일이 정의) |
| edge 양자화 (3-bit 기본, n-bit 균일 확장) | VNU 출력을 th 캐스케이드로 레벨 {7,5,3,1}에 양자화. 균일 레벨이면 등가식 max(min(\|raw\|, top), 1) | `src/decoder.py:164-195`, `src/llr_matrix.py:60-120` | 레벨은 설정 가능 (`edge_resolution_bits`, `edge_max_value`) |
| restart (Edge Clear) | 지정 iteration에 CN 상태를 클리어하고 (syndrome 유지) restart row의 −1 값을 그대로 써서 순수 syndrome bit-flip iteration이 된다 | `src/decoder.py:137-144, 342-349`, `src/llr_matrix.py:25-28` | LLR 파일의 restart_iter가 정의 |
| 동점 반전 | sum_t == 0이면 반전 (C++ 원문과 동일) | `src/decoder.py:159-162` | `_vn_decide`로 교체 가능 |
| SD Pre 단계 (2SD, 3SD) | 채널 신뢰도 region별 magnitude를 CN에 심는 초기화. 3-bit 파일은 C++ 고정 상수 2SD [5,1], 3SD [7,5,3,1], 균일 n-bit 레벨은 1..top 균등 분할 (C++ 대응 없음). SD restart도 Pre를 재실행하고 판정을 read bit로 되돌린다 | `src/decoder.py:120-134, 294-314, 350-359` | 모드가 SD일 때 |
| region 매핑 | 채널 sd, cc 플래그를 ch 열 인덱스로. 2SD `1−sd`, 3SD `2(1−sd)+(cc⊕sd)` (0이 가장 강함) | `src/decoder.py:223-247` | 모드가 SD일 때 |
| 무포화 합산 | sum_t는 float32로 포화 없이 누적하고 양자화는 VNU 출력에서만 | `src/decoder.py:382-398, 407` | 아니오 |
| genie 성공 판정 | 매 iteration 판정 bit를 정답(all-zero)과 정보 구간에서 비교해 일치하면 성공 확정. CRC 조기종료의 이상화 (미스검출 없음) | `src/decoder.py:316-334, 433-452` | 아니오 (사용자 결정 2026-07-30) |
| 채널 모델 3종 | rber (RBER를 역 Q함수로 σ 환산, BPSK+가우시안, HD/2SD/3SD 양자화), fixed_error (프레임당 정확히 E개 flip), strong_error (SER, SCR 비율로 strong/weak 배치) | `src/channel.py:43-135` | `channels.type`으로 선택 |
| 균일 LLR 매트릭스 합성 | 파일 없이 균일 간격 레벨과 전 dv 공통 ch로 그룹 1개 매트릭스를 만들어 DAO 포맷으로 저장 후 같은 로더로 읽는다 | `src/llr_matrix.py:60-89, 285-344`, `src/run.py:412-441` | `use_input_llr_matrix=false` |
| fer_vs_iter 산출 | 프레임별 성공 iteration 기록으로 "max_iter를 k로 줄였다면"의 FER를 한 번의 실행에서 계산 | `src/sim.py:77, 103`, `src/run.py:656-677` | `log.items.fer_vs_iter` |

## 2. 구현 특화 (성능이나 자원을 위한 구조)

| 기법 | 목적 | 어디에 |
|---|---|---|
| 프레임 배치 벡터화 | 프레임 B개와 lane z개를 numpy 축으로 동시 처리. 배열 축은 (B, N_b, z) | `src/decoder.py:38`, `docs/차이.md:50` |
| QC 연결을 `np.roll`로 처리 | edge shift s에 대해 VN 정렬 ↔ CN 정렬 변환을 roll(∓s)로 | `src/pcm.py:4-5`, `src/decoder.py:396, 409` |
| 성공 프레임 마스킹 (배치 압축) | 성공 확정 프레임을 상태 배열에서 제외해 뒤 iteration 비용을 줄인다. 결과 불변 | `src/decoder.py:441-452`, `docs/차이.md:45` |
| column 우선 edge 정렬 | edge 배열을 column 우선으로 정렬해 column 루프에서 연속 접근 | `src/pcm.py:39-44` |
| argpartition 위치 추출 | 프레임별 정확히 E개 에러 위치를 정렬 없이 고른다 (집합만 균일, 구간 슬라이스 금지) | `src/channel.py:71-75` |
| 균일 레벨 등가식 | th 개수만큼 돌던 캐스케이드를 상수 시간 `_uniform_saturate`로 (정수 raw에서만 등가) | `src/decoder.py:189-195` |
| 에러 집계를 column 루프 밖에서 | 부분 스케줄 재정의에도 집계 유지 | `src/decoder.py:316-334` |
| 로그 항목 선택 수집 | 켠 항목만 iteration별로 집계해 속도 비용 한정 | `src/decoder.py:415-431`, `src/run.py:113-114` |
| 난수 스트림 파생 | 포인트마다 `[seed, 채널 인덱스, int(1e6 × 포인트)]`로 독립 스트림 | `src/run.py:586` |
| summary.txt 제자리 갱신 | 진행 줄을 파일 꼬리에서 제자리 갱신하다 결과 줄로 대체 (실시간 기록) | `src/sim.py:21-26, 134-135, 164-166` |
| 커밋 해시 기록 | 실행 폴더 summary.txt에 `git rev-parse --short HEAD`와 `+dirty` | `src/run.py:603-618` |

## 3. 없는 것 (자주 묻는 기법 중 이 프로젝트에 없는 것)

| 기법 | 비고 |
|---|---|
| normalized min-sum, offset min-sum | `_c2v_reconstruct`가 min1, min2를 그대로 반환하고 스케일 인자나 오프셋이 없다 (`src/decoder.py:155-157`). 붙이려면 교체 지점 `_c2v_reconstruct` |
| flooding 스케줄, row 단위 layered, dynamic scheduling (residual 기반 순서 결정) | `_column_order`가 `range(N_b)` 고정이고 residual 계산이 없다 (`src/decoder.py:148`). 순서 변경은 교체 지점 `_column_order` |
| syndrome check 조기 종료 | CSW를 매 iteration 계산하지만 (`src/decoder.py:370`) 테이블 row 선택에만 쓰고 종료에는 쓰지 않는다. 종료는 genie (`:436-442`) |
| 양자화 레벨 적응 (adaptive quantization) | edge 레벨은 `edge_mag`로 고정 (`src/decoder.py:116`). iteration/CSW에 따라 바뀌는 것은 th와 ch 테이블 값이다 (1절 참조) |
| 독립 bit flipping 디코더 | BF 구간 미구현 (`docs/차이.md:18`). restart row의 ch=−1, th=−1이 그 iteration을 사실상 syndrome bit-flip으로 만들지만 (`src/decoder.py:28-29`) 테이블 값이 만드는 부수 동작이다 |
| trapping set 후처리, error floor 감지 | 없음. 원본 `Adjust_HD_Floor_Type` 상태머신 미구현 (`docs/차이.md:19`) |
| BF (hard bit flipping) 구간 | 원본 비 AUTO 빌드의 1-bit precision 구간. DAO 빌드는 비활성이라 미구현 (`docs/차이.md:18`) |
| power stopping | 전력 절감용 채널 LLR 교체. 미구현 (`docs/차이.md:21`) |
| 1.5SD 모드, Jump_Iter | 계획 없음 (`docs/차이.md:17`) |
| dual update | off (단순화 취지, 사용자 결정 2026-07-30, `README.md:220`) |
| 파이프라인 store 지연 (2~3 column) | 미재현 (`README.md:203`) |
| CRC 조기종료, HCU, 쇼트닝, 펑처링 | 단순화 형태에서 제거 (`README.md:216-217`, `src/channel.py:15`) |
| 실수(연속값) 채널 LLR 입력 | 디코더 입력은 HD read bit와 SD region 인덱스뿐이다 (`src/decoder.py:233-240`). 채널 LLR 크기는 테이블 ch 값이 정한다 |
| 실제 인코더 | `encode`는 all-zero 반환 임시 함수 (`src/encoder.py:18-21`) |
| 병렬 실행 (mpi4py, numba, multiprocessing) | import 0건. mpi_runner는 재설계 예정 (`README.md:221`, `_pm/TODO.md`) |
| 단위 테스트 | `tests/` 없음 |
| 후순위 분석 로그 7종 | bit_err_by_col, flip_count_per_iter, table_row_history, min_sum_stats, fail_frame_positions, fail_frame_seed, channel_stats (`_pm/TODO.md`) |
