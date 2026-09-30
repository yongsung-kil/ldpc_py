### arxiv:2008.13470v1 - Construction of LDPC convolutional codes via difference triangle sets (2020, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | (n-k)/n(예제마다 다름, 미상) |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | difference triangle set(및 weak version)을 이용해 임의 유한체 F_q 상 (n,k,δ) LDPC convolutional code를 구성하고, free distance/컬럼거리 하한과 2ℓ-cycle FRC 회피용 체 크기 하한을 유도 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | non-binary(GF(q)) 구성법 순수 수학 이론이며 디코더·복호성능·HW 언급이 전혀 없음, binary NAND ECC와 무관 |
| 추가확인 | 없음 |

> 총평: 조합론적 difference triangle set을 이용한 non-binary LDPC convolutional code의 순수 구성법/사이클 회피 이론 논문으로, decoder/HW/NAND와 접점이 없어 이식 가치가 낮음.

### B. 알고리즘 요약

1. 대상은 임의 유한체 `F_q` 상의 (n,k,δ) LDPC convolutional code로, sliding parity-check matrix `H(z)=H0+H1z+...+Hµz^µ`의 (right) kernel로 정의됨(channel/NAND 특정 없음).
2. 풀려는 문제: LDPC block code와 달리 LDPC convolutional code에는 조합론적 구성법이 드물어, 임의 rate/field에서 girth·free distance를 보장하는 체계적 구성법이 부재.
3. 핵심 가정/모델: 채널·간섭 모델 없음(순수 부호 구성 이론); 대신 (N,M)-difference triangle set(DTS)과 weak version(wDTS)이라는 조합 객체를 정의.
4. 핵심 기법: `H`의 각 열 지지집합을 wDTS의 원소 `T_l`로 설정(`H̄_{i,l}=α^{il}` if `i∈T_l`), scope `m(T)`로부터 코드 차수 `µ=⌈m(T)/(n-k)⌉-1` 결정.
5. 핵심 식: `dfree(C)≥w̃+1`, `d^j_c(C)≥min(w_j,w̃)+1` — wDTS의 최소 차이값(scope)이 자유거리·컬럼거리 하한을 직접 결정.
6. 확장: FRC(full rank condition) 위반 2ℓ-cycle을 배제하기 위한 체 크기 하한 `q > 2(µ+1)(n-k)(ℓ-1)(k-1)-2(k-1)(ℓ-1)+1`(ℓ 홀수) 및 ℓ 짝수 케이스를 별도 유도.
7. 구현 디테일: primitive element `α`의 지수로 nonzero entry 값을 설정(Definition 3), 추가로 prime `P` 지수화로 조건을 완화하는 변형 구성(Definition 4) 제시.
8. 최적화 절차 없음(GA/NN/DE 없음) — 순수 대수적 증명(determinant 0 여부 분석)으로 조건 도출.
9. 결과는 수치 시뮬레이션이 아닌 예제 코드(예: (7,2,1)_q code가 임의 q에서 cycle-free, (6,2)_q code에서 girth≥12 위해 field size >4.7×10^8 필요 등) 이론적 파라미터 관계로 제시.
10. 한계: 전적으로 이론/구성법 논문으로 BP 디코더 시뮬레이션, BER, HW 설계가 전혀 없고 non-binary(GF(q)) 대상이라 binary NAND LDPC와 직접 연관 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| non-binary GF(q) H-matrix 구성(difference triangle set) | 대응 없음 | Prime ECC는 binary QC-LDPC 전용이라 GF(q) 비이진 구성법과 근본적으로 불일치 |
| convolutional(sliding) parity-check 구조 | 대응 없음 | Prime ECC는 block QC-LDPC이며 convolutional/sliding 구조 자체가 없음 |
| cycle/FRC(absorbing set) 회피 조건 | ecc_top.cpp `Load_PCM()` | H-matrix 설계 시 girth/absorbing set 고려라는 개념적 유사성만 있고, 실제 GF(q) 대수 조건은 binary QC 설계에 적용 불가 |

> 적용 가치: **낮음** — non-binary convolutional LDPC의 순수 조합론적 구성 이론으로, decoder/HW/NAND 요소가 전무하고 Prime ECC의 binary QC-LDPC block 구조와 근본적으로 다름.

### D. JSON 블록

```json
{
  "id": "arxiv:2008.13470v1",
  "title": "Construction of LDPC convolutional codes via difference triangle sets",
  "year": 2020,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "difference triangle set(및 weak version)을 이용해 임의 유한체 F_q 상 (n,k,δ) LDPC convolutional code를 구성하고, free distance/컬럼거리 하한과 2ℓ-cycle FRC 회피용 체 크기 하한을 유도",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "non-binary(GF(q)) 구성법 순수 수학 이론이며 디코더·복호성능·HW 언급이 전혀 없음, binary NAND ECC와 무관",
  "todo_check": "없음"
}
```
