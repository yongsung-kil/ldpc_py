---
summary: 구 코드(2026-08-03 시점)에서 3-bit 내부 정밀도의 th와 ch 조합을 추정으로 튜닝해 6-bit 기준선과의 갭을 줄이려 했다
result: partial
tags: [precision, tuning, legacy, toy]
date: 2026-08-03
source:
  - _pm/DONE.md (2026-08-03 항목)
  - _pm/TODO.md (평가 대상 입력 파일 교체 항목)
adopted_as: decisions/20260730_input-files-external-supply
---

## 시도 내용

- ㉮ 시점: column_wise 스케줄 구현과 함께 진행한 3-bit internal precision(내부 정밀도) 튜닝 2차와 3차. 당시 코드는 DAO LLR_MATRIX 파일 경로 이전의 구 구조다
- ㉯ 방법: th(VNU 양자화 임계값) 조합과 ch(채널 LLR) 조합을 바꿔 가며 fixed_error 채널의 정정 한계(프레임당 에러 bit 수 E)를 비교. BF(bit flipping) 1-bit 구간도 시험
- ㉰ 기준선: 6-bit column_wise, E=380에서 0/512
- ㉱ 목표: 소실된 하드웨어 실값 없이 추정만으로 3-bit 갭을 좁히기

## 결과

- ㉮ 발견: 낮은 dv 열의 ch가 메시지 최대 레벨(7) 이상이면 그 열이 trapping된다. ch를 낮추면 해소
- ㉯ th 조합별 성격이 갈렸다. 한 조합은 E=300까지 클린(FER 1e-2)이지만 340에서 절벽, 다른 조합은 380까지 버티나 약 7% 잔여 floor
- ㉰ BF 1-bit 구간은 기준 디코더에서 무효과
- ㉱ 결론: 3-bit 잔여 갭은 소실된 하드웨어 TH와 CH 실값 없이는 추정 튜닝에 한계가 있다. 갭을 닫지 못했다
- ㉲ 이후: 2026-08-06 개정으로 DAO(decoder auto optimizer, 테이블 최적화 도구) 산출 LLR_MATRIX 파일 경로로 바뀌어 당시 튜닝값은 현행 코드와 무관하다
- 교훈:
  - ㉠ 튜닝 대상 값이 외부에서 오는 것이면 추정 튜닝은 파이프라인 확인 이상을 노리지 않는다
  - ㉡ 발견 ㉮는 반전 가능 조건 `ch <= 7*dv`로 일반화되어 LLR 최적화 제약으로 살아남았다 (2026-08-07 등재)

## 대안 선택 (있을 경우)

- ㉮ 평가 대상 H-matrix와 LLR 테이블을 외부 공급으로 받는 결정(2026-07-30)을 그대로 두고 추정 튜닝을 멈췄다. 저장소 파일은 toy로 두고 실물 반입 시 교체
- ㉯ 실값을 받으면 재검증 (TODO 잔류)
- 관련 문서
  - ㉠ [20260730_input-files-external-supply.md](../decisions/20260730_input-files-external-supply.md)
  - ㉡ [20260807_flip-condition-ch-le-7dv.md](../tech/20260807_flip-condition-ch-le-7dv.md)
