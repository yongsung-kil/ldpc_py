### arxiv:1407.5364v1 - Quasi-Cyclic LDPC Codes based on Pre-Lifted Protographs (2014, IEEE Trans. Information Theory (submitted))

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.25~0.57 |
| 부호length | 54~7104 |
| 연판정 | 무관 |
| 핵심기여 | protograph를 두 단계(pre-lift m배 + circulant r배)로 리프팅해 QC-LDPC의 minimum distance/girth 상한을 기존 one-step circulant lifting보다 크게 높이는 구성법 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | HW 미설계, 순수 sum-product BPSK/AWGN 시뮬만 존재하며 encoder/decoder 구현 이슈는 다루지 않음 |
| 추가확인 | Prime ECC 3.1의 고정된 H-matrix(QC-LDPC base+circulant)를 이 pre-lifting 구성법으로 재설계할 실익(면적/검증 비용 대비 성능이득) 있는지 확인 필요 |

> 총평: 순수 부호설계(구성법) 논문으로 QC-LDPC의 minimum distance/girth 상한을 높여 error-floor·waterfall 성능을 동시에 개선하지만, HW/디코더 구현 이슈는 다루지 않아 이식 시 부호 재설계 비용이 큼.

### B. 알고리즘 요약

1. Protograph 기반 QC-LDPC 코드는 base matrix `B`를 circulant permutation으로 N배 리프팅해 만들며, 구현 효율은 좋지만 QC 서브앙상블은 minimum distance 상한이 `(nc+1)!`로 고정되는 한계가 있다.
2. 기존 one-step circulant lifting만으로는 girth/minimum distance를 늘리는 데 근본적 제약이 있어, 임의로 lifting factor `N`을 키워도 error floor가 수렴(한계 성능)하는 문제가 있다.
3. 채널/모델은 BPSK 변조 + AWGN, sum-product 메시지패싱 복호(최대 100 iteration, syndrome 기반 조기종료)로 가정한다.
4. 핵심 기법은 2단계 리프팅: 1단계 "pre-lifting"에서 protograph를 `m`배(작은 값) 커버해 `B↑m`을 만들고, 2단계에서 `r`배(큰 값) circulant 리프팅해 `H = (B↑m)↑r`을 구성한다.
5. `H`는 `mr×mr` circulant-block permutation matrix들로 구성되며, `B↑m`이 서로 commute하지 않는 쌍(strongly noncommutative)을 가지면 minimum distance 상한 `(nc+1)!`을 초과할 수 있다(Theorem 8).
6. 두 가지 설계 규칙 제시: Design Rule 1(pre-lifting 단계는 commuting/circulant permutation, 2단계 shift 파라미터로 non-commutative 유도), Design Rule 2(pre-lifting 단계에서부터 strongly noncommutative 쌍 포함).
7. girth 보장을 위해 특정 permutation 곱들이 fixed column을 갖지 않는 조건을 체크하며, pre-lifting을 쓰면 이 조건 개수가 크게 줄어든다(예: 42개→2~13개).
8. 코드 서치는 sieve 기법(동치 커버링 그래프 제거, 분리된 서브그래프 제거)으로 탐색공간을 축소한다(예: `18!`≈6.4×10^15 → `r^m`=81 수준).
9. 결과: (3,4)-regular 예제에서 pre-lifted 코드가 동일 length의 기존 QC Tanner 코드 대비 BER 10^-5에서 약 1dB 이상 SNR 이득, 큰 lifting factor에서도 error floor 미관측(10^-6까지).
10. 한계: HW 설계 전무, encoder 복잡도/실장 비용 미검토, 예제별 rate/length가 상이해 단일 대표값 확정 불가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| pre-lifted protograph 기반 QC-LDPC H-matrix 구성 | `ecc_top.cpp` `Load_PCM()` | 부호구조 자체를 교체해야 하므로 이식 난이도 최상, 기존 고정 H-matrix 재검증 부담 큼 |
| minimum distance/girth 상한 개선(error-floor 대책) | 대응 없음 | Prime ECC는 부호설계 모듈이 별도 최적화 도구가 아니라 고정 H-matrix 로더뿐이라 알고리즘적 대응 모듈 없음 |
| sum-product 메시지패싱 복호(시뮬 검증용) | `decoder.cpp` `LDPC_Decoder()` | Prime ECC는 min-sum만 구현하므로 sum-product 자체는 대응 없음, 다만 반복복호 루프 구조는 유사 |

> 적용 가치: 낮음 - 순수 이론적 부호 구성법으로 특정 QC-LDPC 부호(H-matrix)를 재설계해야 하므로 이미 고정된 Prime ECC H-matrix 구조에 이식 시 전면 재검증이 필요하고, HW/디코더 관점 기여가 없어 직접 적용 가치는 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:1407.5364v1",
  "title": "Quasi-Cyclic LDPC Codes based on Pre-Lifted Protographs",
  "year": 2014,
  "venue": "IEEE Trans. Information Theory (submitted)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.25~0.57",
  "code_length": "54~7104",
  "soft_quant": "무관",
  "key_contribution": "protograph를 두 단계(pre-lift m배 + circulant r배)로 리프팅해 QC-LDPC의 minimum distance/girth 상한을 기존 one-step circulant lifting보다 크게 높이는 구성법",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "HW 미설계, 순수 sum-product BPSK/AWGN 시뮬만 존재하며 encoder/decoder 구현 이슈는 다루지 않음",
  "todo_check": "Prime ECC 3.1의 고정된 H-matrix(QC-LDPC base+circulant)를 이 pre-lifting 구성법으로 재설계할 실익(면적/검증 비용 대비 성능이득) 있는지 확인 필요"
}
```
