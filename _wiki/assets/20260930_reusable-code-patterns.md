---
summary: 다른 시뮬레이터나 배치 실험 코드에 옮겨 쓸 수 있는 코드 패턴 6개와 현재 코드 위치
type: snippet
tags: [python, numpy, reproducibility, config]
date: 2026-09-30
last_verified: 2026-09-30
---

## 내용

- 근거: `src/run.py`, `src/sim.py`, `src/decoder.py` (2026-08-05부터 08-10 사이에 쓰인 코드를 2026-09-30 탐색에서 모았다)

### ㉮ 난수 스트림 파생

- 한 줄: 최상위 seed 하나에서 포인트마다 `np.random.default_rng([seed, channel_index, int(1e6 * point)])`로 독립 스트림을 만든다
- 현재 코드: `src/run.py:586`. 설정 검증이 `int(1e6 * 값)` 중복을 미리 막아 같은 스트림으로 두 번 측정되는 일을 없앤다 (`:175-179`)

### ㉯ 파일 꼬리 제자리 갱신

- 한 줄: 시작 시 파일 크기를 offset으로 기억하고 `seek(offset); truncate(); write(text)`로 진행 줄을 갱신하다가 끝나면 결과 줄로 대체한다
- 현재 코드: `_rewrite_file_tail` (`src/sim.py:21-26`), offset 확보 (`:92`), 진행 줄 (`:135`), 결과 줄 (`:164-166`). 콘솔 `\r` 갱신은 `sys.stdout.isatty()`일 때만 (`:86`)

### ㉰ 재현성 기록

- 한 줄: 실행 폴더에 config 사본과 `git rev-parse --short HEAD`를 남기고, 미커밋 변경이 있으면 `+dirty`를 붙인다
- 현재 코드: `_git_commit_hash` (`src/run.py:603-618`), config 사본과 summary.txt 머리 (`:725-728`)

### ㉱ 설정 검증 원칙

- 한 줄: 소비 여부와 무관하게 형식은 항상 검사하고, 조합 제약은 소비 시점에 검사한다. `_` 접두 키는 설명용이라 검사에서 뺀다
- 현재 코드: 원칙 서술 (`src/run.py:250-254, 296-298`), 조합 제약을 레벨 생성부가 판정 (`:331-337`), `_visible` (`:120-122`)

### ㉲ 선택 항목 오타 검출

- 한 줄: 허용 집합과의 차집합 `요청 - 허용`이 비어 있지 않으면 즉시 에러. 집합 연산 한 줄로 오타를 잡는다
- 현재 코드: `src/decoder.py:497-499`, `src/sim.py:67-70`

### ㉳ 선택 의존성 지연 import와 실패 흡수

- 한 줄: 선택 기능이 쓰는 라이브러리는 그 함수 안에서 import하고, 호출부는 `except Exception`으로 감싸 사유를 출력한 뒤 계속 간다
- 현재 코드: matplotlib 지연 import (`src/run.py:694-696`), 호출부 (`:771-775`)

## 사용 방법

- 언제: 새 시뮬레이터나 배치 실험 하니스를 만들 때, 기존 코드에 진행 표시나 재현성 기록을 붙일 때
- 어떻게: 필요한 패턴의 현재 코드 줄을 열어 그대로 옮긴다. 이름은 옮기는 쪽 용어로 바꾸되 구조(offset 기억, 차집합 검사, 지연 import)는 유지한다
- 주의: ㉮는 seed와 `frames_per_batch`가 같아야 수치가 재현된다. ㉯는 같은 파일에 다른 쓰기가 끼어들면 offset이 어긋난다. ㉳는 필수 산출물에는 쓰지 않는다

관련 문서 (피할 패턴은 여기서 다시 쓰지 않는다)
- [20260806_silent-fallback-config-and-import.md](20260806_silent-fallback-config-and-import.md) (조용한 fallback)
- [20260806_set-uniform-vs-order-uniform.md](20260806_set-uniform-vs-order-uniform.md) (argpartition 구간 슬라이스)
- [20260808_decision-bit-array-count-outside-loop.md](20260808_decision-bit-array-count-outside-loop.md) (column 루프 안 에러 집계)
- [20260808_replacement-point-contract-protection.md](20260808_replacement-point-contract-protection.md) (비정수 raw 등가식, `_cnu_update` 반환값 의존)
