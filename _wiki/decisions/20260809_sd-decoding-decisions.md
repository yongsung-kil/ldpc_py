---
summary: 2SD/3SD 구현의 사용자 확정 네 건. toy 파일로 개발, 균일 생성도 SD 지원, Pre 단계 시딩 magnitude는 3-bit 파일이면 C++ 고정 상수이고 균일 n-bit면 균등 분할, Edge Clear는 전 모드에서 restart iteration만
status: Accepted
tags: [soft-decision, decoder, edge-clear]
date: 2026-08-09
commit: 0394b81 (시험장 사본에 포함)
source: _pm/done/20260809_2SD3SD구현/20260809_2SD3SD구현.md:19-40; _pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md:384-402; src/decoder.py:120-134, 137-144; docs/차이.md:23, 41
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 2SD/3SD(2단계와 3단계 soft decision) 구현을 C++ 원본 정적 분석(파일:줄 근거)으로 설계했다
  - ㉡ 실물 2SD/3SD 파일이 저장소에 없었다. 분석 문서가 "시딩 magnitude는 고정 상수인가 edge_mag 상위 레벨인가"를 미결정으로 올렸다
- ㉯ 확정 네 건
  - ㉠ toy LLR_MATRIX로 개발하고 실물은 반입 시 교체한다 (HD와 같은 방식)
  - ㉡ 균일 생성 모드도 2SD/3SD를 지원한다. `channel_llr`은 HD가 정수 하나, 2SD/3SD는 강한 region부터 2개 또는 4개 리스트 (2026-08-13 `channel_llr_{HD|2SD|3SD}` 자리로 재편)
  - ㉢ Pre 단계 시딩 magnitude: 3-bit DAO 파일은 C++ `Make_LLR`의 고정 상수 2SD [5, 1], 3SD [7, 5, 3, 1]이고 파일에서 읽지 않는다. 균일 n-bit는 C++ 대응이 없어 1..top을 region 수로 균등 분할한다 (3-bit 3SD에서 C++ 값과 일치). 미결정을 파일 종류로 갈라 둘 다 채택했다 (`src/decoder.py:120-134`)
  - ㉣ Edge Clear는 전 모드에서 restart iteration만 한다. 원본 HD의 iteration 1 클리어는 재현하지 않는다 (`:137-144`)
- ㉰ 거부한 대안
  - ㉠ 시딩 magnitude를 LLR 파일에서 읽기 (C++ `Make_LLR`이 고정 상수라 대응이 없다)
  - ㉡ 원본 HD의 iteration 1 클리어 재현
- ㉱ 이유
  - ㉠ 원본 HD의 iteration 1 클리어는 Ref-C와 RTL의 iteration 0 저장 차이를 없애려는 보정(decoder.cpp:6570 주석)이고 py는 그 차이가 없다. iteration 1의 CN 상태가 초기값 그대로라 산술 결과도 같다 (HD 회귀로 산출물 동일 확인)
  - ㉡ 균일 균등 분할은 3-bit 3SD에서 C++ 상수와 일치하므로 확장으로서 자연스럽다
- ㉲ 결과로 생긴 규칙과 비용
  - ㉠ 3-bit 균일 2SD는 [7, 1]이 되어 C++ [5, 1]과 다르다. 사용자가 실행하며 조정한다
  - ㉡ SD restart의 Pre 재실행은 `llr_matrix.is_restart`를 직접 보므로 `_is_edge_clear_iter` 재정의로 바뀌지 않는다
  - ㉢ C++ SD는 클리어 때 syndrome을 지우고 Pre 단계가 check_sum에서 다시 만든다. py는 syndrome을 유지하고 재계산하지 않는다. 두 값이 `H*read_bit`으로 같아 관측 등가다
  - ㉣ 3-bit 파일도 균일 경로도 아닌 넓은 레벨의 SD 시딩은 3-bit 상수로 떨어진다. 의도인지 미확인이다

## 하위 링크

- [../tech/20260930_sd-region-and-pre-stage](../tech/20260930_sd-region-and-pre-stage.md): region 매핑 식, Pre 단계, SD restart의 현행 코드와 C++ 대응
- [../trials/20260809_toy-sd-values-source-lost](../trials/20260809_toy-sd-values-source-lost.md): toy 값을 원본에서 얻으려다 초기화식 소실로 추정값을 쓴 경위
- [20260730_input-files-external-supply](20260730_input-files-external-supply.md): toy로 개발하고 실물은 외부 공급으로 교체하는 원칙
