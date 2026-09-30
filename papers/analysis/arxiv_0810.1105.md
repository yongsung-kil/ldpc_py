### arxiv:0810.1105v1 - Low-Density Parity-Check Codes Which Can Correct Three Errors Under Iterative Decoding (2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 504~816 |
| 연판정 | hard-1bit |
| 핵심기여 | column-weight-3/4 부호가 hard-decision MP로 3개 오류를 정정하기 위한 필요충분(트래핑셋/expansion 회피) 조건과 이를 만족하는 수정 PEG 구성법 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 중 |
| 한계,주의 | γ=3/4 regular·rate-0.5·hard-decision(Gallager-A/B) 전용, 3개 오류만 보증 - 고rate QC-LDPC min-sum에 조건이 직접 적용 안됨 |
| 추가확인 | 고 column-weight QC-LDPC + min-sum soft에서 유사 트래핑셋 회피 조건 유도 가능성, 구성 시간 복잡도 |

> 총평: 트래핑셋/expansion 회피로 유한 오류 정정을 보증하는 부호설계 방법론(error-floor 직결). 방향은 NAND error-floor에 유의미하나 구체 조건이 저 column-weight·저rate·hard-decision 한정이라 고rate QC-LDPC min-sum에 직접 이식 불가.

### B. 알고리즘 요약

1. 대상: `(γ,ρ)`-regular binary LDPC, hard-decision message-passing(Gallager-A/B), BSC/AWGN 고SNR error-floor 문제.
2. 문제: 유한길이 LDPC의 error-floor는 저중량 uncorrectable 오류패턴(트래핑셋)에서 발생 - 보증된 오류정정능력을 부호설계로 확보 필요.
3. 핵심 정의: `(a,b)` 트래핑셋, critical number `ξ`(디코더가 그 트래핑셋에 빠지기 위한 최소 초기오류수).
4. col-weight-3 결과: girth 8이고 `(5,3)`·`(8,0)` 트래핑셋(및 `(3,3)`=6-cycle)을 포함하지 않으면 Gallager-A로 임의 3개 오류 정정 보증(Theorem 3).
5. 증명 방식: 3개 오류변수가 유도하는 5가지 부그래프를 하나씩 분석해 반복마다 메시지 전파를 추적, 유효 코드워드 수렴 확인.
6. col-weight-4 결과: girth 6에서 `4→11, 5→12, 6→14, 7→16, 8→18` expansion 조건 만족 시 4회 반복 내 3개 오류 정정(iff, Theorem 4).
7. 구성법: 수정 PEG(Algorithm 1) - 트리를 depth 6까지 확장해 후보 check 중 `(5,3)` 트래핑셋을 만들지 않는 최소차수 check에 연결. weight-8 codeword는 사후 edge swap로 제거.
8. FER 기울기 이론: 최소 critical number `i`인 부호의 log-FER 기울기 ≈ `i`, 즉 3개 정정(critical number≥4) 부호는 저 `α`에서 기울기 4로 급강하.
9. 결과: col-weight-3 `(504,252)` rate-0.5 부호는 14개 `(5,3)` 트래핑셋을 가진 동길이 PEG 부호보다 저 `α`에서 우수. col-weight-4 length-816 부호는 25회 반복 시 최소 오류패턴 weight 7, FER 기울기 8.
10. 한계: HW 미설계, hard-decision 한정, 저 column-weight(3/4)·rate 0.5, col-weight-4 필요충분조건은 length에 지수적 구성시간(4→12 완화 사용).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 트래핑셋 회피 부호설계(수정 PEG, H-matrix 구성) | `ecc_top.cpp` `Load_PCM()` | 우리 H-matrix 설계/재검증 지점에 대응하나 QC-LDPC 고정·고column-weight라 조건 이식 난이도 높음 |
| hard-decision message-passing(Gallager-A/B) 디코딩 | `decoder.cpp` `LDPC_Decoder()` | 우리는 min-sum soft라 디코딩 알고리즘 상이 - 직접 대응 아님 |
| 트래핑셋/critical number 기반 error-floor 수렴실패 분석 | `corner.cpp` (수렴실패 추적) | 수렴실패 케이스 추적 관점에서 개념적 대응 |
| FER 기울기 = 최소 critical number 이론 | 대응 없음 | 코드에 대응 모듈 없음(설계 지표) |

적용 가치: **낮음** - error-floor/트래핑셋 회피라는 주제는 NAND에 유의미하나, 구체 조건이 column-weight-3/4·rate-0.5·hard-decision Gallager 전용이라 고rate·고degree QC-LDPC min-sum 엔진에 직접 이식할 수 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:0810.1105v1",
  "title": "Low-Density Parity-Check Codes Which Can Correct Three Errors Under Iterative Decoding",
  "year": 2008,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "504~816",
  "soft_quant": "hard-1bit",
  "key_contribution": "column-weight-3/4 부호가 hard-decision MP로 3개 오류를 정정하기 위한 필요충분(트래핑셋/expansion 회피) 조건과 이를 만족하는 수정 PEG 구성법",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "중",
  "caveat": "γ=3/4 regular·rate-0.5·hard-decision(Gallager-A/B) 전용, 3개 오류만 보증 - 고rate QC-LDPC min-sum에 조건이 직접 적용 안됨",
  "todo_check": "고 column-weight QC-LDPC + min-sum soft에서 유사 트래핑셋 회피 조건 유도 가능성, 구성 시간 복잡도"
}
```
