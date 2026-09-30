### arxiv:2601.10170v1 - On Existence of Girth-8 QC-LDPC Code with Large Column Weight: Combining Mirror-sequence with Classification Modulo Ten (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.45~0.55 |
| 부호length | 2652~6708 |
| 연판정 | 미상 |
| 핵심기여 | mirror-sequence와 modulo-10 row-regrouping을 결합한 GCD 프레임워크로 column weight 7/8, girth-8 QC-LDPC를 기존보다 짧은 circulant size로 대수적 구성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 대수적 부호 구성법으로 특정 QC-LDPC 구조(column weight 7/8, girth-8) 고정, HW/디코더 설계 없음 |
| 추가확인 | 제시된 두 예제((2652,1195), (6708,2879))의 rate가 Prime ECC의 high-rate(~0.9)와 크게 달라 실이식 시 rate 재설계 필요 여부 |

> 총평: NAND ECC에 필요한 고rate 대역이 아닌 medium-rate(~0.5) 영역의 순수 대수적 girth-8 부호 구성법으로, Prime ECC 3.1에 직접 이식할 여지는 낮음.

### B. 알고리즘 요약

1. QC-LDPC 부호는 base matrix(exponent matrix `E`) + circulant shift로 구성되며, column weight `J`(=7 또는 8)와 임의의 row weight `L`에 대해 girth-8(4-cycle, 6-cycle 없음)을 대수적으로 보장하는 구성을 목표로 한다.
2. 기존 GCD 프레임워크는 column weight 5·6까지만 짧은 길이로 구성 가능했고, weight가 커질수록 기존 대수적 방법의 결과 길이가 지나치게 길어지는 문제가 있었다.
3. `mirror sequence` 개념(예: `M = [0, 4, L, L+8, 3L+4, 3L+12, 4L+8]`에서 `4+(4L+8) = L+(3L+12) = (L+8)+(3L+4)`처럼 항끼리 대칭 합을 이루는 정수열)을 도입해 exponent matrix `E = M^T · [0,1,...,L-1]`을 구성한다.
4. mod(L,10) 값에 따라 10가지 세부 구성(basic/derived construction)으로 분기하며, 각 triple `[0,a1,a2]`의 GCD indicator(`a2/gcd(a2,a1)`)가 `L` 이상임을 보여 4/6-cycle 부재를 증명한다(Lemma 1~13).
5. Consecutive Circulant Size(CCS) 하한: circulant size `P`가 특정 임계값 이상이면 girth-8이 항상 보장됨 (Theorem 1: J=7일 때 `P_LB=4(L-1)(L+5)+1`, Theorem 3: J=8일 때 `P_LB=4(L-1)(L+7)+1`) — 기존 최적 결과 대비 약 20% 개선.
6. 하한보다 작은 circulant size에서도 특정 닫힌식(`P = L(3L+4)` 등, Lemma 3~13)으로 girth-8을 구성할 수 있음을 증명해, 하한 대비 약 25% 더 작은 circulant size를 제공(Theorem 2, 4로 상한 `P_UB` 도출).
7. row-regrouping을 modulo 6에서 modulo 10으로 확장한 것이 이 논문의 핵심 트릭으로, 이를 통해 column weight 7·8까지 대수적 구성 범위를 확장했다.
8. 별도의 학습/최적화 절차는 없으며, "extensive random search and pattern induction"으로 10가지 구성 패턴을 먼저 찾은 뒤 이를 일반화된 정리로 증명하는 방식이다.
9. 결과: J=7, L=12 예제에서 동일 circulant size(221)일 때 기존 SYM 코드(girth 6) 대비 새 코드(girth 8)가 BER/BLER 모두 크게 개선; circulant size 559(둘 다 girth 8)에서도 새 코드가 SYM 대비 우수함.
10. 한계: 순수 부호 구성/존재성 증명 논문으로 디코더 알고리즘·HW 설계·양자화 등은 전혀 다루지 않으며, 시뮬레이션도 AWGN 채널 기반 BER/BLER 곡선(50 iteration, sum-product 추정)에 국한되고 rate가 0.45~0.55대로 NAND ECC의 고rate 영역과 거리가 있다.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Girth-8 (J,L)-regular QC-LDPC 부호 구성(exponent matrix 설계) | `ecc_top.cpp` `Load_PCM()` | 특정 H-matrix 대수 구성법으로, 현재 고정 QC-LDPC 구조 교체는 재검증 부담이 커 이식 난이도 높음 |
| Column weight 7/8 부호 성능(BER/BLER) | 대응 없음 | Prime ECC 구조(VN degree 17, z_sb=32)와 column weight·구조가 상이해 직접 대응 모듈 없음 |
| 디코더/HW/양자화 | 대응 없음 | 논문에서 전혀 다루지 않음 |

적용 가치: 낮음 — 순수 대수적 girth-8 QC-LDPC 구성법이며 medium-rate(~0.5) 영역 예제뿐이라 Prime ECC의 고rate 고정 QC-LDPC 구조에 바로 이식하기 어렵고, 디코더/HW 요소도 전혀 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.10170v1",
  "title": "On Existence of Girth-8 QC-LDPC Code with Large Column Weight: Combining Mirror-sequence with Classification Modulo Ten",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.45~0.55",
  "code_length": "2652~6708",
  "soft_quant": "미상",
  "key_contribution": "mirror-sequence와 modulo-10 row-regrouping을 결합한 GCD 프레임워크로 column weight 7/8, girth-8 QC-LDPC를 기존보다 짧은 circulant size로 대수적 구성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 대수적 부호 구성법으로 특정 QC-LDPC 구조(column weight 7/8, girth-8) 고정, HW/디코더 설계 없음",
  "todo_check": "제시된 두 예제((2652,1195), (6708,2879))의 rate가 Prime ECC의 high-rate(~0.9)와 크게 달라 실이식 시 rate 재설계 필요 여부"
}
```
