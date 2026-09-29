# 검증 B 보고: 누락 탐색 (중요한데 빠진 것, 폴더와 파일 목록 대조)

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장. 경로는 저장소 루트 기준 상대 경로로 바꿨다). 검증 대상은 `explore/r1_perspectives/취합.md` ("취합 :N"은 그 파일의 줄).

## 확인한 것

### 1. 저장소 파일 전체 대조

실제 파일 142개 (`.git/` 제외). 루트 4, `src/` 8 + `__pycache__` 8, `Input/` 7, `docs/` 8, `workspace/` 22, `_pm/` 2 + `done/` 42 + `tasks/` 41. 취합이 언급하지 않은 것:

- ㉮ 빠짐: 루트 `CLAUDE.md` (온보딩 양식, 자리표시자 그대로였음). "CLAUDE.md도 빈 양식"이라고 적어야 한다.
- ㉯ 빠짐: `docs/profile/README.md` (양식 규칙)와 `docs/adr/README.md` (ADR 양식). 프로파일 작성 규칙 자체가 여기 있다.
- ㉰ 미확인: `docs/explore/`에 파일이 하나도 없다. 탐색 산출물은 `_pm/tasks/20260930_explore_프로젝트전체/explore/r1_perspectives/`에 있다.
- ㉱ 빠짐: `_pm/tasks/20260930_explore_프로젝트전체/`에 메인 태스크 문서(`{작업명}.md`)가 없다. `_pm/tasks/_template/README.md`도 없다 (전역 pm 규칙이 "삭제 금지"로 요구). `_pm/tasks/20260808_review/` 36개 파일은 미완 항목이다 (TODO.md:12-13).
- ㉲ 빠짐: `_pm/TODO.md:6`이 `docs/plan.md` §4를 참조하지만 파일이 없다 (TODO.md:27에 "plan.md 삭제" 기록). "문서와 코드가 어긋난 곳"에 추가할 항목.
- ㉳ 빠짐: README.md:5의 `_test/20260806_setup_구성_실험/` 폴더 없음. 경미.
- ㉴ `workspace/matrix_sel_1_HD/_probe/` 내용:
  - ㉠ `260818_225547_probe/`: E=380, 128프레임 0 에러, avg_iter 20.19, 13.2초, 9.7 f/s, 196 it/s (summary.txt:17, fer_fixed_error.csv:2).
  - ㉡ `260818_225612_probe_sweep/`: E=500이 512/512 실패 FER 1.00, 4분 38초에서 끊기고 남은 4포인트와 CSV가 없다. 중단된 실행으로 추정.
  - ㉢ 두 summary 모두 `code commit: ecec8ae+dirty`. 원본 저장소의 커밋 해시다.
  - ㉣ summary.txt:6-8: `matrix_sel_1.txt`는 base 15x145, z=256, N=37120, K=33280, rate=0.8966, E(base)=777, col degree {2:14, 3:69, 4:20, 11:42}, row degree {51:3, 52:12}, max iteration 120.
  - ㉤ `_probe.json` `_desc:4` "포인트당 프레임 에러 20개"인데 값은 max_frame_errors 5, max_frames 1024, frames_per_batch 512.
  - ㉥ `matrix_sel_1_HD_fixed/config.json` `_desc:4`도 "20개"라 적었지만 max_frame_errors 15 (:22). `matrix_sel_1_HD/config.json`은 20 / 200000 / 64 / 640.
- ㉵ `Input/` 파일 내용:
  - ㉠ `LLR_MATRIX_HD_0.txt`: dv 4구간 [11,4,3,2], 그룹 3개 (row 1개씩, 전부 CSW 타입), restart iter 2, max_iter 5.
  - ㉡ `LLR_MATRIX_HD_1.txt`: 그룹 2개 (1 row씩, CSW 타입), restart 없음, max_iter 20. dv=2의 ch=28 (TODO.md:31 위반값, HD_0도 같음).
  - ㉢ `LLR_MATRIX_2SD_toy0.txt`: num_param 5, dv 1..11 단일 구간, 그룹 3개 ITER, restart iter 11, max_iter 20. `3SD_toy0`: num_param 7, 같은 구조.
  - ㉣ `LLR_MATRIX_HD_matrix_sel_1.txt`: 그룹 8개 (rows [1,5,5,7,6,10,10,13] = 57 row), 전부 CSW 타입, restart 없음, iter 구간 1-1, 2-4, 5-20, 21-40, 41-60, 61-80, 81-100, 101-120, max_iter 120. 저장소에서 유일하게 multi-row CSW 그룹(`needs_csw` True)이라 CSW 적응 row 선택이 실제로 동작하는 파일.
  - ㉤ `example_18x147_z256.qc`: 행렬 1벌 (취합 :212 미확인 해소). `matrix_sel_1.txt`: 탭 구분.

### 2. `src/` 공개 심볼과 "모듈과 import 방향" 표 대조

- 맞음: 표의 모든 줄 번호가 코드와 일치. 8모듈 합계 2,208줄.
- 틀림 (경미): "나머지 다섯은 numpy만 import". `llr_matrix.py`는 os, re, warnings도 import (:39-43).
- 빠짐 `pcm.py`: 속성 `N`, `M`, `K`, `rate`, `E`, `M_b`, `N_b`, `z` (:31-36, :43). 생성자 검사 (:26-29). J/K 초과 검사 (:78-81). "column block은 DV 내림차순 배치를 전제" (:18).
- 빠짐 `channel.py`: `qfunc_inv` :24, `dev_from_rber` :37, `_R_OFFSET` :21, `_rand_positions` :71.
- 빠짐 `llr_matrix.py`: `uniform_edge_mag` :51, `GROUP_TYPE_ITER`/`GROUP_TYPE_CSW` :46, `_NAME_RE` :48, `_detect_uniform_edge_mag` :92, `_validate` :172, `is_restart` :359, `_group_of_iter` :362, `has_uniform_levels` :389, `needs_csw` :403, `summary` :408. 속성 `row_values`/`row_ch`/`row_th`/`row_csw`/`row_iter` (:156-161), `group_slices` (:165-169), `restart_iters` (:152), `th_nonmonotonic` (:222), `max_value`/`min_value` (:153-154).
- 빠짐 `sim.py`: `_format_duration` :12, `_rewrite_file_tail` :21, 정수 가드 (:58-65), 결과 dict의 `fps`, `ips`, `summary_line`.
- 빠짐 `run.py` 비공개 함수 14개 (`_check_channel_values` :158 ... `_plot_fer_curves` :692).
- 빠짐 `decoder.py`: `collect_profile` 인자, signed LLR 배열 입력 경로 (:241-244), `assert` (:246).

### 3. `BaseDecoder` 메서드 전체 (19개) 대조

- 맞음: 교체 지점 6개, 단계별 7개, 보조 3개 언급.
- 빠짐: `_channel_seed_levels` :120-134. 균일 n-bit 레벨이면 SD Pre seed magnitude를 `round(1 + (top−1)×(R−1−k)/(R−1))`로 1..top 균등 분할하며 "C++ 대응이 없다"(:124)고 코드가 명시. 저장소 고유 결정.
- 빠짐: `__init__` 검사 두 건 (:105-109)과 파생 속성 (:113-118).
- 빠짐 (경계 규칙): `_run_iteration`은 `_is_edge_clear_iter` (:342)와 별개로 `llr_matrix.is_restart` (:350)를 직접 불러 SD Pre 재실행을 결정. `_column_order(0)`가 Pre 단계에서 호출 (:303).

### 4. config 스키마 키

- 틀림: "허용 키 집합 8개". 실제 9개. `_path_pair` 인라인까지 검사 지점은 10곳.
- 잎 키 전체 36개 (H_matrix 2, decoder 11, channels 5, run 7, output 4, log 8). README JSON은 3개만 빠짐, 산문은 전부 다룸.
- 빠짐: 값 제약 목록. rber 0 < p < 0.5 (:166-170), 에러 bit 수 0 이상 정수 (:172-174), `int(1e6×값)` 중복 금지 (:175-179), type 중복 금지 (:200-201), `channel_llr_*` 길이 = region 수이고 원소 1 이상 (:309-314), `edge_resolution_bits` 2..16 (:258-265), `edge_max_value` 1 이상이고 2^n−1 형태 (:266-267, :331-337), seed 0 이상 (:357), `stop_below_fer` 0 초과 또는 null (:365-370), `csv_prefix`/`label` 문자열 (:350-353), 섹션 값 null 거부 (:283-285).
- 빠짐: 내부 키 `decoder._used_llr_matrix_path` (setup :442가 심고 report :765가 읽음).

### 5. LLR_MATRIX 파일 필드와 QCCode 속성

- 맞음: 헤더 순서, row 구성, 모드 판별, 3-bit 전용, max_iter.
- 빠짐: `max_value`/`min_value`는 디코딩에 쓰이지 않고 저장 왕복에만 (:153-154, :334-335). `floor`는 파싱되지만 `__init__`이 r[0..3]만 읽어 버림 (:156-161). `_validate` 추가 검사: restart 그룹이 마지막이면 에러 (:218-219), ITER 다중 row 그룹 내부 연속성 (:198-210). th 비단조면 `warnings.warn` (:220-226).

### 6. 보유 기법

- 맞음 (없다고 적은 것): `src/` grep 결과 BF, error floor, power stopping, dual update, CRC, HCU, 쇼트닝, 펑처링, numba, mpi, layered, Jump_Iter, 1.5SD 구현 없음.
- 코드에 있는데 취합에 없는 기법: ㉮ CSW 적응 row 선택 규칙 상세 (:369-386), 실제 동작 파일은 HD_matrix_sel_1 하나. ㉯ HD restart row의 −1 의미. ㉰ C2V 재구성식. ㉱ column 직렬 즉시 갱신 스케줄. ㉲ `_channel_seed_levels` 균일 분기. ㉳ th 비단조 경고. ㉴ 지표 정의 (`final_err_bits`는 codeword 전체, `final_info_err_bits`는 정보 구간 :283-289, :324-328; 0 에러 포인트는 그림에서 0.5/frames 상한 마커 run.py:700-704). ㉵ `sum_t`는 무포화 float32 (:407 주석), C2V 최소 크기 1 (llr_matrix.py:52-56). ㉶ region 매핑식 2SD `1−sd`, 3SD `2(1−sd)+(cc⊕sd)` (:236-240), 근거 문서 `_pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md`를 decoder.py:226, :380이 참조.
- "없는 것" 추가 후보: syndrome(CSW==0) 기반 조기 종료 없음; normalized/offset min-sum 없음; 실수 채널 LLR 입력 없음 (HD는 read bit, SD는 region 인덱스만, :233-240); row 기반 layered 없음; 실제 인코더 없음; 자동 테스트 없음.

### 7. 제약 (README 확정 결정, 차이.md 대조)

README.md:215-224 결정 10행 중 빠짐: 2 "단순화 형태는 py 전용, 유효한 기법은 실제 형태의 C++에 적용해 재비교" (:216). 3 제거 항목 중 timing/SRAM/PMU/TV, GT(Graph Thinning) (:217). 7 "max_iter=120 기준" (:221). 8 기준 치수 (:222). 9의 부수 "z_sb=256이면 C++ PMU/Clk 경로 활성화 확인 필요" (:223).

docs/차이.md 1절 빠짐: 4 "테이블 세트 전환은 AUTO(DAO) 경로만 구현" (:20). 6 "iteration 0을 H×r 직접 계산으로 대체, py iteration 번호는 1부터" (:22). 2절 빠짐: 11 수치 표현 (:43, 경미).

제약 후보 추가:
- ㉮ DV 내림차순 column 배치 전제 (pcm.py:18). 코드 검사 없음. genie와 post-FEC BER가 "앞쪽 N_b−M_b 블록 = 정보 구간"으로 보므로 (decoder.py:324-325) 배치가 어긋나면 잘못된 구간을 본다 (추정).
- ㉯ `edge_max_value`를 키우면 `channel_llr_*`도 같은 배율로 (`workspace/_template/config.json:33-34`).
- ㉰ 토이 LLR 파일의 dv=2 ch=28은 반전 가능 조건 ch <= 7×dv=14를 위반한 상태 (`_pm/TODO.md:29-31`).

### 8. 용어 (README 용어 표 9행 밖의 약어)

- ㉮ 그래프 낱말: CN/VN, C2V/V2C, lane, lifting (pcm.py:95), circulant shift, J/K (최대 column degree / 최대 row degree), dc (row degree), z_sb, N_b/M_b/B/E/K/N/M.
- ㉯ 채널 낱말: RBER (원어 풀이 없음), AWGN, BPSK, SNR, Q함수, r_offset, sd/cc 플래그, SER/SCR (원어 없음), XOR25.
- ㉰ 디코더 낱말: sum_t, vnu_in/vnu_out, check_sum, edge_sgn, min1/min2/min1_pos, prev_csw, RESET / V_VERY_STRONG, EDGE / EDGE_MAG, cwc (판정비트, :267), genie, Pre 단계, region, edge_mag, ch / th, ITER/CSW 그룹 타입, restart, floor flag, Edge Clear, uniform.
- ㉱ 지표와 출력: post-FEC BER, e/fr, f/s, it/s, fps/ips, iter_hist, fer_vs_iter, dirty, Sim_Output, `_generated`, `_probe`, label, csv_prefix.
- ㉲ 원본 참조 낱말: Ref-C, RTL/HW/SRAM, AUTO 빌드 / `__AUTO_LLR_OPT__`, HCU, GT, PMU/TV, 4KB.
- ㉳ 이름 충돌: `E`는 edge 수 (pcm.py:43)이면서 에러 bit 수 포인트 (channel.py:92). `th`는 LLR 양자화 임계값이면서 rber 채널의 SD region 임계값 (channel.py:57-61). `K`는 정보 bit 수 (pcm.py:35)이면서 헤더의 최대 row degree (pcm.py:10). `floor`는 row의 floor flag이면서 error floor. "구간"은 dv 구간과 iteration 구간 둘 다.

## 관계와 흐름

빠진 항목들은 "LLR 파일 → row 선택 → 디코더 산술"의 중간 고리와 "실제 운용 파일"에 몰려 있다. 토이 파일은 그룹마다 row가 하나라 CSW 적응 선택이 동작하지 않고, `LLR_MATRIX_HD_matrix_sel_1.txt`와 `matrix_sel_1.txt` 짝만 그 경로를 탄다. `_probe/` 산출물이 그 짝의 치수와 처리량을 유일하게 기록한 자료다. `_is_edge_clear_iter`(교체 가능)와 `llr_matrix.is_restart`(직접 호출)가 restart 판단을 둘로 나눠 갖고 있어 SD restart의 Pre 재실행은 교체 지점 밖에 있다.

## 못 본 것과 추정

- ㉮ `docs/explore/`가 빈 폴더인지는 Glob으로 알 수 없다.
- ㉯ `_pm/done/`, `_pm/tasks/20260808_review/` 본문은 읽지 않았다. DONE.md가 언급하는 `workspace/minsum_dual_clip/`, `workspace/실험로그.md`, `workspace/vanilla/`는 이 사본에 없다.
- ㉰ `_probe_sweep`가 중단된 실행이라는 것은 추정.
- ㉱ DV 내림차순 배치가 어긋나면 genie가 잘못된 구간을 본다는 것은 코드 읽기 추정.
- ㉲ `_channel_seed_levels`는 비균일 넓은 레벨(예: bits 3, max 15 → {15,11,7,3})의 SD 경로에서 `_uniform_levels`가 False라 3-bit 고정 상수 [5,1] / [7,5,3,1]로 떨어진다 (:129-134). 최대 레벨 15와 seed 5의 불균형이 의도인지는 미확인.
- ㉳ 2SD/3SD 경로와 `count_cycles4`, th_len==1 분기는 실행하지 않았다.
