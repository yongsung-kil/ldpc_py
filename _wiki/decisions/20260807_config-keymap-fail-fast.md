---
summary: config 검증은 키맵, 필수값, 값 제약 세 층으로 `load_config`에서 한꺼번에 fail-fast하고, `_` 접두 키만 설명용으로 건너뛰며, 디코더 임포트 실패도 에러로 끝낸다 (조용한 대체 없음)
status: Accepted
tags: [config, validation, fail-fast]
date: 2026-08-07
commit: 0394b81 (시험장 사본에 포함)
source: _pm/done/20260807_리뷰후속수정/20260807_리뷰후속수정.md:15, 17-18, 32-38; src/run.py:98-144; _pm/TODO.md:22, 28; docs/profile/structure.md:61
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 2026-08-06 딥 리뷰 F3: `run` 하위 키를 `.get()`으로만 읽어 오타 키와 구 이름이 조용히 기본값으로 실행됐다. 최상위 블록 이름을 한 글자 틀리면 디코더가 통째로 기본 구성으로 바뀐 채 완주했다 (실측 FER가 크게 달랐다)
  - ㉡ F19: 값 타입과 범위 검사가 없었다
  - ㉢ 2026-08-08 리뷰: `except ImportError`가 "패키지 없음"과 "패키지 내부 import 실패"를 구분하지 않아 기본 디코더로 조용히 대체됐다
- ㉯ 거부한 대안
  - ㉠ 모르는 키를 조용히 무시하고 기본값으로 진행
  - ㉡ 임포트 실패 시 기본 디코더로 대체하고 계속 실행
  - ㉢ F21 "config 값 통계가 무의미"는 테스트용 config라 폐기
- ㉰ 이유
  - ㉠ 오타 난 키가 조용히 무시되면 사용자가 의도한 설정과 다른 실험이 완주되고, 결과만 보고는 알 수 없다
  - ㉡ 조용한 대체는 실수를 유발한다. dv 미매칭을 에러로 두는 결정과 같은 뿌리다
- ㉱ 결과로 생긴 규칙
  - ㉠ 키맵(섹션별 허용 키 집합), 필수값, 값 제약 세 층을 `load_config`에서 일괄 fail-fast한다. 허용 밖 키는 섹션과 키 이름을 적은 `ValueError`로 즉시 종료하고, 소비 여부와 무관하게 형식은 항상 검사한다
  - ㉡ `_`로 시작하는 키(`_desc`)는 설명용이라 검사에서 뺀다
  - ㉢ `run_fer_point` 진입부에도 최소 가드를 둔다 (직접 호출이 `load_config`를 우회하므로). run 기본값은 `_RUN_DEFAULTS` 한 곳이고 검증, 소비, 요약이 같은 값을 쓴다
  - ㉣ 디코더 임포트 실패는 에러 종료 (2026-08-09 사용자 확정). registry 폐지 뒤에는 런처가 클래스를 직접 import하므로 실패가 곧 에러다
  - ㉤ 키맵 9개와 헬퍼 4개의 현행 위치와 검사 순서는 [20260930_config-validation-rules.md](../tech/20260930_config-validation-rules.md)
- ㉲ 비용
  - ㉠ 새 키를 추가하면 키맵도 함께 고친다
  - ㉡ 키별 허용값 확정 목록은 TODO에 남아 있다
  - ㉢ 2026-08-13 스키마 재편 뒤에도 세 층 구조는 그대로다

## 하위 링크

- [../assets/20260806_silent-fallback-config-and-import](../assets/20260806_silent-fallback-config-and-import.md): 이 결정이 막은 조용한 fallback 증상 셋과 점검 항목
- [../tech/20260930_config-validation-rules](../tech/20260930_config-validation-rules.md): 현행 키맵 9개, 헬퍼 4개, 검사 순서
- [20260813_config-slots-and-flags](20260813_config-slots-and-flags.md): 검증이 걸리는 config 구조 (값 자리와 플래그)
