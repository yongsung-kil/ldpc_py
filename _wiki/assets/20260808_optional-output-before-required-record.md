---
summary: 선택 산출물(그림) 저장이 필수 기록(summary.txt) 앞에 있어 라이브러리 없는 새 환경에서 커밋 해시와 디코더 클래스 기록이 사라졌다. 순서 이동과 예외 흡수를 병용한다
type: antipattern
tags: [output, dependency, robustness]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/tasks/20260808_review/r3_round3_lv2_verification/team_b_verification.md`, `_pm/tasks/20260808_review/종합보고.md`

### ㉮ 증상 (리뷰 시점 사실, 2026-08-08)

- 그림 저장(matplotlib)이 summary.txt 저장보다 먼저 실행됐다. matplotlib이 없는 환경에서 측정을 완주한 뒤 exit 1
- CSV는 남고 summary.txt는 없었다. 재실행 없이 복구 불가 항목 2건: 커밋 해시, 실제 쓰인 디코더 클래스

### ㉯ 왜 엣지케이스가 아닌가

- 의존성 선언 파일이 없었고, config 두 벌 모두 그림 저장이 기본 on이었다. 새 환경의 첫 실행이 곧 이 경로였다
- 리뷰가 HIGH로 상향했다. 조용히 사라지는 기록은 실패보다 늦게 발견된다

### ㉰ 점검 항목

- ㉠ 필수 기록(설정 사본, 커밋 해시, 디코더 클래스, 결과 줄)은 측정 시작 시점과 포인트 종료 시점에 먼저 쓴다
- ㉡ 선택 항목은 `except Exception`으로 감싸 사유를 출력하고 정상 종료한다. `ImportError`만 잡으면 `savefig` 실패를 놓친다
- ㉢ 순서 이동과 try/except는 배타가 아니라 병용한다
- ㉣ 서드파티 의존은 requirements 같은 선언 파일에 적는다

### ㉱ 현재 코드 (수리된 위치)

- ㉠ `create_run_dir`가 측정 전에 config 사본과 summary.txt 머리(run 표기, 커밋 해시 `+dirty`, 실험 요약)를 쓴다 (`src/run.py:715-733`)
- ㉡ 포인트 결과 줄은 측정 중 `run_fer_point`가 summary.txt 꼬리에 실시간 기록한다 (`src/sim.py:164-166`)
- ㉢ `report`는 CSV, 로그 CSV, LLR 사본 뒤에 그림을 마지막으로 두고 `except Exception`으로 감싼다. matplotlib은 그 함수 안에서만 지연 import한다 (`src/run.py:694-696, 769-775`)
- ㉣ `requirements.txt`가 저장소 루트에 있다. `fer_curve_png`는 log 항목이라 기본 꺼짐이다 (`src/run.py:386-387`)

## 사용 방법

- 언제: 결과 저장 함수에 그림, 리포트 변환, 외부 업로드처럼 실패해도 되는 단계를 넣을 때
- 어떻게: 산출물을 "재실행 없이 복구 불가"와 "다시 만들 수 있음"으로 나눈다. 앞 것은 만들어지는 즉시 쓰고, 뒤 것은 마지막에 예외 흡수로 감싼다
- 주의: 새 환경 첫 실행을 시험 케이스로 둔다. 의존성을 하나 지운 가상환경에서 한 번 돌려 필수 기록이 남는지 본다

관련 문서
- [20260930_run-dir-and-output-files.md](../tech/20260930_run-dir-and-output-files.md)
- [20260810_avg-iteration-and-realtime-summary.md](../decisions/20260810_avg-iteration-and-realtime-summary.md)
- [20260806_silent-fallback-config-and-import.md](20260806_silent-fallback-config-and-import.md)
- [20260930_reusable-code-patterns.md](20260930_reusable-code-patterns.md)
