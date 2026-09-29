---
summary: 교체 단위는 원본 C++ 함수 경계다. 본체 디코더가 그 경계를 따라 교체용 함수를 떼어 두고, 논문 아이디어는 BaseDecoder를 상속한 자식 클래스에서 그 함수만 재정의한다. `src/` 본체는 고치지 않고, 기준선 `workspace/base_run/`은 재정의 0개다
status: Accepted
tags: [replacement-point, decoder, architecture]
date: 2026-08-07
commit: 0394b81 (시험장 사본에 포함)
source: _pm/DONE.md 2026-08-07 "논문 아이디어 교체 지점 구조 + Ideas/ 뼈대" 항목, src/decoder.py:40-46, 136-220, README.md:161-162, workspace/base_run/README.md:5-9, docs/profile/replacement_points.md:9-11, 24-39, docs/profile/constraints.md:28-29
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 논문 아이디어를 하나씩 적용할 때 모듈화 수준을 어디에 둘지 논의했다 (2026-08-07)
  - ㉡ 아이디어마다 본체 전체를 복사하면 본체 개선이 전파되지 않고, 디코더를 통째로 바꾸면 중복이 생긴다
- ㉯ 거부한 대안
  - ㉠ 아이디어마다 전 파일 복사
  - ㉡ 디코더 클래스 통짜 교체
- ㉰ 이유
  - ㉠ C++ 함수 단위로 자르면 실물 C++ 이식 지점과 1:1로 대응한다. 유효한 기법을 C++로 옮길 때 어느 함수를 고칠지가 바로 보인다
  - ㉡ 자식 클래스면 본체 변경이 자식에 자동 전파된다
  - ㉢ 기준선(당시 이름 vanilla)도 같은 틀의 한 항목으로 두자는 사용자 제안으로 reference 실험까지 한 구조로 통일했다
- ㉱ 결과로 생긴 규칙이나 비용
  - ㉠ 교체용 함수는 현재 6개다: `_is_edge_clear_iter`, `_column_order`, `_c2v_reconstruct`, `_vn_decide`, `_vnu_quantize`, `_cnu_update`. 각 docstring 첫 줄에 `[교체 지점: C++ 함수 대응]` 표지가 있다. 시그니처는 리팩토링에서도 불변이다
  - ㉡ `workspace/base_run/`에는 decoder.py를 두지 않는다. 재정의 0개가 "본체와 같다"는 보증이다
  - ㉢ `_cnu_update`는 받은 배열을 제자리에서 고친다 (반환값 미사용). 비정수 raw를 만드는 `_vnu_quantize` 재정의는 `_uniform_saturate`도 함께 재정의한다
  - ㉣ 새 상태 배열이 필요한 기법, iteration 구조를 바꾸는 기법, 채널 추가, 실제 인코딩은 교체 지점에 맞지 않고 본체 수정 범위가 정해져 있다 (docs/profile/replacement_points.md:33-39)
  - ㉤ 재정의 검증은 두 방향이다. 무효과 파라미터로 기준선과 수치 완전 일치, 유효 재정의로 수치가 달라짐
  - ㉥ 단계별 함수 7개(`_read_channel_input` 등)는 교체 지점이 아니다. 교체 지점 개수를 7개로 적은 이력 기록(2026-08-07 단계별 함수 추출 항목)은 현재 docstring의 6개와 다르다
- 날짜: 2026-08-07. 디코더 선택 방식은 2026-08-10에 registry에서 `DECODER_CLASS`로 바뀌었다

## 하위 링크

- [../tech/20260930_replacement-points-six.md](../tech/20260930_replacement-points-six.md): 교체 지점 6개의 시그니처, 입력 축, 지킬 경계
- [../assets/20260813_paper-idea-single-override-procedure.md](../assets/20260813_paper-idea-single-override-procedure.md): 논문 아이디어를 교체 지점 하나만 재정의해 붙이는 절차와 검증 두 방향
- [20260810_decoder-class-single-switch-registry-removed.md](20260810_decoder-class-single-switch-registry-removed.md): 자식 디코더를 주입하는 한 곳 `DECODER_CLASS`
- [../../docs/profile/replacement_points.md](../../docs/profile/replacement_points.md): 교체 지점 표, 지킬 경계, 맞지 않는 변경, 새 버전을 붙이는 절차
