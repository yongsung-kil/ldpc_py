---
summary: 코드 줄을 인용한 짧은 사용자 리뷰 노트를 항목별 변경 표로 옮겨 이름, 기능, 구조로 갈라 반영하고 원문은 보존하는 방식
type: pattern
tags: [review, naming, user-note]
date: 2026-08-08
last_verified: 2026-09-30
---

## 내용

- 근거: `_pm/done/20260808_의견1_반영/의견1.md`, `_pm/DONE.md` 2026-08-08 항목
- ㉮ 노트 형식: 코드 한 줄을 인용하고 뒤에 "X는 Y야? 그렇게 수정해" 또는 "이건 뭐야?"가 붙는 짧은 질문 묶음
- ㉯ 해석 원칙: 질문 자체가 결함 신호다. 물어봐야 뜻을 아는 이름은 고친다. 이름의 판단 기준은 [20260807_purpose-is-the-name.md](../decisions/20260807_purpose-is-the-name.md)
- ㉰ 반영 방식: 질문을 성격별로 가른다
  - ㉠ 이름 질문: "현재 이름 | 새 이름 | 이유" 항목별 변경 표로 만들고 일괄 치환한다. 치환 뒤 조사 어긋남과 부분문자열 오염을 grep으로 검사한다
  - ㉡ 정보 요구 ("summary에 코드 정보, 디코더 정보, 읽은 config 정보"): 기능으로 구현한다 (setup 직후 콘솔과 summary.txt 상단의 실험 요약)
  - ㉢ 구조 요구: 코드 구조로 반영한다
  - ㉣ 구현 용어 노출 (자료형 이름이 docstring에): 뜻 중심 표현으로 바꾼다
- ㉱ 문장 규칙 승격: 노트 속 서술 규칙은 프로젝트 문장 규칙으로 올렸다. 내용은 [20260808_rewrite-not-patch-positive-rules.md](../decisions/20260808_rewrite-not-patch-positive-rules.md)
- ㉲ 보존: 노트 원문은 손대지 않고 완료 폴더에 그대로 둔다. 답변을 원문에 끼워 넣지 않는다
- ㉳ 잘못된 패턴: 질문에 답만 하고 이름을 그대로 둔다. 기존 문장 뒤에 괄호로 단서를 덧댄다. docstring에 변경 이력을 적는다

## 사용 방법

- ㉮ 언제: 사용자가 코드를 읽으며 남긴 노트 파일을 받았을 때
- ㉯ 어떻게: 노트를 `_pm/tasks/{작업명}/`에 원문 그대로 두고, 태스크 문서에 변경 표를 만든 뒤 반영한다. 완료 시 표를 DONE 항목에 요약한다
- ㉰ 주의: 이름을 바꾸면 CSV 헤더와 진행 줄 지표, 프로파일 문서까지 같은 이름으로 맞춘다. 식별자는 영어, 주석과 예외 문구는 한국어
- 관련 문서
  - [20260807_purpose-is-the-name.md](../decisions/20260807_purpose-is-the-name.md)
  - [20260808_rewrite-not-patch-positive-rules.md](../decisions/20260808_rewrite-not-patch-positive-rules.md)
  - [20260806_task-document-template-usage.md](20260806_task-document-template-usage.md)
