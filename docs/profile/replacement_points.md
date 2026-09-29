---
title: 교체 지점
tags: [profile, replacement-points]
---
# 교체 지점 (새 기법을 끼워 넣는 자리)

> onboard 스킬이 채우고 idea-apply 스킬이 쓴다 (최초 2026-09-30). 교체 지점이란 본체가 어떤 단계를 일부러 따로 떼어 두어, 새 버전이 그 부분만 갈아 끼울 수 있게 만든 자리다. 경로는 저장소 루트 기준이다.

## 1. 교체 단위

있음. `src/decoder.py`의 `BaseDecoder`를 상속한 자식 클래스에서 메서드 하나를 재정의한다. 본체는 원본 C++ 함수 경계를 따라 6개 메서드를 따로 떼어 두었고, 각 메서드 docstring 첫 줄에 `[교체 지점: C++ 함수 대응]` 표지가 있다 (`src/decoder.py:40-46, 136-220`). 자식 클래스는 실험 폴더 `run.py`의 `DECODER_CLASS` 한 곳이 `main(decoder_class=)`로 주입하고 (`workspace/_template/run.py:24-28`, `src/run.py:780-786`), 설정 JSON에는 디코더 선택 키가 없다 (`README.md:108-109`). 본체 `src/`는 고치지 않는다 (`README.md:161-162`).

## 2. 교체 지점 표

| 바꿀 수 있는 것 | 교체 단위 | 위치 (파일:줄) | 입력 | 출력 | 상태 |
|---|---|---|---|---|---|
| CN 상태를 클리어할 iteration (restart 정책) | 메서드 `_is_edge_clear_iter(self, iteration)` | `src/decoder.py:137-144` (호출 `:342`) | iteration 번호 (1부터) | bool. True면 min1, min2, min1_pos, check_sum, edge_sgn 클리어 (syndrome 유지) | 있음 |
| column block 처리 순서 (스케줄) | 메서드 `_column_order(self, iteration)` | `src/decoder.py:146-148` (호출 `:365`, SD Pre 단계 `:303`) | iteration 번호 (Pre 단계는 0) | column block 인덱스 iterable. 기본 `range(N_b)` | 있음 |
| CN 상태에서 C2V 메시지 재구성 | 메서드 `_c2v_reconstruct(self, iteration, edge, min1_row, min2_row, min1_pos_row, syndrome_row, check_sum_row, edge_sgn_row)` | `src/decoder.py:150-157` (호출 `:392`) | 그 edge의 CN row block 슬라이스 (활성 프레임 수, z) | 부호 있는 C2V (CN 정렬, roll 전). 기본은 mag = min1 (자신이 min1이면 min2), sign = syndrome ⊕ check_sum ⊕ edge_sgn | 있음 |
| VN 판정 (bit 반전 규칙) | 메서드 `_vn_decide(self, sum_t)` | `src/decoder.py:159-162` (호출 `:400`) | sum_t (활성 프레임 수, z) = ch + Σ C2V | bool 배열, True면 현재 bit 반전. 기본 `sum_t <= 0` (동점 반전) | 있음 |
| VNU 출력 양자화 | 메서드 `_vnu_quantize(self, raw, vnu_in, th)` | `src/decoder.py:164-187` (호출 `:408`) | raw = sum_t − vnu_in, vnu_in (부호 결정용), th (활성 프레임 수, th 개수) 프레임별 임계 | 부호 있는 양자화 값 (VN 정렬). 기본은 캐스케이드 \|raw\| >= th_k → edge_mag[k], 균일 레벨이면 `_uniform_saturate` | 있음 |
| CN 상태 갱신 (min-sum 변형) | 메서드 `_cnu_update(self, edge, edge_clear, new_sgn, new_mag, row_blk, min1, min2, min1_pos, check_sum, edge_sgn)` | `src/decoder.py:197-220` (호출 `:412`, SD Pre 단계 `:310`) | 새 메시지 부호와 크기 (CN 정렬), CN 상태 배열 전체 | None. 받은 배열을 제자리에서 고친다. 기본은 remove old 후 insert new (`<=` 비교, 새 min1이면 min2 = RESET) | 있음 |

지킬 경계 (코드에 적힌 것):
- ㉮ `_cnu_update`는 재정의해도 받은 배열을 제자리에서 고쳐야 한다. 반환값은 쓰이지 않는다 (`src/decoder.py:202-203`)
- ㉯ `_vnu_quantize` 재정의가 비정수 raw를 만들면 `_uniform_saturate`(`src/decoder.py:189-195`)도 함께 재정의하거나 캐스케이드 경로를 쓴다
- ㉰ `_column_order`가 일부 column만 방문해도 에러 집계는 유지된다. `_collect_error_metrics`가 column 루프 밖에서 세기 때문이다 (`src/decoder.py:316-320`)
- ㉱ 자식 클래스 생성자는 `decoder_class(code, llr_matrix=...)` 호출에 맞아야 한다 (`src/run.py:445`). 그 밖에 본체가 디코더 객체에서 읽는 속성은 `max_iter` (`src/sim.py:72`, `src/run.py:482`)와 `llr_matrix`의 `num_dv`, `dv_from`, `dv_to`, `mode` (`src/sim.py:73`, `src/run.py:507, 623-624, 742`)다. `isinstance` 검사는 없어 BaseDecoder 상속은 관례이고 강제는 아니다
- ㉲ 재정의한 메서드의 입력 배열 축은 (활성 프레임 수, z)이고, 활성 프레임 수는 성공 프레임이 빠지며 iteration마다 줄어든다 (`src/decoder.py:433-452`)
- ㉳ `_is_edge_clear_iter`는 CN 상태 클리어(`src/decoder.py:342-349`)에만 관여한다. SD restart의 Pre 재실행 여부(`:350-359`)는 `llr_matrix.is_restart`를 직접 보므로 이 메서드를 재정의해도 바뀌지 않는다. SD Pre 단계는 `_column_order(0)`과 `_cnu_update(edge_clear=True)`를 고정 인자로 부른다 (`:303, :310`)
- ㉴ 상속 경계 규칙의 정본 문서 `새논문적용규칙.md`는 이 저장소 밖(`3_LDPC_ideas/`)에 있다. `src/decoder.py:46`이 적은 `docs/새논문적용규칙.md` 경로는 존재하지 않는다 (미확인 항목)

## 3. 교체 지점에 맞지 않는 변경

- ㉮ 새 상태 배열이 필요한 기법 (예: edge별 이력, 프레임별 카운터): `_DecodeState`(`src/decoder.py:54-96`)와 `_init_state`(`:249-292`), `_check_errors`의 배치 압축 목록(`:441-452`)을 함께 고쳐야 한다. 단계별 함수 7개(`_read_channel_input`, `_init_state`, `_run_iteration`, `_process_column`, `_record_iteration`, `_check_errors`, `_build_result`)는 교체 지점 표지가 없어 재정의 대상이 아니다 (금지 문구는 없다)
- ㉯ iteration 구조 자체를 바꾸는 기법 (iteration 안에서 여러 pass, 부분 재복호): `_run_iteration` 전체를 다시 써야 한다
- ㉰ 채널 모델 추가: `src/channel.py`에 함수를 더하고 `CHANNELS`, `CHANNEL_MODES`(`:138-149`)와 `run.py`의 채널 검증(`:183-247`)을 고친다
- ㉱ LLR 테이블 형식 변경 (4-bit, th 개수 변경): 사용자 확정으로 3-bit만 쓴다 (`docs/차이.md:26`). 필요하면 `src/llr_matrix.py:136-142`와 `_channel_seed_levels`(`src/decoder.py:120-134`)
- ㉲ 실제 인코딩: `encode`(`src/encoder.py:18-21`)와 genie 정답 참조(`src/decoder.py:316-327`), BER 집계(`src/sim.py:76, 144`) 셋을 함께 바꿔야 한다

이때 재사용할 수 있는 부품: 부호 로더 `QCCode`, LLR 로더 `LLRMatrix`, 채널 함수, 측정 루프 `run_fer_point`, 설정 검증 `load_config`, 실행 폴더와 출력 `create_run_dir`와 `report`, 디코더 주입 사슬 `main(decoder_class=)`.

## 4. 새 버전을 붙이는 절차

- 1. 양식 복사: `workspace/_template/`를 새 실험 폴더로 복사한다 (`run.py`, `config.json`, `README.md`). README의 "목적, 바꾼 것, 결과, 결론" 네 절을 채운다 (`workspace/_template/README.md:1-22`). 원래 배치에서는 논문 실험을 `3_LDPC_ideas/` 쪽 양식으로 시작한다 (`workspace/base_run/README.md:23-25`)
- 2. 재정의: 실험 폴더에 `decoder.py`를 만들어 `BaseDecoder` 자식 클래스에서 교체 지점 메서드만 재정의하고, `run.py`의 `DECODER_CLASS`를 그 클래스로 바꾼다 (`workspace/_template/run.py:24-28`). 최소 형태:

   ```python
   # workspace/{실험}/decoder.py
   from src.decoder import BaseDecoder

   class MyDecoder(BaseDecoder):
       def _vn_decide(self, sum_t):
           return sum_t < 0        # 예: 동점을 반전하지 않는 변형
   ```

   ```python
   # workspace/{실험}/run.py
   from decoder import MyDecoder
   DECODER_CLASS = MyDecoder
   ```

   이 사본에서는 자식 디코더를 실행할 경로가 아직 없다. 런처는 `2_LDPC_base/src`를 찾지 못해 종료하고, `python -m src.run`은 BaseDecoder 고정이라 자식을 주입할 수 없다 (`src/run.py:794-795`). 런처 탐색 조건을 고치거나 저장소 루트를 `sys.path`에 넣는 별도 런처를 두는 코드 변경이 필요하며, 어느 쪽으로 할지는 판정요청 `_pm/tasks/20260930_explore_프로젝트전체/판정요청_시험장사본_260930.md` 물음 1에 올려 두었다 (2026-09-30)
- 3. 기준 실험과 비교: 같은 `config.json`(같은 seed, `frames_per_batch`)으로 `workspace/base_run/`(off)과 새 실험(on)을 돌리고, 두 실행 폴더의 `fer_{label}.csv`와 `summary.txt` 결과 줄을 비교한다. 재정의 0개면 base_run과 수치가 완전히 같아야 한다 (`workspace/base_run/README.md:5-9`, `README.md:120-121`). 결과와 결론은 실험 폴더 README 표에 적는다
