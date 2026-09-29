---
summary: 균일 n-bit 양자화의 VNU 출력 레벨은 0을 두지 않고 최소 1인 포화형 `[top..2,1,1]`이다 (크기 = `max(min(|raw|, top), 1)`)
status: Accepted
tags: [quantization, uniform, vnu]
date: 2026-08-09
commit: 0394b81 (시험장 사본에 포함)
source: _pm/tasks/20260808_review/종합보고.md:25-39, 104; _pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md:204-234; src/llr_matrix.py:51-57; src/decoder.py:189-195
supersedes: (없음)
---

## 맥락, 대안, 이유

- ㉮ 맥락
  - ㉠ 처음 구현한 균일 모드는 레벨 0을 포함한 `[top..0]`이었다. 2026-08-08 딥 리뷰가 레벨 0 하나에서 세 증상이 나온다고 밝혔다
  - ㉡ 공명 붕괴: ch가 top과 같으면 iteration 1에서 합이 정확히 0이 되어 레벨 0으로 살아남고 CN을 침묵시켜 FER 1.0으로 붕괴하는데 경고가 없다. 인접 값은 정상이라 스윕 중 함정이다
  - ㉢ min1 점유: 크기 0 메시지가 `<=` 비교로 항상 min1 자리를 차지해 워터폴에서 FER가 1.2~1.9배 나빠졌다
  - ㉣ 부호 소실: `sgn * 0`이 `-0.0`이 되어 부호 판정이 양수로 읽고 CSW 계열 로그 전 행이 틀렸다
  - ㉤ 로더 제약: 레벨 개수 = th 개수 + 1. 파일 포맷과 커밋된 파일을 그대로 두고 고칠 안이 필요했다
- ㉯ 거부한 대안
  - ㉠ 레벨 0 유지
  - ㉡ 원 처방 `[top..1]`: 로더 제약에 걸려 즉시 ValueError
  - ㉢ th `[top..2]`, edge_mag `[top..1]`: 기존 파일이 선언 범위를 넘는 크기로 읽힌다
  - ㉣ C++ 4-bit 매핑을 문자 그대로 옮긴 `[top+1..1]` (크기 = `min(|raw|, top) + 1`): 상한이 1 커지고 FER 미측정
- ㉰ 이유
  - ㉠ C++도 C2V 크기 0을 내보내지 않는다 (내부 V 도메인 0을 EDGE 도메인 1로 복원). 하한을 1로 막는 방향이 같다
  - ㉡ 포화형은 포맷 불변이고 커밋 파일 재생성이 필요 없으며, 공명과 min1 점유를 동시에 없앤다. FER 1.0이 나오던 공명 조건에서 개선을 실측했다
- ㉱ 결과로 생긴 규칙
  - ㉠ `uniform_edge_mag(top) = [top, ..., 2, 1] + [1]`. 마지막 두 항이 1인 것은 레벨 개수 제약 때문이다 (`src/llr_matrix.py:51-57`)
  - ㉡ 균일 레벨은 O(1) 등가식 `_uniform_saturate`로 계산한다. 정수 raw에서만 캐스케이드와 같으므로 비정수 raw를 만드는 재정의는 이 함수도 함께 재정의한다 (`src/decoder.py:189-195`)
  - ㉢ `-0.0` 문제가 원천 소멸해 signbit 처방은 불필요해졌다
  - ㉣ 2026-08-13 레벨 분리 뒤 간격 2 이상 배치에서는 최소 레벨이 `step-1`이다

## 하위 링크

- [../assets/20260808_zero-level-not-in-original](../assets/20260808_zero-level-not-in-original.md): 원본에 없는 값 도입이 만든 세 증상의 상세
- [../tech/20260930_vnu-quantize-cascade](../tech/20260930_vnu-quantize-cascade.md): 캐스케이드와 균일 등가식의 현행 코드
- [20260813_edge-quantization-bits-max-split](20260813_edge-quantization-bits-max-split.md): 간격 2 이상 배치에서의 최소 레벨
