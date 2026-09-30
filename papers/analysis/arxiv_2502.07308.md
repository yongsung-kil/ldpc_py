### arxiv:2502.07308v1 - Explicit Codes approaching Generalized Singleton Bound using Expanders (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 확장기(AEL) 기반 명시적 부호로 list decoding capacity·일반화 Singleton bound 달성, 부산물로 LDPC 부호 구성 |
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
| 한계,주의 | 순수 이론(list decoding·SoS), 알파벳 크기 2^(1/ε)^O(1)로 거대, binary NAND ECC와 무관 |
| 추가확인 | 없음 (구성이 대알파벳·비반복 SoS 디코더라 NAND binary QC-LDPC에 이식 대상 없음) |

> 총평: 확장기 기반 list-decodable 부호의 조합론적 구성/증명 논문으로, NAND binary QC-LDPC 파이프라인과 접점이 없어 이식성 하.

### B. 알고리즘 요약

1. `Cin`(내부, 상수크기)·`Cout`(외부, 고rate)·`(n,d,λ)-expander G`를 결합하는 Alon-Edmonds-Luby(AEL) 거리증폭을 일반화한 명시적 부호 구성.
2. 문제: 기존 capacity-achieving 명시 부호는 folded Reed-Solomon 등 대수적 구조(다항식 보간)에 의존 — 조합론적·명시적 대안이 없었다.
3. 핵심결과: AEL 절차가 "average-radius (ε-완화) generalized Singleton bound"를 local→global로 증폭 (`E[∆(g,h)] ≥ (|H|-1)/|H| · (1-R-ε)`).
4. `k=O(1/ε)`로 두면 반경 `1-R-ε`에서 list size `O(1/ε)`의 capacity-achieving 부호 획득.
5. 증명 도구: expander mixing lemma로 local 거리 부등식을 global 거리로 전달, 공통 오류위치를 erasure로 처리하는 귀납법.
6. 부산물: `Cout`를 LDPC로 잡으면 `CAEL`도 LDPC(패리티체크 크기 `2^(1/ε)^O(1)`) — 명시적 LDPC로 list decoding capacity 최초 달성.
7. 알고리즘: Sum-of-Squares(SoS) SDP 계층 + "proofs-to-algorithms"로 다항시간 결정론적 list decoder 구성.
8. SoS: 코드워드를 형식변수 `Z1..Zk`로 두고 average-distance 부등식을 sum-of-squares로 표현해 pseudocodeword의 존재/피복성 증명.
9. 결과(이론): 반경 `(k-1)/k·(1-R-ε)`에서 `n^{2(k^k/ε)^O(1)}` 시간, list size `≤ k-1`.
10. 한계: 알파벳 크기 `2^(1/ε)^O(1)`로 거대, binary가 아님, 반복 message-passing 디코더 없음, 실측/HW/시뮬 전무.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| AEL expander 기반 부호 구성 | 대응 없음 | 고알파벳 확장기 부호, binary QC-LDPC H-matrix 구조와 무관 |
| SoS/SDP list decoder | 대응 없음 | min-sum 반복복호와 원리 다름 |
| LDPC 부산물(패리티체크 크기) | 대응 없음 | 알파벳 `2^(1/ε)^O(1)`, non-binary·거대라 Load_PCM()에 적재 불가 |

적용 가치: 낮음 — 대알파벳·비반복 SoS 디코더 기반 이론 구성으로, NAND용 binary QC-LDPC(부호설계→min-sum 디코더→HW) 어느 레이어에도 떼어 쓸 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2502.07308v1",
  "title": "Explicit Codes approaching Generalized Singleton Bound using Expanders",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "확장기(AEL) 기반 명시적 부호로 list decoding capacity·일반화 Singleton bound 달성, 부산물로 LDPC 부호 구성",
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
  "caveat": "순수 이론(list decoding·SoS), 알파벳 크기 2^(1/ε)^O(1)로 거대, binary NAND ECC와 무관",
  "todo_check": "없음 (구성이 대알파벳·비반복 SoS 디코더라 NAND binary QC-LDPC에 이식 대상 없음)"
}
```
