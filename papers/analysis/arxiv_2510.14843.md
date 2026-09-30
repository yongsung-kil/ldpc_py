### arxiv:2510.14843v1 - Rate-Adaptive Spatially Coupled MacKay-Neal Codes with Thresholds Close to Capacity (2025, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0~1 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 외부 DM 파라미터 ω만 바꿔 전 rate 구간에서 SC MN 부호로 capacity 0.15 dB 이내 threshold 달성 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 비선형 outer(DM) 결합·nonsystematic 인코더 구조로 NAND binary QC-LDPC와 이질적, 순수 asymptotic DE threshold 분석뿐 (유한길이·HW 없음) |
| 추가확인 | rate adaptation을 DM이 아니라 부호 자체로 하는 NAND 시나리오와의 정합성, 유한 lifting에서의 error-floor |

> 총평: capacity 근접 rate-adaptive 구성의 이론적 우수성은 크나, 비선형 DM+nonsystematic SC LDPC 구조라 NAND binary QC-LDPC ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. 시스템: 외부 비선형 DM(constant-composition CC 부호) + 내부 nonsystematic protograph SC-LDPC 부호를 연접, biAWGN 채널로 전송하는 MacKay-Neal(MN) 구조.
2. 문제: 기존 block-LDPC 기반 MN 부호는 전 rate 구간에서 Shannon limit 대비 약 1 dB gap. rate 적응을 위해 부호 puncturing/shortening 없이 넓은 rate를 얻고 싶음.
3. 핵심 아이디어: 내부 부호를 (2)형 base matrix의 regular protograph SC-LDPC로 교체하여 SC의 threshold saturation·universality를 활용, 전 rate에서 capacity 근접.
4. rate 적응: DM 파라미터 ω(fractional Hamming weight)만 조정 → 전체 rate `R = R_O R_I`가 `Hb(ω)`로 수렴, `ω∈[0,1/2]`로 `R∈[0,1]` 전 구간 span. 내부 부호는 고정.
5. 비선형성 우회: i.i.d. bit scrambler 도입으로 all-zero codeword 가정을 회복, 성능이 등가 parallel channel(EPC) 모델의 선형 부호 분석으로 환원.
6. EPC 모델: a-priori 채널(A, cross-over ω인 BSC) + communication 채널(C, biAWGN) 병렬, 미전송 punctured VN=채널-A, 전송 VN=채널-C에 연결. rate-1/2 한계 `hA+hC ≤ 1`.
7. threshold 계산: (3,6)·(4,8) regular SC 앙상블에 대해 BEC-BEC, biAWGN-biAWGN은 PEXIT(가우시안 근사), BSC-biAWGN은 quantized DE(1023 양자화 레벨)로 `(h*A,h*C)` 산출.
8. 핵심 관찰: BSC를 biAWGN로 근사해도 threshold가 거의 일치 → 단일 파라미터 PEXIT만으로 신뢰성 있는 추정 가능.
9. 결과: (3,6)·(4,8) SC MN 앙상블 모두 전 rate에서 capacity 0.7 dB 이내, (4,8)은 최대 gap ≈0.15 dB (기존 block MN의 ≈1 dB 대폭 개선).
10. 한계: asymptotic(L→∞, ℓ→∞) DE threshold 분석뿐, 유한길이 성능·복호 iteration·HW 구현·error-floor 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph SC-LDPC 부호 구성 / base matrix | ecc_top.cpp `Load_PCM()` | 우리는 고정 binary QC-LDPC이므로 SC 구조·비선형 MN은 직접 대응 없음(재검증 부담 큼) |
| DM 기반 rate 적응(외부 비선형 부호) | 대응 없음 | Prime ECC는 부호 고정 rate, 외부 DM 개념 없음 |
| BP threshold DE/PEXIT 분석 | 대응 없음 | 알고리즘 아닌 이론 분석 도구, 코드베이스에 상응 모듈 없음 |
| punctured VN prior 초기화(`ln[(1-ω)/ω]`) | channel.cpp `Set_LLR_Th()` (개념적 유사) | LLR 초기화라는 형식만 유사, MN 특유의 DM prior라 그대로 이식 불가 |

적용 가치: **낮음** — 비선형 DM + nonsystematic SC-LDPC 기반 rate-adaptive MN 부호로, NAND binary QC-LDPC 디코더/HW/부호구조 어느 레이어에도 떼어 붙일 수 없고 순수 asymptotic 이론 분석에 그침.

### D. JSON 블록

```json
{
  "id": "arxiv:2510.14843v1",
  "title": "Rate-Adaptive Spatially Coupled MacKay-Neal Codes with Thresholds Close to Capacity",
  "year": 2025,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "외부 DM 파라미터 ω만 바꿔 전 rate 구간에서 SC MN 부호로 capacity 0.15 dB 이내 threshold 달성",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "비선형 outer(DM) 결합·nonsystematic 인코더 구조로 NAND binary QC-LDPC와 이질적, 순수 asymptotic DE threshold 분석뿐",
  "todo_check": "rate adaptation을 DM이 아니라 부호 자체로 하는 NAND 시나리오와의 정합성, 유한 lifting에서의 error-floor"
}
```
