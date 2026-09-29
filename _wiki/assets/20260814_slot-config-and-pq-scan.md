---
summary: 같은 delta를 스케일이 다른 환경 세 벌(headroom, balanced, real)의 슬롯 config에서 돌리고, (P,Q) 쌍 목록을 인자로 받는 scan 스크립트로 반복 실행하는 구조
type: pattern
tags: [config, scan, experiment-structure, environment]
date: 2026-08-14
last_verified: 2026-09-30
---

## 내용

이 사본에는 `workspace/minsum_dual_clip/`(scan.py, config 3종)과 `workspace/실험로그.md`가 없다. 아래 구조는 `_pm/DONE.md`(2026-08-13, 2026-08-14)와 태스크 문서 서술 기준이다.

- ㉮ 슬롯 config 3종 (실험 폴더 안)
  - ㉠ `config_headroom.json`: edge 상한 15, 균일 ch=8. ch가 edge 상한보다 작아 여유가 큰 환경. 무클립 붕괴와 클리핑 복구가 보인다
  - ㉡ `config_balanced.json`: edge 상한 15, ch=16. 비율을 되돌린 환경. 무클립 건강, 클리핑 사망
  - ㉢ `config_real.json`: 실물 H-matrix와 LLR 파일명 두 자리만 비워 둔 슬롯. 파일명을 채우면 즉시 실행
- ㉯ scan.py: config 경로와 (P,Q) 쌍 목록을 인자로 받아 쌍마다 실행한다. 처음엔 10쌍 고정이었고 2026-08-14에 인자로 일반화
- ㉰ 쌍 설계
  - ㉠ 무효과 쌍 (7,7): base_run과 수치 일치로 구현 동등성 확인
  - ㉡ P=Q 대조군 3쌍: 단일 상한 대 이중 상한 비교
  - ㉢ 같은 P에서 Q만 바꾸는 열과 같은 Q에서 P만 바꾸는 열: 축 분리
- ㉱ 결합: 같은 쌍 목록을 세 config에서 돌려 득실이 환경 의존임을 드러낸다
- ㉲ 결과 대조: 실행 폴더의 `fer_{label}.csv`와 `summary.txt` 결과 줄. 비교 스크립트는 없어 손으로 표를 만든다
- ㉳ 함께 둔 것: `workspace/실험로그.md`에 실험 환경과 인사이트를 상설 기록 (사용자 지시 2026-08-14)

## 사용 방법

- ㉮ 언제: 한 아이디어를 여러 환경과 파라미터 쌍에서 스캔할 때. 특히 득실이 채널 LLR 스케일 대비 edge 상한 여유에 좌우되는 delta
- ㉯ 어떻게: 실험 폴더에 환경별 config를 슬롯으로 두고, scan 스크립트가 config와 쌍 목록을 인자로 받게 한다. 무효과 쌍과 P=Q 대조군을 항상 넣는다. 통상 `edge_max_value`를 키우면 `channel_llr_*`도 같은 배율로 키우는데, headroom은 일부러 키우지 않은 환경이다
- ㉰ 주의: 이 사본에서는 변형 디코더를 실행할 경로가 없어(런처 폴더 이름, `-m` 경로 BaseDecoder 고정) 스캔을 그대로 재현하지 못한다. 균일 생성 config(`use_input_llr_matrix` false, `edge_quantization`, `channel_llr_HD`)로 headroom과 balanced 환경 자체는 `python -m src.run`으로 만들 수 있다
- 관련 문서
  - ㉠ [20260813_minsum-dual-clip-trial.md](../trials/20260813_minsum-dual-clip-trial.md)
  - ㉡ [20260813_config-slots-and-flags.md](../decisions/20260813_config-slots-and-flags.md)
  - ㉢ [20260813_edge-quantization-bits-max-split.md](../decisions/20260813_edge-quantization-bits-max-split.md)
  - ㉣ [20260807_flip-condition-ch-le-7dv.md](../tech/20260807_flip-condition-ch-le-7dv.md)
  - ㉤ [20260930_variant-decoder-run-path.md](../decisions/20260930_variant-decoder-run-path.md)
