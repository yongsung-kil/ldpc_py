---
summary: BaseDecoder 자식이 재정의하는 교체 지점 6개의 시그니처, 입력 축, 지킬 경계, 교체 지점에 맞지 않는 변경의 수정 범위
tags: [decoder, replacement-point, override, contract]
sources: [src/decoder.py:40-46, src/decoder.py:136-220, src/decoder.py:303, src/decoder.py:310, src/decoder.py:316-320, src/decoder.py:342, src/decoder.py:350, src/decoder.py:365, src/decoder.py:392, src/decoder.py:400, src/decoder.py:408, src/decoder.py:412, src/decoder.py:433-452, src/run.py:443-445, src/run.py:482, src/run.py:507, src/run.py:624, src/sim.py:72-73, workspace/_template/run.py:24-28, docs/profile/replacement_points.md:9-41, docs/profile/techniques.md:44-64]
last_verified: 2026-09-30
---

## 무엇을 하는가

본체 `src/decoder.py`가 원본 C++ 함수 경계를 따라 메서드 6개를 따로 떼어 두고, 논문 아이디어는 `BaseDecoder` 자식에서 그 메서드만 재정의한다. 본체는 고치지 않고 기준선 `workspace/base_run/`은 재정의 0개다. 정본은 `docs/profile/replacement_points.md`이며 여기서는 표와 경계를 요약한다.

## 어떻게 도는가

- ㉮ 표지와 주입: 각 메서드 docstring 첫 줄 `[교체 지점: C++ 함수 대응]` (`src/decoder.py:40-46, 136-220`). 실험 폴더 `run.py`의 `DECODER_CLASS` 한 곳 (`workspace/_template/run.py:24-28`) → `main(decoder_class=)` → `setup`의 `decoder_class(code, llr_matrix=)` (`src/run.py:443-445`)

| 메서드 (시그니처) | C++ 대응 | 위치 / 호출 (`src/decoder.py`) | 입력 | 출력 (기본 동작) |
|---|---|---|---|---|
| `_is_edge_clear_iter(self, iteration)` | Is_Iter_Type_Edge_Clear | `:137-144` / `:342` | iteration (1부터) | bool. True면 min1, min2, min1_pos, check_sum, edge_sgn 클리어, syndrome 유지 (기본 `is_restart`) |
| `_column_order(self, iteration)` | 메인 루프 스케줄 | `:146-148` / `:365`, Pre `:303` | iteration (Pre 단계는 0) | column block 인덱스 iterable (기본 `range(N_b)`) |
| `_c2v_reconstruct(self, iteration, edge, min1_row, min2_row, min1_pos_row, syndrome_row, check_sum_row, edge_sgn_row)` | C2V_Cal | `:150-157` / `:392` | 그 edge의 CN row block 슬라이스 (활성 프레임 수, z) | 부호 있는 C2V, CN 정렬 roll 전 (mag = min1, 자신이 min1이면 min2. sign = syndrome ⊕ check_sum ⊕ edge_sgn) |
| `_vn_decide(self, sum_t)` | VN_Cal_HD 판정부 | `:159-162` / `:400` | sum_t (활성 프레임 수, z) = ch + Σ C2V | bool 반전 마스크 (기본 `sum_t <= 0`, 동점 반전) |
| `_vnu_quantize(self, raw, vnu_in, th)` | VN_Cal_HD 양자화부 | `:164-187` / `:408` | raw = sum_t - vnu_in, vnu_in (raw==0 부호용), th (활성 프레임 수, th 개수) | 부호 있는 양자화 값, VN 정렬 (캐스케이드 `\|raw\| >= th_k`면 `edge_mag[k]`, 균일이면 `_uniform_saturate`) |
| `_cnu_update(self, edge, edge_clear, new_sgn, new_mag, row_blk, min1, min2, min1_pos, check_sum, edge_sgn)` | CNU_Remove_Old_Sgn, CNU_Update_New_Mag | `:197-220` / `:412`, Pre `:310` | 새 메시지 부호와 크기 (CN 정렬), CN 상태 배열 전체 | None. 제자리 갱신 (remove old 후 insert new, `<=` 비교, 새 min1이면 min2 = RESET) |

- ㉯ 입력 축: 재정의 메서드가 받는 배열은 (활성 프레임 수, z)이고 활성 프레임 수는 성공 프레임이 빠지며 iteration마다 줄어든다 (`src/decoder.py:433-452`). dtype은 min1, min2, new_mag가 float32, check_sum, edge_sgn, new_sgn이 uint8, min1_pos가 int32
- ㉰ 경계 규칙
  - ㉠ `_cnu_update`는 받은 배열을 제자리에서 고친다. 반환값은 쓰이지 않는다 (`src/decoder.py:202-203`)
  - ㉡ `_vnu_quantize`가 비정수 raw를 만들면 `_uniform_saturate` (`src/decoder.py:189-195`)도 함께 재정의하거나 캐스케이드 경로를 쓴다 (등가식은 정수 raw에서만 같다)
  - ㉢ `_column_order`가 일부 column만 방문해도 에러 집계는 유지된다 (`_collect_error_metrics`가 루프 밖, `src/decoder.py:316-320`)
  - ㉣ `_is_edge_clear_iter`는 CN 클리어에만 관여한다. SD restart의 Pre 재실행은 `llr_matrix.is_restart`를 직접 본다 (`src/decoder.py:350`). Pre 단계는 `_column_order(0)`과 `_cnu_update(edge_clear=True)`를 고정 인자로 부른다 (`:303`, `:310`)
  - ㉤ 본체가 디코더 객체에서 읽는 것: 생성자 꼴 `decoder_class(code, llr_matrix=)` (`src/run.py:445`), `max_iter` (`src/sim.py:72`, `src/run.py:482`), `llr_matrix`의 `num_dv`, `dv_from`, `dv_to`, `mode` (`src/sim.py:73`, `src/run.py:507, 624`). `isinstance` 검사는 없다
- ㉱ 맞지 않는 변경과 수정 범위 (`docs/profile/replacement_points.md:33-39`)

| 변경 | 고쳐야 하는 곳 |
|---|---|
| 새 상태 배열 (edge별 이력, 프레임별 카운터) | `_DecodeState` (`src/decoder.py:54-96`), `_init_state` (`:249-292`), `_check_errors`의 압축 목록 (`:441-452`) |
| iteration 구조 (여러 pass, 부분 재복호) | `_run_iteration` 전체 (`src/decoder.py:336-370`) |
| 채널 모델 추가 | `src/channel.py`의 `CHANNELS`, `CHANNEL_MODES`와 `src/run.py`의 채널 검증 |
| LLR 형식 (4-bit, th 개수) | 3-bit 전용 확정. `src/llr_matrix.py:136-142`와 `_channel_seed_levels` (`src/decoder.py:120-134`) |
| 실제 인코딩 | `encode`, genie 정답 참조, BER 집계 셋을 함께 |

## 쓰는 법

- ㉮ 최소 형태: 실험 폴더 `decoder.py`에 `class MyDecoder(BaseDecoder)`를 두고 메서드 하나만 인자 목록 그대로 재정의, `run.py`에서 `from decoder import MyDecoder` 뒤 `DECODER_CLASS = MyDecoder`. 파라미터는 우선 클래스 속성으로 전달한다
- ㉯ 붙일 자리: normalized min-sum과 offset min-sum은 `_c2v_reconstruct`, 스케줄 변경은 `_column_order` (`docs/profile/techniques.md:48-49`). 증분 갱신 상태(`_cnu_update`)에 값 변형을 넣기 전에 등가한 읽기 시점(`_c2v_reconstruct`)이 있는지 먼저 본다
- ㉰ 검증 두 방향: 무효과 파라미터로 base_run과 수치 완전 일치(구현 동등성), 유효 재정의로 BER이 달라짐(주입 반영). 같은 seed와 `frames_per_batch`로 돌린다
- ㉱ 주의: `__init__`에서 `self._vnu_quantize = ...`처럼 인스턴스에 바인딩하면 자식 재정의가 조용히 무시된다. 단계별 함수 7개(`_read_channel_input` 등)는 교체 지점 표지가 없어 재정의 대상이 아니다
- ㉲ 이 사본의 제약: 런처가 `2_LDPC_base/src`를 찾지 못하고 `python -m src.run`은 BaseDecoder 고정이라 자식을 실행할 경로가 없다 (판정요청 대기)

## 관련 문서

- decisions [20260807_replacement-point-cpp-function-boundary.md](../decisions/20260807_replacement-point-cpp-function-boundary.md), [20260810_decoder-class-single-switch-registry-removed.md](../decisions/20260810_decoder-class-single-switch-registry-removed.md), [20260930_variant-decoder-run-path.md](../decisions/20260930_variant-decoder-run-path.md)
- assets [20260808_replacement-point-contract-protection.md](../assets/20260808_replacement-point-contract-protection.md), [20260813_paper-idea-single-override-procedure.md](../assets/20260813_paper-idea-single-override-procedure.md), [20260813_clip-at-reconstruct-not-stored-state.md](../assets/20260813_clip-at-reconstruct-not-stored-state.md)
- tech [20260930_cnu-min1-min2-update.md](20260930_cnu-min1-min2-update.md), [20260930_vnu-quantize-cascade.md](20260930_vnu-quantize-cascade.md), [20260930_decoder-stages-and-state.md](20260930_decoder-stages-and-state.md), [20260930_testbed-copy-vs-original-layout.md](20260930_testbed-copy-vs-original-layout.md)
- profile `../../docs/profile/replacement_points.md`, `../../docs/profile/techniques.md`
