---
summary: avg_decoding_iteration은 실패 프레임을 max_iter로 포함한 전 프레임 평균이고, summary.txt는 측정 시작 전에 만들어 진행 줄을 꼬리에서 제자리 갱신하다 결과 줄로 대체한다
status: Accepted
tags: [metrics, summary, output]
date: 2026-08-10
commit: 0394b81 (시험장 사본에 포함)
source: _pm/DONE.md:93-118; src/sim.py:21-26, 139-147, 156-166; src/run.py:603-618, 715-733; README.md:132-155
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 기존 지표 `avg_decode_success_iteration`은 성공 프레임만 평균해 전 프레임이 실패하면 0.0이 나왔다
  - ㉡ summary.txt는 종료 후에만 저장돼 중간에 죽으면 사라졌다. 2026-08-08 딥 리뷰에서 그림 저장이 summary 앞에서 실패해 커밋 해시와 실제 디코더 클래스 기록이 소실된 사례가 있었다
  - ㉢ 실행 폴더 자체는 2026-08-07에 도입됐고, 2026-08-10 사용자 지시로 지표와 기록 시점을 바꿨다
- ㉯ 거부한 대안
  - ㉠ 성공 프레임만 평균하는 지표 유지
  - ㉡ summary를 종료 후 저장하되 그림 저장만 try/except로 감싸기
- ㉰ 이유
  - ㉠ 실패 프레임은 max_iter를 다 돌았으므로 처리량 지표(it/s)와 같은 분자를 써야 평균 iteration이 실제 연산량을 말한다
  - ㉡ 필수 기록(설정 사본, 커밋 해시, 디코더 클래스, 결과 줄)은 측정 시작 시점과 포인트 종료 시점에 먼저 쓴다. 순서 이동과 try/except는 병용한다
- ㉱ 결과로 생긴 규칙
  - ㉠ `avg_decoding_iteration = (성공 프레임 수렴 iteration 합 + errors * max_iter) / frames`. `ips`(초당 iteration)도 같은 분자를 쓴다 (`src/sim.py:140-147`)
  - ㉡ 표시명은 avg_iter, 내부 키와 CSV 열명은 avg_decoding_iteration
  - ㉢ 실행 폴더 `{output.dir}/{YYMMDD_HHMMSS}_{label}/`와 summary.txt 머리(run 표기, code commit과 `+dirty`, start 시각, 실험 요약)를 `create_run_dir`가 측정 전에 만든다 (`src/run.py:715-733`)
  - ㉣ 진행 줄은 `progress_interval_frames`마다 `_rewrite_file_tail`로 파일 꼬리를 교체하고, 포인트가 끝나면 결과 줄로 대체한다. 터미널 여부와 무관하게 파일에는 항상 반영된다 (`src/sim.py:21-26, 135, 165`)
  - ㉤ 콘솔 결과 줄과 summary 결과 줄은 `summary_line` 하나를 공유해 문자 단위로 같다
  - ㉥ CSV, 로그, 그림은 종료 후 저장하고 그림 실패는 `except Exception`으로 흡수한다
- ㉲ 비용과 활용
  - ㉠ 회귀 비교는 fer CSV와 summary 결과 줄 대조로 한다. 지표 변경 전 실행과는 avg_iter 값이 다르다
  - ㉡ 진행 줄 갱신마다 파일 열기와 truncate가 일어난다 (간격은 `run.progress_interval_frames`로 조절)

## 하위 링크

- [../tech/20260930_fer-point-loop-and-metrics](../tech/20260930_fer-point-loop-and-metrics.md): 측정 루프, 지표 산식, 진행 줄의 현행 코드
- [../tech/20260930_run-dir-and-output-files](../tech/20260930_run-dir-and-output-files.md): 실행 폴더 구조와 summary.txt, CSV 열
- [../assets/20260808_optional-output-before-required-record](../assets/20260808_optional-output-before-required-record.md): 선택 산출물이 필수 기록 앞에서 죽는 antipattern
