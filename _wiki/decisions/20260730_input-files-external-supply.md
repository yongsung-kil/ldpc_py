---
summary: 평가 대상 H-matrix와 LLR 테이블은 저장소 밖에서 공급받아 `Input/`에 넣고 config로 지정한다. 저장소에 든 파일은 toy(예시)이고, toy로 개발한 뒤 실물이 들어오면 교체한다
status: Accepted
tags: [input, data, toy]
date: 2026-07-30
commit: 0394b81 (시험장 사본에 포함)
source: README.md:39-41, 205-206, 223, _pm/done/20260730_review/r2_round2_lv1_analysis/report.md:17-18, 22, _pm/tasks/20260808_review/종합보고.md:17-23, _pm/done/20260809_2SD3SD구현/20260809_2SD3SD구현.md:19-24, _pm/TODO.md:38-40, src/run.py:403-404, docs/profile/constraints.md:32, 49, 54
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 계획 리뷰(2026-07-30)에서 H-matrix 파일, LLR 테이블 실값, 빌드 가능한 C++ 소스 세 자산이 저장소에 없음이 확인됐다. LLR 실값은 원본 소스 손상으로 소실됐다
  - ㉡ 2026-08-03에 구 코드로 3-bit 정밀도를 추정 튜닝했으나 실값 없이는 한계였다
  - ㉢ 2026-08-09 딥 리뷰가 저장소 toy LLR 파일의 기본 실행 FER 1.0을 HIGH로 잡았다
- ㉯ 거부한 대안
  - ㉠ 저장소 toy 파일을 실사용 파라미터로 계속 튜닝하는 것
  - ㉡ toy 파일이 FER 1.0을 내는 상태를 "고쳐야 할 결함"으로 다루는 것 (생성자 검사 추가, toy 값 수정)
  - ㉢ H-matrix 생성을 실험 흐름 안에 두는 것
- ㉰ 이유
  - ㉠ 실값 없이는 추정 튜닝에 한계가 있고, toy는 파이프라인 동작 확인용이면 충분하다
  - ㉡ toy 파일의 FER 1.0은 디코더 결함이 아니라 데이터 특성이다. 실물 반입 시 교체되므로 조치하지 않는다 (사용자 확인 2026-08-09)
  - ㉢ H-matrix 생성은 별도 프로젝트 담당이라 실험 흐름은 파일로만 받는다
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ config의 `H_matrix`와 `decoder.llr_matrix`는 `{"dir", "file"}`로 `Input/` 아래 파일을 가리킨다. setup은 H-matrix가 없으면 에러를 내고 생성하지 않는다 (src/run.py:403-404)
  - ㉡ 2SD/3SD도 toy 파일로 개발하고 실물 반입 시 교체한다 (사용자 확정 2026-08-09)
  - ㉢ "평가 대상 파일을 `Input/`에 넣고 config 기본값 교체"가 TODO에 남아 있고, 논문 실험(minsum_dual_clip)의 최종 판정이 이 항목을 선행 조건으로 둔다
  - ㉣ toy 파일의 반전 가능 조건 위반은 알려진 위반 상태로 프로파일에 기록되어 있다 (docs/profile/constraints.md:49)
  - ㉤ 입력 파일의 출처와 공급자를 문서에 적지 않는 명문 규칙은 아직 없고 판정요청에 올라 있다 (2026-09-30)
- 날짜: 2026-07-30 (자산 부재 확인, 외부 공급), 2026-08-09 (toy로 개발, FER 1.0 무조치)

## 하위 링크

- [20260809_fer-one-no-action-example-data.md](20260809_fer-one-no-action-example-data.md): 저장소 예시 LLR의 FER 1.0을 조치하지 않기로 한 결정과 반전 가능 조건
- [../trials/20260803_three-bit-precision-tuning-trial.md](../trials/20260803_three-bit-precision-tuning-trial.md): 실값 없이 한 추정 튜닝의 한계. 외부 공급으로 방향을 바꾼 계기
- [20260930_input-source-notation-rule.md](20260930_input-source-notation-rule.md): 입력 파일 공급자와 실값을 적지 않는 규칙 신설 여부 (판정요청)
- [../../docs/profile/constraints.md](../../docs/profile/constraints.md): "입력 파일은 외부 공급" 행, 알려진 위반 상태, 기밀과 표기 규칙 ㉯
