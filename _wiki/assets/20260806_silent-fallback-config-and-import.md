---
summary: 설정 키 오타, 블록 이름 오타, 디코더 임포트 실패가 에러 없이 기본값이나 다른 디코더로 완주하는 조용한 대체 경로
type: antipattern
tags: [config, fallback, import, validation]
date: 2026-08-06
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260806_review/r3_round3_lv2_verification/team_a_verification.md`, `_pm/done/20260806_review/r2_round2_lv1_analysis/report.md`, `_pm/tasks/20260808_review/r2_round2_lv2_analysis/worker_c_2.md`

### ㉮ 증상 (리뷰 시점 사실, 2026-08-06과 08-08)

- ㉠ `run` 하위 키를 `.get()`만으로 읽어 구 이름(`target_errors`)과 오타가 조용히 기본값으로 실행됐다
- ㉡ 최상위 `decoder` 블록 이름을 한 글자 틀리면 `setdefault`가 빈 dict를 만들어 디코더가 통째로 기본 구성으로 바뀐 채 완주했다. 실측 FER 0.9844 대 0.0000
- ㉢ `except ImportError`가 "패키지 없음"과 "패키지 내부 import 실패"를 구분하지 않아 기본 디코더로 조용히 대체됐다. 실행 루트를 잘못 잡아도 같은 대체가 발동했다
- ㉣ 원본 C++도 같은 부류다. dv 미매칭이면 `table_col_idx = 0`을 조용히 쓰고, 미커버 iteration에서 `selected_group = -1`로 배열 범위 밖을 읽는다. 재현하지 않기로 결정했다

### ㉯ 원인

- 검증 규칙이 "직접 인덱싱하는 필수 키의 부재"만 걸렀다. 선택 블록 이름과 미지 키는 전부 새어 나갔다
- "없으면 기본값"으로 처리한 곳이 전부 조용한 오동작 경로가 됐다

### ㉰ 점검 항목

- ㉠ 섹션별 허용 키 집합(키맵)으로 미지 키를 거부한다. 최상위 키도 키맵에 넣는다
- ㉡ 기본값은 dict 하나를 단일 정본으로 두고 검증, 소비, 요약이 같은 값을 읽는다
- ㉢ `except`는 원인을 구분한다 (`err.name` 확인). 대체가 일어나면 콘솔에 알리거나 에러로 끝낸다
- ㉣ 검증을 우회하는 직접 호출 경로(`run_fer_point` 직접 호출)에도 최소 가드를 둔다
- ㉤ 설정 메타(seed, 디코더 클래스, 커밋 해시)를 산출물에 남겨 사후 판별이 가능하게 한다

### ㉱ 현재 코드 (수리된 위치)

- ㉠ 키맵 `_TOP_KEYS`부터 `_STRONG_RATIOS_KEYS`까지 9개 (`src/run.py:98-111`), `_check_keys` (`:125-130`). `decoder` 블록 이름 오타는 최상위 키맵 검사가 거부한다 (`:281`)
- ㉡ `_RUN_DEFAULTS` 한 곳 (`src/run.py:116-117`)을 검증 (`:358-360`), 소비 (`:557-563`), 요약 (`:486-489`)이 함께 읽는다
- ㉢ 디코더는 `main(decoder_class=)`로 주입하고 `None`이면 `BaseDecoder`다 (`src/run.py:443-445`). 런처는 `from src.run import main`을 감싸지 않아 임포트 실패가 그대로 에러다 (`workspace/_template/run.py:22`)
- ㉣ `run_fer_point` 진입부 가드: 정수 4개 1 이상, log 항목 오타 (`src/sim.py:58-70`)
- ㉤ summary.txt 머리에 커밋 해시 `+dirty`, 디코더 모듈과 클래스, seed (`src/run.py:603-618, 483-484, 726-728`)
- ㉥ dv 미매칭은 에러 (`src/llr_matrix.py:347-357`), 미커버 iteration은 로더가 거부 (`:193-196`)

## 사용 방법

- 언제: 설정 파일을 읽는 코드, 변형 클래스를 임포트하는 코드, `.get(key, default)`나 `setdefault`를 쓰는 곳을 추가하거나 리뷰할 때
- 어떻게: "이 키 이름이 한 글자 틀리면 무슨 일이 일어나는가"를 묻는다. 답이 "기본값으로 완주"면 점검 항목 ㉠㉡을 적용한다. 임포트는 실패 원인을 구분하고 대체 없이 종료한다
- 주의: 조용히 틀린 수치는 hang보다 실질 피해가 크다. 심각도 판단에서 "완주했다"를 감점 사유로 본다

관련 문서
- [20260807_config-keymap-fail-fast.md](../decisions/20260807_config-keymap-fail-fast.md)
- [20260807_llr-file-interpretation-rules.md](../decisions/20260807_llr-file-interpretation-rules.md)
- [20260930_config-validation-rules.md](../tech/20260930_config-validation-rules.md)
- [20260930_reusable-code-patterns.md](20260930_reusable-code-patterns.md)
