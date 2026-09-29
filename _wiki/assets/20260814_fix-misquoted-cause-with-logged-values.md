---
summary: 실험 결론의 원인 서술에 실험이 타지 않은 경로의 파라미터 값을 인용하는 오류와, summary.txt와 파일 실값과 dv별 로그로 바로잡는 절차
type: antipattern
tags: [root-cause, misquote, summary, dv-log]
date: 2026-08-14
last_verified: 2026-09-30
---

## 내용

- ㉮ 증상: 2026-08-13 minsum_dual_clip 결론이 "채널 LLR 8, 반전 조건 ch <= P*dv"라고 적었다. 8은 균일 생성 경로의 `channel_llr` 값인데 실험은 LLR 파일 로드 경로였고 파일의 ch는 dv마다 달랐다 (toy 파일 dv=4는 10, dv=2는 28). 잘못된 값 위에 세운 결론이라 사망 경계도 틀렸다
- ㉯ 원인
  - ㉠ 결론을 쓸 때 실행 폴더의 summary.txt를 다시 보지 않고 머릿속 config 값을 인용했다
  - ㉡ 균일 경로와 파일 경로가 같은 로더를 타므로 결과 파일 모양만으로는 어느 경로였는지 구분되지 않는다
  - ㉢ dv별 분해 없이 프레임 단위 FER만 보고 원인을 추정했다
- ㉰ 점검 항목 (원인 서술을 쓰기 전)
  - ㉠ summary.txt의 `LLR matrix` 줄로 실제 경로를 확인한다 ("(파일 로드)"인지 `_generated/` 아래 uniform 파일명인지)
  - ㉡ 그 경로의 실값을 읽는다. 파일 경로면 LLR 파일의 dv 구간별 ch, 균일 경로면 `channel_llr_{mode}`
  - ㉢ summary.txt의 `col degree` 분포에서 지배 dv를 찾는다
  - ㉣ `log.items.bit_err_by_dv`(dv별 에러 로그)와 `fail_frame_detail`로 어느 dv가 고착인지 실측 대조한다
  - ㉤ 무클립에서도 이미 위반인 열(예: toy 파일 dv=2)은 on/off 차이의 원인에서 제외한다
- ㉱ 정정 절차
  - 1. 위 점검 ㉠㉡으로 인용값을 바로잡는다
  - 2. (P,Q)마다 dv별 경계 `Q + (dv-1)*P`를 계산해 생존 표를 만든다
  - 3. dv별 로그로 표를 실측 대조한다 (예: dv=4, ch=10이면 (2,3)은 9로 사망, (2,5)는 11로 생존)
  - 4. 태스크 문서와 DONE.md에 정정 경위를 한 줄 남긴다. 원 문장은 덧대지 않고 다시 쓴다
- ㉲ 트리거: 사용자의 대안 가설 질문("H-matrix 품질이나 edge 양자화 자체가 원인 아니냐")에 실값으로 답하려다 오류를 발견했다. 대안 가설 질문은 재검토 신호로 다룬다

## 사용 방법

- ㉮ 언제: 실험 결과의 원인을 파라미터 값으로 설명하는 문장을 쓸 때마다. 특히 config에 값 자리가 여러 개 있고 플래그가 하나를 고르는 구조에서
- ㉯ 어떻게: 원인 문장에 인용한 숫자마다 "summary.txt 어느 줄, 어느 파일 어느 값"을 괄호로 적을 수 있는지 확인한다. 적을 수 없으면 인용하지 않는다
- ㉰ 주의: 이 사본에는 당시 실행 폴더가 없어 수치는 DONE.md 서술 기준이다. summary.txt 실험 요약 줄의 형식은 `src/run.py:458-493`의 `_experiment_summary_lines`가 정하며 `LLR matrix` 줄은 파일명 뒤 괄호에 공급 경로를 적는다 (`:481`)
- 관련 문서
  - ㉠ [20260813_minsum-dual-clip-trial.md](../trials/20260813_minsum-dual-clip-trial.md)
  - ㉡ [20260807_flip-condition-ch-le-7dv.md](../tech/20260807_flip-condition-ch-le-7dv.md) (사망 경계 판단 절차)
  - ㉢ [20260930_run-dir-and-output-files.md](../tech/20260930_run-dir-and-output-files.md)
  - ㉣ [20260813_config-slots-and-flags.md](../decisions/20260813_config-slots-and-flags.md)
