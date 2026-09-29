# 검증 D 보고: 실용성 (목적에 비춰 취합 문서로 프로파일 다섯 문서를 채울 수 있는가, 더 봐야 할 것은)

> 작성: 2026-09-30 (explorer 에이전트 보고 원문, 메인이 저장). 경로는 저장소 루트 기준. 실행은 하지 않았고 코드 읽기와 grep으로만 판정했다.

## 확인한 것

### 1. 취합 문서 주장의 코드 대조

| 판정 | 항목 | 근거 |
|---|---|---|
| 맞음 | 교체 지점 6개의 위치, 입력, 출력, 호출 위치 | `src/decoder.py:137-148, 150-162, 164-187, 197-220`, 호출 `:303, 310, 342, 365, 392, 400, 408, 412` |
| 맞음 | 경계 규칙 4건 | `src/decoder.py:202-203, 192-194, 316-320`, `src/run.py:445` |
| 맞음 | `main` 호출 순서와 사용법 | `src/run.py:780-791, 783` |
| 맞음 | 성능 지표 이름과 CSV 열 | `src/sim.py:142-148, 174-175` |
| 맞음 | 런처가 `2_LDPC_base/src`를 하드코딩 | 세 파일 직접 대조 동일 |
| 맞음 | 정본 문서 부재와 경로 불일치 | Glob 0건 |
| 맞음 | 테스트 파일 없음 | Glob `**/*.py` 14개 전부 `src/`와 런처 |
| 맞음 | `channel_config.get("label")` 죽은 코드 | `_check_channels`(`src/run.py:224-247`)가 `label` 키를 만들지 않음 |
| 틀림(사소) | "허용 키 집합 8개" | 9개 |
| 틀림(사소) | "`_collect_error_metrics`(:316-320)" | 함수 본체는 `:316-334` |
| 빠짐 | 아래 2절부터 6절까지 | 정의식, 절차, 예시, 용어, 기밀 문구 목록이 취합에 없음 |

### 2. overview.md 채우기 판정

- ㉮ 성능 지표 정의식: `src/sim.py:139` fer = errors/frames. `:144` post_fec_ber = Σ final_info_err_bits / (frames × K), K = N − M (`src/pcm.py:35`), 분자는 information 구간 잔여 에러 (`src/decoder.py:324-327`). `:141, 145` avg_decoding_iteration = (성공 프레임 수렴 iteration 합 + errors × max_iter) / frames. 프레임 에러 = information 구간 decision_bits에 1이 하나라도 (`src/decoder.py:326`). CSV 정밀도 fer와 ber 6e, avg_iter .3f (`src/sim.py:178-182`)
- ㉯ 입력 실물 치수: `example_18x147_z256.qc` (147 18 / 4 31 / 256), `matrix_sel_1.txt` (145 15 / 11 52 / 256, 실행 요약 N=37120, K=33280, rate 0.8966, dv {2:14, 3:69, 4:20, 11:42}, dc {51:3, 52:12}), `LLR_MATRIX_HD_1.txt` (dv 구간 4개, 그룹 2개, restart 0, max_iter 20), `LLR_MATRIX_HD_matrix_sel_1.txt` (그룹 8개 전부 CSW, max_iter 120)
- ㉰ 빌드 "없음", 테스트 "없음"과 대체 관습, 실행 명령은 채울 수 있다

### 3. structure.md 채우기 판정

4절 실행 모드와 분기에 더할 것: restart iteration 유무 (`src/llr_matrix.py:359-360`, `src/decoder.py:342-359`), 그룹 타입 ITER 대 CSW (`src/llr_matrix.py:377-386`), 균일 레벨 등가식 분기 (`src/decoder.py:175-181`)

### 4. replacement_points.md 채우기 판정과 4절 절차

- ㉮ 1절과 2절: 채울 수 있다. "만들어야 함" 후보는 단계별 함수 7개, 채널 추가 (`src/run.py:226-246` 분기가 하드코딩), 인코더
- ㉯ 4절 절차 근거: `README.md:36-37, 157-175`, `workspace/README.md:7-13`, `workspace/_template/run.py:24-28`, `workspace/_template/README.md`, `workspace/base_run/README.md:5-9, 21-25`
- ㉰ **실용상 결정적 문제**: 이 사본에는 자식 디코더를 실행할 경로가 없다. 런처는 `2_LDPC_base` 폴더를 찾지 못해 종료하고 (`workspace/_template/run.py:12-16`), `python -m src.run`은 `main()`을 인자 없이 불러 (`src/run.py:794-795`) `decoder_class` 주입이 불가능하다. 선택지는 ㉠ 런처의 탐색 조건을 `os.path.isfile(os.path.join(_root, "src", "run.py"))`로 바꿔 폴더 이름 의존을 없애는 것, ㉡ 실험 폴더에 저장소 루트를 `sys.path`에 넣는 짧은 런처를 새로 두는 것. 둘 다 코드 변경이라 Decision 등급이다
- ㉱ 최소 재정의 골격 (`src/decoder.py:146-148, 159-162`, `src/run.py:445`):

```python
# workspace/{실험}/decoder.py
from src.decoder import BaseDecoder

class ReverseOrderDecoder(BaseDecoder):
    def _column_order(self, iteration):
        return range(self.code.N_b - 1, -1, -1)
```

- ㉲ 기준 실험과 비교: 비교 스크립트는 없다. 같은 config, seed, `frames_per_batch`로 각각 실행 → 두 `fer_{label}.csv`를 표로 → `summary.txt`의 `decoder` 줄(`src/run.py:483`)과 `code commit` 줄(`:727`)로 식별 → 로직 무변경은 수치 완전 일치

### 5. techniques.md 3절 "없는 것" 판정 (grep과 코드 읽기, `_pm/` 제외)

| 기법 | 판정 | 근거 |
|---|---|---|
| normalized min-sum, offset min-sum | 없음 | `_c2v_reconstruct`가 min1/min2를 그대로 반환, 스케일 인자나 오프셋 없음 (`src/decoder.py:155-157`) |
| layered 대 flooding 스케줄 | 명시 모드 없음. 실제는 column 직렬 | column 하나씩 처리하며 CN 상태 즉시 갱신 (`:365-366, 412-413`). flooding이나 row layered 경로 없음 |
| syndrome check 조기 종료 | 없음 | CSW를 매 iteration 계산하지만 (`:370`) 종료에 쓰지 않고 row 선택에만 (`src/llr_matrix.py:382-386`). 종료는 genie (`src/decoder.py:436-442`) |
| bit flipping 계열 | 독립 디코더 없음 | BF 구간 미구현 (`docs/차이.md:18`). restart row의 ch=-1, th=-1이면 그 iteration이 사실상 syndrome bit-flip (`src/decoder.py:28-29`), 테이블 값이 만드는 부수 동작 |
| adaptive quantization | edge 레벨 적응은 없음. 테이블 적응은 있음 | 레벨은 `edge_mag` 고정 (`:116`). th와 ch는 iteration과 직전 CSW로 row를 골라 바뀜 (`src/llr_matrix.py:369-386`). 1절(있음)과 3절(없음)에 나눠 적어야 한다 |
| trapping set 후처리 | 없음 | grep 0건. error floor 감지 미구현 (`docs/차이.md:19`) |
| dynamic scheduling, informed dynamic scheduling | 없음 | `_column_order`는 `range(N_b)` 고정 (`:148`), residual 계산 없음 |
| 실제 인코딩 | 없음 | `src/encoder.py:18-21` |
| 1.5SD, Jump_Iter, power stopping, HCU, 펑처링, 쇼트닝, dual update, 파이프라인 지연 | 없음 | `docs/차이.md:17-21`, `src/decoder.py:35`, `README.md:216-217` |
| 병렬화 | 없음 | import 0건 |

2절 구현 특화에 더할 것: column 우선 edge 정렬 (`src/pcm.py:39`), argpartition 위치 추출 (`src/channel.py:71-75`).

### 6. constraints.md 채우기 판정

- ㉮ 1절: 취합 표 근거 전부 맞음
- ㉯ 2절 기밀 규칙: 저장소에 명시적 기밀 규칙은 없다. 입력 파일 출처와 성격을 드러내는 문구는 실재한다:
  - 1. `README.md:223` "LLR 값은 원본 소스 손상으로 소실", "z_sb=256이면 C++ 쪽 PMU/Clk 경로가 최초로 활성화"
  - 2. `_pm/TODO.md:31` "벤더 참고값: dv=2 ch=10", `:39` "소실된 HW TH/CH 값"
  - 3. `_pm/DONE.md:369` "소실된 HW TH/CH 실값"
  - 4. `_pm/done/20260806_review/r3_round3_lv2_verification/team_b_verification.md:41, 47, 106`, 같은 폴더 `worker_b_1.md:146-163, 387, 421, 465-466`: 벤더 3-bit 채널 테이블 실값 수록
  - 5. `_pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md:313-321` "소실된 값 (소스 손상)" 절
  - 6. `workspace/matrix_sel_1_HD_fixed/README.md:7` "4_H_matrix_tool에서 선별"
  - 7. 외부 도구와 형제 프로젝트 이름(DAO, Ref-C, 0_LDPC_original 등)은 코드 docstring과 README 전반에 있어, 2절 규칙을 "출처 기재 금지"로 쓰면 코드 주석까지 위반이 된다. 규칙 문구는 결정거리다
- ㉰ 상위 CLAUDE.md ㉴(개인 절대 경로와 계정 정보 금지) 대조: 취합.md에는 0건. `agent_A.md`에 드라이브 문자만. 이력물에는 계정 이름이 든 실경로가 남아 있다: `_pm/done/20260806_review/r3_round3_lv2_verification/team_a_verification.md:190`, `worker_a_3.md:17, 44, 88`, `worker_b_2.md:337`, `worker_c_1.md:9`, `_pm/done/20260806_review/r4_round2_lv1_fix_review/agent_1.md:277`, `_pm/tasks/20260808_review/r3_round3_lv2_verification/worker_a_1.md:332`, `context.md:52`, `worker_c_1.md:144`, `_pm/tasks/20260808_review/r2_round2_lv2_analysis/worker_c_3.md:8, 11, 108, 121`, `worker_c_2.md:279`. "이력물 보존" 방침(`_pm/TODO.md:20`)과 충돌하므로 결정거리다
- ㉱ 3절 용어: `README.md:43-55` 표에 더할 것: Ref-C, genie, restart와 edge clear, region, RESET, min1/min2/min1_pos, ch와 th, E와 SER/SCR, z lane
- ㉲ 4절 실험과 검증 환경: base_run 설정 (`workspace/base_run/config.json:7-49`), test, matrix_sel_1_HD 두 폴더 (`_probe/` 결과 2건 커밋됨, E=380 128프레임 fer 0), 직접 실행 경로, 회귀 기준, git 무시 의도만 있음

## 관계와 흐름

새 논문 기법을 붙이는 작업자의 동선:
- 1. 무엇을 바꿀지 고르기: 교체 지점 표로 충분. shape와 정렬(CN 대 VN, roll 방향)은 `src/decoder.py:372-413`을 직접 읽어야 한다
- 2. 재정의 쓰기: 골격과 `workspace/_template/run.py:24-28` 주석으로 충분. 정본이 없으므로 프로파일 replacement_points.md가 사실상 정본이 된다
- 3. 실행하기: **여기서 막힌다.** 런처는 폴더 이름 때문에 종료하고, `python -m src.run`은 자식 클래스를 받지 못한다
- 4. 비교하기: 같은 config로 각각 돌려 `fer_{label}.csv`를 손으로 대조

## 못 본 것과 추정

- ㉮ 실행 검증을 하지 않았다
- ㉯ 런처 5개 중 3개만 직접 대조
- ㉰ "없는 기법" grep은 `_pm/` 제외
- ㉱ 재정의한 `_column_order`가 iteration 0에서도 불린다는 점은 경계 규칙에 추가할 가치가 있다
- ㉲ 저장소 밖 정본은 볼 수 없어 원문과의 어긋남은 판단하지 못했다
- ㉳ 상위 CLAUDE.md ㉰(회사 이름 등 금지)은 `plugin/` 한정 규칙으로 읽었다
