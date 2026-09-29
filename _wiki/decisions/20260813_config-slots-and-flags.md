---
summary: config는 값 자리를 전부 미리 만들어 두고 플래그(`use_input_llr_matrix`, `use_default_edge_quantization`, `channels.type`)가 필요한 것만 골라 읽는 구조다. 설명 정본은 `workspace/_template/config.json`이고 루트 config.json은 삭제했다
status: Accepted
tags: [config, schema, flags]
date: 2026-08-13
commit: 0394b81 (시험장 사본에 포함)
source: _pm/DONE.md 2026-08-13 "edge 양자화 파라미터 분리 + config 스키마 재편" ㉱㉲㉳㉴, 2026-08-10 "루트 config.json 삭제", 2026-08-05 "JSON 설정 기반 4단계 구조", README.md:85-130, workspace/_template/config.json:2-8, 20-27, 84-91, src/run.py:17-80, 406-422
supersedes: 20260807_channel-config-list-restored
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 2026-08-05에 파라미터와 코드를 분리하는 원칙으로 JSON 기반 4단계 흐름(load_config, setup, run_experiment, report)을 만들었다
  - ㉡ 이후 스키마가 바뀔 때마다 config 여러 벌을 고치는 비용과 어긋남이 생겼다 (루트 config, 기준 실험 config, 템플릿)
  - ㉢ 사용자는 값 자리를 재구성하지 않고 스위치만 바꿔 파일 로드 경로와 균일 생성 경로를 오가는 config를 원했다 (2026-08-13)
- ㉯ 거부한 대안
  - ㉠ 경로마다 다른 키 집합을 두는 것 (예: 파일 로드 경로에서 `decoder.max_iter`를 두면 에러)
  - ㉡ channels를 리스트로 두고 항목마다 type과 points를 적는 것 (2026-08-07 리스트 복원 결정)
  - ㉢ 루트 config를 스키마 예시 겸 빠른 실행용으로 유지하는 것
- ㉰ 이유
  - ㉠ 플래그 하나로 두 방식을 오가야 실험 전환이 빠르다
  - ㉡ "이 경로에서는 읽지 않는다"는 소비 구분이 에러 규칙을 대체한다
  - ㉢ 스키마 설명은 README, 실행 표준은 workspace라 루트 config의 역할이 겹쳤다 (2026-08-10)
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ 존재하는 값 공간은 전부 형식 검사하고, 고른 type이 쓰는 공간만 필수다. 소비 여부와 무관하게 형식은 항상 검사한다
  - ㉡ `channels`는 객체다. `type`(문자열 또는 리스트)이 채널을 고르고 `rber`, `fixed_error`, `strong_ratios` 공간이 미리 있다. `fixed_error` 공간은 fixed_error type과 strong_error type이 공용 소비한다 (에러 개수 자리 공유는 사용자 결정)
  - ㉢ 파일 로드 경로에서는 mode와 max_iter를 파일이 정하고 config의 `decoder.mode`, `decoder.max_iter`는 읽지 않는다. 균일 생성 경로에서는 그 둘과 `channel_llr_{mode}`가 필수다
  - ㉣ `use_default_edge_quantization`이 true면 `edge_quantization` 블록을 읽지 않는다. 형식 검사는 그래도 한다
  - ㉤ 실험 폴더 config는 정본 참조 한 줄만 적고, 템플릿은 전 키가 기본값으로 채워져 있어 플래그만 바꾸면 동작한다. JSON에 주석이 없어 설명은 `_desc` 키로 단다
  - ㉥ 새 값 공간이나 플래그를 더하면 키맵과 필수값 규칙도 함께 고친다
- 날짜: 2026-08-05 (4단계 흐름), 2026-08-10 (루트 config 삭제), 2026-08-13 (자리와 플래그 구조, channels 객체화)

## 하위 링크

- [20260807_config-keymap-fail-fast.md](20260807_config-keymap-fail-fast.md): 키맵, 필수값, 값 제약의 fail-fast 검증과 `_` 접두 키 규칙
- [20260807_channel-config-list-restored.md](20260807_channel-config-list-restored.md): 이 결정이 대체한 채널 리스트 스키마. "여러 채널을 같은 경로로" 원칙만 남았다
- [../tech/20260930_config-validation-rules.md](../tech/20260930_config-validation-rules.md): 키맵 9개, 헬퍼 4개, 검사 순서, 정규화 결과
- [20260813_edge-quantization-bits-max-split.md](20260813_edge-quantization-bits-max-split.md): 같은 날 함께 재편한 edge 양자화 키
- [../../README.md](../../README.md): "JSON 설정 스키마" 절
