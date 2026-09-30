### arxiv:1604.05256v1 - Check-hybrid GLDPC Codes: Systematic Elimination of Trapping Sets and Guaranteed Error Correction Capability (2016, arXiv/ISIT-계열)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.9034 |
| 부호length | 미상 |
| 연판정 | hard-1bit |
| 핵심기여 | trapping set의 critical check를 2-error 정정 super check로 치환해 error-floor 제거·보증정정능력(최대5) 확보 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | GLDPC super check 도입으로 rate 급감(0.9034→0.61/0.32), BSC·PBF/Gallager-B(경판정)만 분석, min-sum·soft 미검증 |
| 추가확인 | 우리 고정 QC-LDPC의 지배 trapping set에 splitting-number 기법 적용 시 실제 error-floor·rate 트레이드오프 |

> 총평: trapping set 지식을 이용해 최소 super check 치환으로 error-floor를 구조적으로 제거하는 부호설계 논문 — 아이디어(critical set/splitting number)는 우리 QC-LDPC error-floor 보증 설계에 참고 가치 있으나 큰 rate 손실과 경판정 BSC 한정이 걸림돌.

### B. 알고리즘 요약

1. 대상은 BSC 상 column-weight 3인 `(3,ρ,8)` 및 column-weight 4인 `(4,ρ,6)` (QC 포함) 정칙 LDPC를 global code로 쓰는 CH-GLDPC.
2. 문제: iterative 디코더(PBF/Gallager-B)의 error-floor를 유발하는 소형 trapping set을 구조적으로 제거하되 rate 손실 최소화.
3. 모델: all-zero codeword 송신 가정, BSC, elementary trapping set `T(a,b)` (degree-1 CN b개, 나머지 degree-2)를 분석 단위로.
4. 핵심기법: trapping set의 일부 single parity check(critical check)를 2-error 정정 component code의 super check로 치환 → super check가 두 개의 독립 degree-1 check처럼 동작해 cycle을 끊음.
5. 핵심개념: critical set의 최소크기 = splitting number `s(a,b)(H)`; super check 1개가 최대 2개 flip만 보내는 BDD 성질이 trapping set 무해화의 근거.
6. 확장: subdivision 개념으로 cycle 수가 같은 파생 trapping set은 splitting number 동일(`s(a+1,b+1)=s(a,b)`)임을 이용해 계산 절감.
7. 상계: permutation-based `(3,ρ,8)`에서 모든 elementary TS 제거에 `s(a,b)(H)≤2p`, `T(5,3)/T(7,3)`은 `≤p`, girth-12 조건 시 `T(4,4)`도 `≤p`.
8. 보증정정: VN당 super check 2개(CI)면 PBF가 최대 5-error 정정(크기 6 반례 존재); VN당 1개(CII)면 원 LDPC 수준(1-error). `(4,ρ,6)`는 super check 3개면 최소 3-error.
9. 결과: `(3,31,8)` rate 0.9034 부호에 BCH(31,21) super check를 VN당 1개면 실제 rate 0.6130, 2개면 0.3236 (rate 손실 큼). 결과는 Gallager-B로도 동일하게 일반화.
10. 한계: 이론적 보증정정만 제시(BER 시뮬/HW 없음), BSC·경판정(PBF/Gallager-B) 한정, super check 도입에 따른 rate 급감.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| critical set/super check로 trapping set 제거 (H 설계) | ecc_top.cpp `Load_PCM()` + H-matrix | error-floor 보증 설계 아이디어 — 우리 고정 QC-LDPC PCM 재설계에 참고(단 super check 도입은 구조 큰 변경) |
| 보증정정능력(5-error)·fixed set 분석 | ecc_top.cpp `Load_PCM()` | 부호 error-floor 특성 평가에 이론 근거 제공 |
| PBF/Gallager-B 경판정 디코딩 | 대응 없음 | 우리는 min-sum BP(soft) 기반, PBF/Gallager-B 미사용 |
| GLDPC super check(component BCH) 디코딩 | 대응 없음 | 단일 binary QC-LDPC 구조로 component-code super check 미지원 |

적용 가치: **중간** — trapping set을 구조적으로 없애 error-floor를 보증하는 설계 관점은 우리 고rate QC-LDPC 부호설계에 참고 가치가 있으나, GLDPC super check 도입에 따른 큰 rate 손실과 경판정 BSC 한정으로 직접 이식은 부담.

### D. JSON 블록

```json
{
  "id": "arxiv:1604.05256v1",
  "title": "Check-hybrid GLDPC Codes: Systematic Elimination of Trapping Sets and Guaranteed Error Correction Capability",
  "year": 2016,
  "venue": "arXiv (cs.IT)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": 0.9034,
  "code_length": "미상",
  "soft_quant": "hard-1bit",
  "key_contribution": "trapping set의 critical check를 2-error 정정 super check로 치환해 error-floor 제거·보증정정능력(최대5) 확보",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "GLDPC super check 도입으로 rate 급감(0.9034→0.61/0.32), BSC·PBF/Gallager-B(경판정)만 분석, min-sum·soft 미검증",
  "todo_check": "우리 고정 QC-LDPC의 지배 trapping set에 splitting-number 기법 적용 시 실제 error-floor·rate 트레이드오프"
}
```
