---
summary: toy 2SD/3SD LLR 파일의 ch와 th 값을 C++ 원본의 하드코딩 기본 테이블에서 가져오려 했으나 초기화식이 소실되어 추정값을 썼다
result: failed
tags: [sd, toy, cpp-source, lost-values]
date: 2026-08-09
source:
  - _pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md
  - _pm/done/20260809_2SD3SD구현/20260809_2SD3SD구현.md
adopted_as: decisions/20260809_sd-decoding-decisions
---

## 시도 내용

- ㉮ 배경: 2SD/3SD(2-bit, 3-bit soft decision) 구현을 toy LLR 파일로 개발하기로 했고, 실물 SD 파일이 저장소에 없었다
- ㉯ 시도: 태스크 문서의 미결정 "toy 파일의 ch/th 값은 C++ 분석에서 원본 기본값이 나오면 그것을 쓴다". C++ 정적 분석에서 비 AUTO 빌드가 쓰는 하드코딩 기본 테이블을 찾았다

## 결과

- ㉮ `Ch_LLR_3SD`(decoder.cpp:6932)와 `table_HD`, `table_2SD`, `table_3SD`(decoder.cpp:7143-7145)는 선언만 있고 초기화식이 없다. 3SD 채널 LLR 기본표와 VNU 임계값 기본표 전부 소실
- ㉯ `Ch_LLR_2SD`(decoder.cpp:6842-6931)와 `Ch_LLR_HD`(decoder.cpp:6693-6841)는 초기화식이 있으나 3-bit 분기의 전 row가 같은 자리표시 값이라 iteration별 변화가 사라졌다
- ㉰ 결론: toy 2SD/3SD 파일의 ch와 th 값은 원본에서 가져올 수 없다
- ㉱ 영향 범위: AUTO(DAO) 빌드는 파일에서 읽으므로 이식 자체에는 영향 없음. toy 값의 근거로만 쓸 수 없다
- 교훈:
  - ㉠ 원본 소스의 손상 여부(선언만 있는 배열, 깨진 인코딩)를 분석 앞머리에서 확인하고 "확인 불가 항목"으로 명시한다
  - ㉡ 실물 값은 외부 공급이다. 저장소 파일은 파이프라인 확인용 toy로 둔다

## 대안 선택 (있을 경우)

- ㉮ 합리적 추정값 사용. `Ch_LLR_2SD`의 자리표시 값은 "strong이 weak의 약 3배"라는 크기 관계 참고로만 썼다
- ㉯ 추정값은 반전 가능 조건 `ch <= 7*dv`를 지켜 만들었다
- ㉰ 실물 SD 파일 반입 시 HD와 같은 방식으로 교체
- 관련 문서
  - ㉠ [20260809_sd-decoding-decisions.md](../decisions/20260809_sd-decoding-decisions.md)
  - ㉡ [20260809_cpp-static-analysis-procedure.md](../assets/20260809_cpp-static-analysis-procedure.md)
  - ㉢ [20260807_flip-condition-ch-le-7dv.md](../tech/20260807_flip-condition-ch-le-7dv.md)
  - ㉣ [20260730_input-files-external-supply.md](../decisions/20260730_input-files-external-supply.md)
