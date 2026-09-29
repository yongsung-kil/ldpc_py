# 자산 (assets) 목록

다시 쓸 수 있는 것. 패턴, 잘못된 패턴, 프롬프트, 코드 조각.

문서 22편. 마지막 갱신 2026-09-30 (wiki 스킬 첫 실행).

| 문서 | 요약 | 종류 |
|---|---|---|
| [20260806_set-uniform-vs-order-uniform](20260806_set-uniform-vs-order-uniform.md) | argpartition으로 뽑은 앞 k개는 집합만 균일하고 내부 순서는 균일하지 않다. 결과를 구간 슬라이스로 나눠 쓰면 위치 편향이 생긴다 | antipattern |
| [20260806_silent-fallback-config-and-import](20260806_silent-fallback-config-and-import.md) | 설정 키 오타, 블록 이름 오타, 디코더 임포트 실패가 에러 없이 기본값이나 다른 디코더로 완주하는 조용한 대체 경로 | antipattern |
| [20260806_task-document-template-usage](20260806_task-document-template-usage.md) | 태스크 문서 양식 6절과 실제 사용에서 굳어진 확장 절(착수 조건, 확정 사항, 검증, 분석 문서 분리)의 쓰임새 | pattern |
| [20260807_fixed-input-array-regression](20260807_fixed-input-array-regression.md) | 리팩토링 전에 고정 seed 결과를 저장하고 뒤에 같은 조건으로 재실행해 배열 단위 완전 일치를 확인하는 회귀 방법. 실행 폴더 비교와 주입 검증의 통과 기준 포함 | pattern |
| [20260807_function-extraction-refactoring](20260807_function-extraction-refactoring.md) | 긴 진입 함수를 흐름 함수 하나와 목적 이름의 단계 함수, 상태 묶음 객체로 나누되 교체 지점 시그니처는 그대로 두는 절차 7단계 | pattern |
| [20260808_decision-bit-array-count-outside-loop](20260808_decision-bit-array-count-outside-loop.md) | 에러 집계는 column 루프 밖에서 판정비트 배열 전체를 훑는다. 루프 안에서 세면 부분 스케줄이 성공으로 오판정된다 | pattern |
| [20260808_deep-review-operating-rules](20260808_deep-review-operating-rules.md) | 딥 리뷰 검증 라운드에서 효과가 확인된 운영 규칙 6과 거짓 양성으로 판명된 지적의 공통 원인 5, 처방 채택 전 점검 4 | pattern |
| [20260808_equivalence-verification-methods](20260808_equivalence-verification-methods.md) | 등가 구현을 검증할 때 고르는 방법 9종 (스칼라 전수 대조, 비트 단위 회귀, 바이트 대조, 저장 로드 왕복, 분포 검정, 저장소 무수정 실증, 자동 검증 묶음, AST 대조, 무효과 조건 일치) | pattern |
| [20260808_optional-output-before-required-record](20260808_optional-output-before-required-record.md) | 선택 산출물(그림) 저장이 필수 기록(summary.txt) 앞에 있어 라이브러리 없는 새 환경에서 커밋 해시와 디코더 클래스 기록이 사라졌다. 순서 이동과 예외 흡수를 병용한다 | antipattern |
| [20260808_replacement-point-contract-protection](20260808_replacement-point-contract-protection.md) | 성능 최적화나 방어 코드를 본체에 넣을 때 자식 클래스의 교체 지점 재정의 계약을 깨지 않는 규칙 다섯 | pattern |
| [20260808_shared-rng-batch-dependence](20260808_shared-rng-batch-dependence.md) | 한 난수 생성기를 메시지와 잡음이 공유하고 종료 검사가 배치 단위라 frames_per_batch가 같은 seed의 수치를 바꾼다. 코드 수리 없이 문언 교정으로 종결 | antipattern |
| [20260808_user-review-note-handling](20260808_user-review-note-handling.md) | 코드 줄을 인용한 짧은 사용자 리뷰 노트를 항목별 변경 표로 옮겨 이름, 기능, 구조로 갈라 반영하고 원문은 보존하는 방식 | pattern |
| [20260808_zero-level-not-in-original](20260808_zero-level-not-in-original.md) | 원본에 없는 값(메시지 크기 0)을 균일 레벨에 도입하자 공명 붕괴, min1 점유, -0.0 부호 소실 세 증상이 한 뿌리에서 나왔다 | antipattern |
| [20260809_antipattern-filename-decides-semantics](20260809_antipattern-filename-decides-semantics.md) | 파일에 없는 정보(VNU 출력 레벨)를 파일명 부분문자열로 정하면 오탐과 무경고 오답이 생긴다. 판정은 파일 내용의 값 패턴으로 한다 | antipattern |
| [20260809_cpp-static-analysis-procedure](20260809_cpp-static-analysis-procedure.md) | C++ 원본을 빌드 없이 정적으로 읽어 이식 설계를 확정하는 절차 11단계 (함수 사슬 추적, 비교표, 상수 분리, 이식 지점 매핑, 확인 불가 명시, 실증) | pattern |
| [20260813_clip-at-reconstruct-not-stored-state](20260813_clip-at-reconstruct-not-stored-state.md) | min1/min2가 증분 갱신되는 CN 저장 상태에는 값 변형을 넣지 않고, C2V를 읽어 내는 시점(`_c2v_reconstruct`)에 변형을 건다 | pattern |
| [20260813_paper-idea-single-override-procedure](20260813_paper-idea-single-override-procedure.md) | 논문 아이디어를 교체 지점 하나만 재정의해 붙이고, 무효과 조건 일치와 유효 재정의 차이의 두 방향으로 검증한 뒤 on/off 비교하는 절차 | pattern |
| [20260813_refactor-regression-by-worktree](20260813_refactor-regression-by-worktree.md) | refactor 직전 커밋을 git worktree로 꺼내 같은 조건으로 실행하고 HEAD와 수치 완전 일치를 확인하는 회귀 절차. 기준 커밋 선택 함정 포함 | pattern |
| [20260814_fix-misquoted-cause-with-logged-values](20260814_fix-misquoted-cause-with-logged-values.md) | 실험 결론의 원인 서술에 실험이 타지 않은 경로의 파라미터 값을 인용하는 오류와, summary.txt와 파일 실값과 dv별 로그로 바로잡는 절차 | antipattern |
| [20260814_slot-config-and-pq-scan](20260814_slot-config-and-pq-scan.md) | 같은 delta를 스케일이 다른 환경 세 벌(headroom, balanced, real)의 슬롯 config에서 돌리고, (P,Q) 쌍 목록을 인자로 받는 scan 스크립트로 반복 실행하는 구조 | pattern |
| [20260930_doc-code-drift-checklist](20260930_doc-code-drift-checklist.md) | 문서와 코드가 어긋나는 유형 17가지. 유형마다 사례 한 줄과 검사 방법 한 줄 (리뷰 3회와 탐색 교차 검증에서 수집) | antipattern |
| [20260930_reusable-code-patterns](20260930_reusable-code-patterns.md) | 다른 시뮬레이터나 배치 실험 코드에 옮겨 쓸 수 있는 코드 패턴 6개와 현재 코드 위치 | snippet |
