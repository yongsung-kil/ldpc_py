---
summary: 논문 ieee:9496601의 min1/min2 이중 상한 클리핑을 `_c2v_reconstruct` 하나만 재정의해 붙이고 toy 환경에서 (P,Q) 쌍을 스캔했다
result: partial
tags: [min-sum, clipping, paper-idea, toy]
date: 2026-08-13
source:
  - _pm/done/20260813_minsum_dual_clip/20260813_minsum_dual_clip.md
  - _pm/DONE.md (2026-08-13, 2026-08-14 항목)
  - _pm/TODO.md (평가 대상 입력 파일 교체 항목)
adopted_as: (없음, 판정 보류)
---

## 시도 내용

- ㉮ 대상 논문: ieee:9496601 (IEEE TCAD 2022, NAND 플래시용 저비트폭 min-sum). CNU(check node unit, 검사 노드 연산부)에서 min1은 상한 P, min2는 상한 Q로 클리핑한다 (P <= Q <= 진폭 상한). 진폭 성장을 늦춰 error floor를 지연시킨다는 주장
- ㉯ 구현: 실험 폴더 `workspace/minsum_dual_clip/`의 `MinSumDualClipDecoder`. `BaseDecoder`를 상속하고 `_c2v_reconstruct`(C++ C2V_Cal 대응) 하나만 재정의. P와 Q는 클래스 속성 (사용자 확정 2026-08-13). `src/` 무변경
- ㉰ 클리핑 위치: 저장 상태(`_cnu_update`)가 아니라 읽기 시점(`_c2v_reconstruct`). 이유는 asset 문서 참조
- ㉱ 사전 검증: refactor 4건 직전 커밋을 worktree로 꺼내 `workspace/base_run/`(당시 이름 vanilla)과 수치 완전 일치 확인
- ㉲ 스캔: (P,Q) 10쌍과 P=Q 대조군 3쌍. (7,7)은 무효과 조건
- ㉳ 환경: z=256 예시 H-matrix, 3-bit 레벨 {7,5,3,1}, edge 상한 7, 저장소 toy LLR 파일 로드

## 결과

- ㉮ (7,7)은 base_run과 수치 완전 일치. 구현 동등성 검증
- ㉯ 원 toy 환경에서 유효 클리핑 전부 악화. P가 작을수록 단조 악화
- ㉰ 같은 P에서 Q를 키우면 일관 개선. "P<Q가 P=Q보다 낫다"는 논문의 구조 주장은 방향 재현
- ㉱ 원인 (2026-08-14 확정): dv 열의 최대 extrinsic `Q + (dv-1)*P`가 그 dv의 ch(채널 LLR)보다 작으면 반전 불능. toy 파일에서 지배 열 dv=4(ch=10)가 (2,3)에서 9로 사망, (2,5)는 11로 생존. dv별 에러 로그(`bit_err_by_dv`)로 직접 확인. dv=2(ch=28)는 무클립에서도 반전 불능(알려진 위반)이라 on/off 차이와 무관
- ㉲ 정정 경위: 2026-08-13 결론은 균일 생성 경로의 ch 값을 잘못 인용해 "ch <= P*dv"라고 적었다. 실험은 LLR 파일 로드 경로였고 dv별 ch가 달랐다. 사용자의 대안 가설 질문(H-matrix 품질, edge 양자화)에 실값으로 답하다 발견해 2026-08-14에 바로잡았다
- ㉳ 환경 대조 (2026-08-14): edge 상한 15에 균일 ch=8(headroom)이면 무클립이 붕괴(FER 1.0)하고 논문 가이드 (4,8)이 0/256으로 완전 복구. ch=16(balanced)으로 비율을 되돌리면 무클립이 건강하고 (4,8)은 사망
- ㉴ 판정: 조건부 유효. 클리핑 득실은 채널 LLR 스케일 대비 edge 상한 여유가 정한다. 실물 H-matrix와 LLR 반입 후 최종 판정 (관리처는 저장소 밖 `3_LDPC_ideas/001_minsum_dual_clip/`)
- ㉵ 한계: toy 상대 비교라 절대 성능 판단 불가. 논문 이득은 저비트폭 대형 부호의 error floor 영역에서 발현
- ㉶ 이 사본: `workspace/minsum_dual_clip/`과 `workspace/실험로그.md`가 없다. 수치와 구조는 태스크 문서와 DONE.md 서술 기준
- 교훈:
  - ㉠ 원인을 말할 때는 실행 폴더 summary.txt로 실험이 실제로 탄 LLR 경로를 확인하고 그 파일의 실값을 인용한다
  - ㉡ 증분 갱신 상태에 변형을 넣지 않고 읽기 시점에 건다
  - ㉢ 클리핑 계열 delta의 득실은 ch 대비 edge 상한 여유로 먼저 계산한다

## 대안 선택 (있을 경우)

- ㉮ config 통로 신설(checker 허용 키 확장과 setup 전달)은 별도 작업으로 미루고 P, Q를 클래스 속성으로 전달 (사용자 확정 2026-08-13)
- ㉯ 최종 판정은 실물 파라미터 교체 뒤로 보류
- 관련 문서
  - ㉠ [20260807_flip-condition-ch-le-7dv.md](../tech/20260807_flip-condition-ch-le-7dv.md) (반전 가능 조건과 사망 경계)
  - ㉡ [20260813_clip-at-reconstruct-not-stored-state.md](../assets/20260813_clip-at-reconstruct-not-stored-state.md)
  - ㉢ [20260814_slot-config-and-pq-scan.md](../assets/20260814_slot-config-and-pq-scan.md)
  - ㉣ [20260814_fix-misquoted-cause-with-logged-values.md](../assets/20260814_fix-misquoted-cause-with-logged-values.md)
  - ㉤ [20260813_paper-idea-single-override-procedure.md](../assets/20260813_paper-idea-single-override-procedure.md)
