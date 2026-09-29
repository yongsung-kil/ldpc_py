# 결정 (decisions) 목록

코드와 프로젝트에 실제 반영된 결정. 왜 그렇게 정했는지가 있는 것만.

문서 25편. 마지막 갱신 2026-09-30 (wiki 스킬 첫 실행).

| 문서 | 요약 | 상태 |
|---|---|---|
| [20260729_scope-relative-comparison-simplified-form](20260729_scope-relative-comparison-simplified-form.md) | Python 시뮬레이터는 후보 기법의 on/off 상대 비교만 맡고, 단순화 형태(쇼트닝, 펑처링, HCU, CRC 조기종료, timing, SRAM, PMU, TV, GT, Dual-Update 제거)는 Python에만 둔다. C++와의 절대 FER 일치는 보장하지 않고 C++ vanilla 파생본도 만들지 않는다 | Accepted |
| [20260730_genie-check-and-all-zero-codeword](20260730_genie-check-and-all-zero-codeword.md) | 성공 판정은 genie(매 iteration 판정 bit를 정답과 정보 구간에서 bitwise 비교)이고 codeword는 all-zero다. encode, genie 정답 참조, BER 집계 셋은 한 묶음이라 하나를 바꾸면 셋을 함께 바꾼다 | Accepted |
| [20260730_input-files-external-supply](20260730_input-files-external-supply.md) | 평가 대상 H-matrix와 LLR 테이블은 저장소 밖에서 공급받아 `Input/`에 넣고 config로 지정한다. 저장소에 든 파일은 toy(예시)이고, toy로 개발한 뒤 실물이 들어오면 교체한다 | Accepted |
| [20260730_sim-policy-max-iter-120-no-numba](20260730_sim-policy-max-iter-120-no-numba.md) | max_iter 120을 기준으로 잡고, 가속은 numpy 프레임 배치 벡터화만 쓰며(numba 미사용), 병렬화는 mpi4py로 코어당 시뮬레이션 1개를 띄운다. mpi_runner는 새 구조 기준으로 재설계 대기 중이다 | Accepted |
| [20260806_analysis-log-core-set](20260806_analysis-log-core-set.md) | 분석 로그는 항목별 on/off에 상위 스위치 `log.enabled`를 두고, 핵심 5종을 먼저 구현하며, C++에 없는 표준 지표 3종을 더하고 3종은 뺐다 | Accepted |
| [20260807_channel-config-list-restored](20260807_channel-config-list-restored.md) | 채널 설정을 `channel.use` 단수 선택에서 리스트로 되돌렸으나 2026-08-13 객체 스키마로 대체됐고, "여러 채널을 같은 경로로" 원칙만 살아남았다 | Superseded-by-20260813_config-slots-and-flags |
| [20260807_config-keymap-fail-fast](20260807_config-keymap-fail-fast.md) | config 검증은 키맵, 필수값, 값 제약 세 층으로 `load_config`에서 한꺼번에 fail-fast하고, `_` 접두 키만 설명용으로 건너뛰며, 디코더 임포트 실패도 에러로 끝낸다 (조용한 대체 없음) | Accepted |
| [20260807_legacy-deleted-not-repaired](20260807_legacy-deleted-not-repaired.md) | legacy 복호 경로와 구 자산은 수리하지 않고 삭제한다 (git 이력으로 복구). plan.md도 삭제하고 결정 기록만 README로 옮겼으며, README 상시 최신 의무는 두지 않는다 | Accepted |
| [20260807_llr-file-interpretation-rules](20260807_llr-file-interpretation-rules.md) | LLR 파일 해석 규칙 다섯 묶음. 파일에 없는 정보(모드는 파일명, max_iter는 마지막 iter_end), 형식 검증은 DAO 규칙 정본, 사람이 만든 파일은 3-bit 전용, dv 미매칭은 에러이고 기준은 H-matrix, floor flag는 보존하지 않는다 | Accepted |
| [20260807_purpose-is-the-name](20260807_purpose-is-the-name.md) | 이름은 수단이 아니라 목적을 말하고, 길어져도 명확한 쪽을 고르며, C++에 대응 개념이 있으면 C++ 용어를 따른다 | Accepted |
| [20260807_replacement-point-cpp-function-boundary](20260807_replacement-point-cpp-function-boundary.md) | 교체 단위는 원본 C++ 함수 경계다. 본체 디코더가 그 경계를 따라 교체용 함수를 떼어 두고, 논문 아이디어는 BaseDecoder를 상속한 자식 클래스에서 그 함수만 재정의한다. `src/` 본체는 고치지 않고, 기준선 `workspace/base_run/`은 재정의 0개다 | Accepted |
| [20260807_single-seed-derived-streams](20260807_single-seed-derived-streams.md) | 난수는 numpy Generator를 쓰고, `run.seed` 하나에서 포인트마다 `[seed, 채널 인덱스, int(1e6 * 포인트)]`로 독립 스트림을 파생한다. `frames_per_batch`는 통계 결과가 아니라 같은 seed의 수치 재현 조건이며, 배치 크기 의존은 코드 수리 없이 문서 문언 교정으로 종결했다 (2026-08-09) | Accepted |
| [20260807_strong-error-two-stage-extraction](20260807_strong-error-two-stage-extraction.md) | strong_error 채널은 에러 위치 E개를 먼저 뽑고 그중 round(E*SER)개를 strong으로 배정하는 2단계 추출이다. 원본의 균일 순열 슬라이스와 통계적으로 등가다 | Accepted |
| [20260808_rewrite-not-patch-positive-rules](20260808_rewrite-not-patch-positive-rules.md) | 수리는 덧대기가 아니라 다시 쓰기, 규칙은 긍정문, 줄표와 가운뎃점 금지. 이력물은 수리 대상에서 뺀다 | Accepted |
| [20260808_uniform-llr-file-then-load](20260808_uniform-llr-file-then-load.md) | 균일 LLR matrix는 파일로 생성해 `output.dir/_generated/`에 저장한 뒤 파일 매트릭스와 같은 로더로 읽는 단일 경로이고, 균일 여부는 파일명이 아니라 th 값 패턴으로 판별한다 | Accepted |
| [20260809_fer-one-no-action-example-data](20260809_fer-one-no-action-example-data.md) | 저장소 예시 LLR 파일로 FER 1.0이 나오는 것은 디코더 결함이 아니라 예시 데이터 특성이라 조치하지 않는다. 반전 가능 조건 `ch <= 7*dv`는 LLR 최적화 제약으로 등록했다 | Accepted |
| [20260809_sd-decoding-decisions](20260809_sd-decoding-decisions.md) | 2SD/3SD 구현의 사용자 확정 네 건. toy 파일로 개발, 균일 생성도 SD 지원, Pre 단계 시딩 magnitude는 3-bit 파일이면 C++ 고정 상수이고 균일 n-bit면 균등 분할, Edge Clear는 전 모드에서 restart iteration만 | Accepted |
| [20260809_uniform-min-level-one](20260809_uniform-min-level-one.md) | 균일 n-bit 양자화의 VNU 출력 레벨은 0을 두지 않고 최소 1인 포화형 `[top..2,1,1]`이다 (크기 = `max(min(\|raw\|, top), 1)`) | Accepted |
| [20260810_avg-iteration-and-realtime-summary](20260810_avg-iteration-and-realtime-summary.md) | avg_decoding_iteration은 실패 프레임을 max_iter로 포함한 전 프레임 평균이고, summary.txt는 측정 시작 전에 만들어 진행 줄을 꼬리에서 제자리 갱신하다 결과 줄로 대체한다 | Accepted |
| [20260810_decoder-class-single-switch-registry-removed](20260810_decoder-class-single-switch-registry-removed.md) | 디코더 선택은 실험 폴더 run.py의 `DECODER_CLASS` 한 곳이 한다 (None이면 BaseDecoder). config의 `decoder.type` 키와 registry(이름에서 클래스 경로로 가는 변환표)를 없앴고, 실험 공간을 `workspace/`(당시 이름 `Ideas/`)로 개명했다 | Accepted |
| [20260813_config-slots-and-flags](20260813_config-slots-and-flags.md) | config는 값 자리를 전부 미리 만들어 두고 플래그(`use_input_llr_matrix`, `use_default_edge_quantization`, `channels.type`)가 필요한 것만 골라 읽는 구조다. 설명 정본은 `workspace/_template/config.json`이고 루트 config.json은 삭제했다 | Accepted |
| [20260813_edge-quantization-bits-max-split](20260813_edge-quantization-bits-max-split.md) | edge 메시지 양자화를 bit 수(`edge_resolution_bits`)와 최대값(`edge_max_value`) 두 축으로 나누고, 기본은 C++ 3-bit 레벨 {7,5,3,1}, th는 레벨값과 같으며, 최대값을 키우면 채널 LLR도 같은 배율로 키운다 | Accepted |
| [20260930_history-docs-personal-path](20260930_history-docs-personal-path.md) | 이력 문서에 남은 개인 계정 절대 경로를 `<루트>`로 치환할지 정한다. 상위 규칙(어느 파일에도 적지 않음)과 이력물 보존 방침이 충돌한다. 권고는 계정 부분만 기계 치환. 사용자 답 없음 | Proposed |
| [20260930_input-source-notation-rule](20260930_input-source-notation-rule.md) | 입력 파일(H-matrix, LLR 테이블)의 공급자와 공급자가 준 실값을 문서에 적지 않는 규칙을 새로 둘지 정한다. 권고는 규칙 신설 없이 프로파일에 "없음(미확인)"으로 적기. 사용자 답 없음 | Proposed |
| [20260930_variant-decoder-run-path](20260930_variant-decoder-run-path.md) | 이 시험장 사본에서 변형 디코더(BaseDecoder 자식)를 실행할 경로를 만들지 정한다. 선택지 셋, 권고는 런처 탐색 조건에 한 줄 추가. 사용자 답 없음 | Proposed |
