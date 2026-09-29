---
title: 제약과 용어
tags: [profile, constraints]
---
# 제약과 용어

> onboard 스킬이 채웠다 (최초 2026-09-30). 모든 스킬이 작업 전에 읽는다. 경로는 저장소 루트 기준이다.

## 1. 변경 금지 대상

README, docs, 코드 주석에서 "바꾸지 말 것", "고정", "전용", "사용자 결정"으로 읽히는 것을 모았다.

| 대상 | 이유 | 위치 |
|---|---|---|
| 상대 비교 전용 | Python은 후보 기법의 on/off 상대 비교(FER 1e-2 ~ 1e-4 영역)를 맡고, C++와의 절대 FER 일치는 보장하지 않는다 (2026-07-29) | `README.md:4, 215`, `src/__init__.py:3-4` |
| 단순화 형태는 Python에만 | 쇼트닝, 펑처링, HCU, CRC 조기종료를 뺀 단순화 형태는 Python 전용. 유효한 기법은 실제 형태의 C++에 적용해 재비교한다 (2026-07-29). timing, SRAM, PMU, TV와 GT(Graph Thinning, FER 영향 0 확인 후)도 제거 | `README.md:216-217` |
| 기준 치수와 max_iter | base 18×147, z=256, codeword 37,632 bit, 정보 33,024 bit. max_iter 120 기준. 전 파라미터는 H-matrix와 LLR 파일에서 읽는다 | `README.md:221-222` |
| iteration 번호는 1부터 | 원본의 iteration 0(신드롬 계산)은 H×r 직접 계산으로 대체했고 py의 iteration 1이 원본의 iter 1에 대응한다 | `docs/차이.md:22`, `src/decoder.py:18-20, 503` |
| 테이블 세트 전환은 DAO 경로만 | 원본 비 AUTO 빌드의 하드코딩 그룹과 FLAG 전환은 미구현. LLR 파일의 그룹 정의만 따른다 | `docs/차이.md:20` |
| column block은 DV 내림차순 배치 전제 | 코드 검사는 없다. genie 판정과 post_fec_ber가 앞쪽 N_b − M_b 블록을 정보 구간으로 보므로 배치가 어긋나면 잘못된 구간을 본다 | `src/pcm.py:18`, `src/decoder.py:324-327`, `README.md:13` |
| `edge_max_value`와 `channel_llr_*`는 같은 배율 | edge 최대 레벨을 키우면 채널 LLR 크기도 같은 배율로 키운다 | `workspace/_template/config.json:33-34` |
| SD Pre 단계 seed 레벨 | 3-bit 파일은 C++ 고정 상수 2SD [5,1], 3SD [7,5,3,1]. 균일 n-bit 레벨은 C++ 대응이 없어 1..top을 region 수로 균등 분할 (저장소 고유 결정). 비균일 넓은 레벨(예: max 15)의 SD 경로는 3-bit 상수로 떨어지는데 의도인지 미확인 | `src/decoder.py:120-134` |
| all-zero codeword, genie 판정, BER 집계 한 묶음 | `encode`는 all-zero 반환 임시 함수이고 genie 정답 참조와 BER 집계가 이를 전제한다. 하나를 바꾸면 셋을 함께 바꾼다 (2026-07-30) | `src/encoder.py:3-8`, `src/decoder.py:32-34`, `README.md:218-219` |
| Ref-C 헤더 형식 전용 | H 파일은 `N_b M_b / J K / z / 빈 줄 / 행렬`만. 구 포맷 지원 제거 (2026-08-06). column block은 DV 내림차순 배치 전제 | `src/pcm.py:7-18`, `README.md:13` |
| DAO LLR_MATRIX 형식만, 모드는 파일명으로 | 파일에 모드가 없어 파일명 `LLR_MATRIX_{HD\|2SD\|3SD}_`로 판별 (2026-08-06). max_iter는 마지막 iter_end. 검증 규칙은 DAO 산출 규칙 기준 (2026-08-07) | `src/llr_matrix.py:11-37`, `README.md:14, 86-88` |
| 3-bit 전용 | 사람이 만든 LLR 파일은 th 3개(레벨 {7,5,3,1})만. 4-bit 확장 계획 없음 (사용자 확정 2026-08-06). 균일 생성물만 n-bit | `src/llr_matrix.py:136-142`, `docs/차이.md:26`, `README.md:201-202` |
| 디코더 선택은 `DECODER_CLASS` 한 곳 | config에 디코더 키가 없다. `python -m src.run` 경로는 BaseDecoder 고정 | `README.md:33, 108-109`, `workspace/_template/run.py:24-28` |
| `src/` 본체 무수정 | 디코더 변형은 BaseDecoder 자식에서 교체 지점 6개만 재정의 | `README.md:161-162`, `src/decoder.py:40-46` |
| `workspace/base_run/`은 재정의 0개 | decoder.py를 두지 않는다. 재정의 0개가 본체와 같다는 보증 | `workspace/base_run/README.md:5-9`, `workspace/README.md:7` |
| `workspace/`는 기준 실험 전용 | 논문 실험은 형제 프로젝트 `3_LDPC_ideas/`에서 | `README.md:159-160`, `workspace/README.md:3-5` |
| 난수 seed 하나 | `run.seed` 하나에서 `[seed, 채널 인덱스, 포인트]`로 파생. XOR25 대신 numpy Generator (2026-07-29) | `README.md:110-111`, `src/run.py:586`, `src/channel.py:16` |
| 입력 파일은 외부 공급 | 평가할 H-matrix와 LLR 테이블은 저장소에 담지 않고 `Input/`에 넣어 config로 지정한다. 저장소의 파일은 예시 | `README.md:205-206, 223` |
| 비교 제외 항목 | dual update, 파이프라인 store 지연, CRC, HCU, 펑처링, 쇼트닝은 비교와 구현 범위 밖 | `docs/차이.md:8-9`, `README.md:216-217, 220` |
| HD iteration 1 edge clear 안 함 | 전 모드에서 restart iteration만 클리어 (사용자 결정 2026-08-09) | `src/decoder.py:137-144`, `docs/차이.md:23` |
| 동점 반전 유지 | `sum_t <= 0` 반전, C++ 원문과 동일 | `src/decoder.py:159-162`, `docs/차이.md:33` |
| dv 미매칭은 에러 | C++의 조용한 col_idx 0 fallback을 재현하지 않는다 (2026-08-06) | `src/llr_matrix.py:31-32, 347-357`, `docs/차이.md:25` |
| 그룹 겹침 금지와 순회 방향 한 쌍 | 겹침 금지를 풀려면 `_group_of_iter` 순회를 C++처럼 역방향으로 함께 바꾼다 | `src/llr_matrix.py:179-182, 362-367` |
| `_cnu_update` 제자리 갱신 | 재정의해도 받은 배열을 제자리에서 고친다. 반환값 미사용 | `src/decoder.py:199-203` |
| `_uniform_saturate` 등가 조건 | 정수 raw에서만 캐스케이드와 등가. 비정수 raw를 만드는 재정의는 함께 재정의 | `src/decoder.py:189-195` |
| 균일 생성 th = 레벨값 | 사용자 결정 2026-08-13 | `src/llr_matrix.py:60-68`, `README.md:224` |
| 균일 판별은 값 기준 | 파일명이 아니라 th 패턴. uniform 파일명인데 패턴이 아니면 에러 | `README.md:106-107`, `src/llr_matrix.py:92-120, 275-279` |
| 채널 모드 전용 | fixed_error는 HD, strong_error는 2SD, rber는 세 모드 | `src/channel.py:78-81, 91-105, 145-149` |
| `_rand_positions` 구간 슬라이스 금지 | 집합만 균일하고 순서는 균일하지 않다 | `src/channel.py:71-75` |
| `qfunc_inv` 계수 유지 | channel.cpp 계수 그대로 | `src/channel.py:24-34` |
| 시뮬 방침 | max_iter 120 기준, numba 미사용 (numpy 배치만), 병렬은 mpi4py로 코어당 sim 1개 (2026-07-30) | `README.md:221` |
| floor flag 왕복 보존 안 함 | 로드 시 버리고 저장 시 −1 기록. 현행 유지 (사용자 확인 2026-08-09) | `src/llr_matrix.py:156-161, 339-340`, `_pm/TODO.md` |
| 이력물 보존 | `_pm/`과 리뷰 기록은 줄표 수리 대상에서 제외 | `_pm/TODO.md:20` |

알려진 위반 상태 (고칠 때 함께 볼 것): 저장소의 토이 LLR 파일(`LLR_MATRIX_HD_0.txt`, `HD_1.txt`)은 dv=2 열의 ch=28이 반전 가능 조건 `ch <= 7*dv`(=14)를 어긴 채 들어 있다. 파라미터 수정 시점에 함께 처리하기로 되어 있다 (`_pm/TODO.md:29-31`).

## 2. 기밀과 표기 규칙

- ㉮ 개인 로컬 절대 경로와 계정 정보를 어느 파일에도 적지 않는다 (상위 폴더 `AI_Assisted_Dev/CLAUDE.md` ㉴). 경로는 저장소 루트 기준 상대 경로로 적는다
- ㉯ 평가 대상 H-matrix와 LLR 테이블 파일은 저장소에 담지 않는다 (`README.md:223`). 입력 파일의 출처와 공급자를 문서와 로그에 적지 않는 명문 규칙은 이 저장소에 없다 (미확인). 출처를 암시하는 문구가 `README.md:223`, `_pm/TODO.md:31, 39`, `_pm/DONE.md`와 `_pm/done/` 리뷰 기록에 남아 있고, 이력 문서 일부에는 개인 계정이 든 절대 경로도 있다. 규칙을 둘지와 이력물을 고칠지는 판정요청 `_pm/tasks/20260930_explore_프로젝트전체/판정요청_시험장사본_260930.md` 물음 2, 3에 올려 두었다 (2026-09-30)
- ㉰ 문장 규칙: 줄표(U+2014)와 가운뎃점(U+00B7)을 쓰지 않는다. 나열은 ㉮㉯㉰와 ㉠㉡, 주소를 받는 갈래는 `- 1.`. 곱셈 기호로 쓰던 가운뎃점은 인라인 코드 안에서 `*`로 적는다 (`_pm/TODO.md:20, 25`)
- ㉱ 사용자 결정은 날짜를 붙여 "사용자 결정 YYYY-MM-DD" 또는 "사용자 확정"으로 코드 docstring과 문서 양쪽에 적는다. 정리 표는 `README.md` "확정 결정 기록" 절
- ㉲ 코드 주석은 원본 C++ 대응 함수 이름과 줄 번호를 괄호에 적는다 (예: `[교체 지점: C2V_Cal 대응]`, `channel.cpp:11-29`)
- ㉳ 언어: 식별자, CSV 헤더, 진행 줄 지표는 영어. docstring, 주석, 예외 문구, 모든 md는 한국어. 디코더 변수명은 C++ 원본 용어 그대로 (`src/decoder.py:3-5`)
- ㉴ 파일명 규칙 (코드가 파싱): LLR 파일 `LLR_MATRIX_{HD|2SD|3SD}_*.txt`, 균일 생성물 `LLR_MATRIX_{mode}_uniform_{bits}bit_max{max}_ch{..}_dv{..}_iter{..}.txt`, 실행 폴더 `YYMMDD_HHMMSS_{label}`, 밑줄 접두 폴더는 보조물 (`_template`, `_probe`, `_generated`)
- ㉵ config JSON에서 `_`로 시작하는 키(`_desc`)는 설명용이고 검사에서 무시된다 (`src/run.py:120-122`)

## 3. 용어 풀이

| 용어 | 원어와 뜻 |
|---|---|
| LDPC | low-density parity-check code (저밀도 패리티 검사 부호) |
| QC | quasi-cyclic (순환 시프트 블록 구조). base matrix의 각 원소가 z×z 순환 시프트 블록 |
| H-matrix | parity-check matrix (패리티 검사 행렬). 파일은 M_b×N_b shift 값 행렬 (−1은 zero block) |
| z | 순환 블록 크기 (lane 수). 기준 256 |
| N_b, M_b | base matrix의 column block 수와 row block 수. N = N_b×z, M = M_b×z, K = N − M |
| J, K (H 파일 헤더 2행) | 최대 column degree와 최대 row degree. 정보 bit 수 K와 이름이 같으니 문맥으로 구분한다 (`src/pcm.py:10, 35`) |
| dc | check node degree (row degree, 검사식 하나에 연결된 변수 수) |
| VN / CN | variable node / check node (변수 노드 / 검사 노드). VNU, CNU는 그 연산부 |
| V2C / C2V | variable-to-check / check-to-variable 메시지 (edge 메시지) |
| edge | base matrix의 −1이 아닌 원소 하나 (row block과 column block의 연결). E는 edge 수. 채널 문맥의 E(에러 bit 수)와 이름이 같으니 문맥으로 구분한다 (`src/pcm.py:43`, `src/channel.py:92`) |
| LLR | log-likelihood ratio (로그 우도비, 비트 신뢰도) |
| LLR_MATRIX, LLR 테이블 | DAO가 만든 iteration/dv/CSW별 파라미터 표. row마다 dv 구간별 ch와 th |
| ch | 채널 LLR 크기 (테이블 값). VN 합에 항상 + 부호로 더해진다 |
| th | VNU 출력 양자화 임계값 (내림차순, 3-bit면 3개). rber 채널 안의 `th`는 SD region 경계값으로 다른 것이다 (`src/channel.py:57-61`) |
| floor flag | LLR row의 마지막 필드. 로드 시 버리고 저장 시 −1로 쓴다. error floor(오류율 바닥 현상)와 다른 낱말이다 |
| uniform | LLR 파일명의 표시. 사람이 만든 파일이 아니라 코드가 균일 레벨로 합성한 파일이라는 뜻 |
| dirty | summary.txt의 `code commit` 줄 접미. 커밋하지 않은 변경이 있는 상태에서 실행했다는 표시 |
| edge_mag | edge 메시지 크기 레벨 (3-bit 기본 {7,5,3,1}). RESET은 최대 레벨 |
| dv | variable node degree (column degree, 변수 노드가 연결된 검사식 수) |
| CSW | check-sum weight (불만족 검사식 수) = Σ(check_sum ⊕ syndrome). 테이블 row 선택의 기준 |
| syndrome | H × read bit (읽은 비트의 패리티 검사 결과). 복호 중 고정 |
| syndrome-aided | 모든 메시지를 초기 read bit 기준 상대값으로 다루는 flip/magnitude 도메인 복호 |
| min-sum | check node 연산을 최솟값으로 근사하는 복호. min1, min2는 최솟값과 두 번째 최솟값 |
| restart, Edge Clear | 지정 iteration에 CN 상태를 클리어하는 동작. LLR 파일의 restart_iter가 정의 |
| 그룹 타입 ITER / CSW | LLR 테이블 그룹의 row 선택 방식. ITER는 iteration 구간, CSW는 직전 CSW 임계 비교 |
| HD / 2SD / 3SD | hard decision / 2-bit, 3-bit soft decision 채널 양자화 (디코딩 모드) |
| region | SD 모드에서 비트별 신뢰도 구간 (2SD 2개, 3SD 4개). ch 열 선택 인덱스 |
| SD Pre 단계 | SD 모드의 iteration 0과 restart에서 채널 magnitude를 CN에 심는 초기화 |
| RBER | raw bit error rate (복호 전 비트 에러율). rber 채널의 포인트 값. 원어 풀이는 코드와 README에 없다 (미확인, 통용 뜻) |
| AWGN, BPSK | additive white Gaussian noise (가우시안 잡음 채널), binary phase-shift keying (비트를 ±1로 보내는 변조). rber 채널이 RBER를 잡음 표준편차로 환산해 쓴다 |
| sd, cc 플래그 | 채널 dict의 SD 정보. sd=1은 strong, cc는 3SD의 very 플래그 (sd=1,cc=1 very strong / 1,0 normal strong / 0,0 normal weak / 0,1 very weak) |
| SER / SCR | strong error ratio / strong correct ratio (strong_error 채널에서 에러와 정정 비트 중 strong 비율) |
| FER / BER | frame error rate / bit error rate. post_fec_ber는 복호 후 정보 비트 에러율 |
| fixed_error | 프레임마다 정확히 E개 비트를 뒤집는 채널. 포인트 값은 E |
| genie | 정답을 아는 이상적 성공 판정 (CRC 조기종료의 이상화) |
| DAO | decoder auto optimizer (LLR 테이블 최적화 외부 도구) |
| Ref-C | 원본 C++ 시뮬레이터 (등가성 비교 기준) |
| BF | hard bit flipping (1-bit precision 복호 구간, 미구현) |
| HCU | 원본의 부가 기능 (단순화 형태에서 제거). 원어는 저장소에 없음 (미확인) |
| 포인트 | 채널 값 하나 (RBER 값 또는 에러 비트 수 E). 포인트마다 FER를 잰다 |
| 배치 (B) | 한 번에 동시 복호하는 프레임 수 (`frames_per_batch`) |

## 4. 실험과 검증 환경

| 환경 | 어디서 | 무엇을 하는지 |
|---|---|---|
| 기준 실험 | `workspace/base_run/` (config.json, run.py, README) | 재정의 없는 BaseDecoder로 기준 FER 커브. 모든 on/off 비교의 off 쪽 |
| 파이프라인 점검 | `workspace/test/` | 전체 파이프라인이 도는지 빠르게 확인 (log 끔, fixed_error [100, 200, 300]). 성능 기록 없음 |
| 특정 H-matrix 실험 | `workspace/matrix_sel_1_HD/`, `matrix_sel_1_HD_fixed/` | `matrix_sel_1.txt`와 `LLR_MATRIX_HD_matrix_sel_1.txt` 조합. `_probe/`에 2026-08-18 결과 2건 |
| 직접 실행 | 저장소 루트에서 `python -m src.run <config.json>` | 폴더 이름과 무관하게 동작. 디코더는 BaseDecoder 고정. 이 사본에서 유일하게 동작하는 경로 (2026-09-30 확인) |
| 회귀 비교 | 같은 config, seed, `frames_per_batch`로 두 실행의 `fer_{label}.csv`와 summary.txt 결과 줄 대조 | 로직 무변경 확인은 수치 완전 일치 (`docs/차이.md:23`, `_pm/TODO.md:21`) |
| 결과 위치 | 각 실험 폴더의 `Sim_Output/YYMMDD_HHMMSS_{label}/` | 이 사본에는 `.gitignore`가 없어 git 무시가 성립하지 않는다 (README.md:170과 어긋남) |
| 단위 테스트 | 없음 | `_pm/DONE.md:71-75`가 말하는 단위 24건 등의 파일은 저장소에 없다 |
