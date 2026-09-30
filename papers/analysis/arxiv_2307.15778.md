### arxiv:2307.15778v2 - Spherical and Hyperbolic Toric Topology-Based Codes on Graph Embedding for Ising MRF Models: Classical and Quantum Topology Machine Learning (2023, arXiv cs.IT / early draft preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | QC-LDPC/trapping-set/Ising-topology를 ML(행렬 factorization·DNN 구조 등가)에 응용하는 code-on-graph 프레임 제시 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | ECC 복호/NAND 무관, Ising·quantum·DNN·화학까지 초광범위 early-draft로 실험은 square-matrix factorization(F-norm) 뿐 |
| 추가확인 | 재사용 가능 요소는 이미 보유한 PEG+ACE/SA+EMD trapping-set 회피 부호구성법(§3 이식난이도 높음)뿐, 신규 이식 가치 없음 |

> 총평: QC-LDPC/trapping set/Ising 토폴로지를 ML 임베딩·DNN·양자·화학에 연결하는 초광범위 이론 preprint로, NAND binary LDPC ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. QC-LDPC(`H` = circulant permutation matrix `P^k` 블록, exponent matrix `E(H)`, circulant size `L`)와 MET/protograph/multigraph 표현을 기본 부호 도구로 사용.
2. 풀려는 문제: Ising/Markov Random Field 바닥상태를 QC-LDPC parity-check matrix로 기술하고, 이를 ML의 저차원 임베딩·행렬 factorization·DNN 구조 해석에 연결하는 것(ECC 복호가 목적이 아님).
3. 핵심 개념: cycle이 얽혀 만드는 `TS(a,0)`(codeword, code distance `dmin=a`)와 `TS(a,b)`(pseudocodeword)로 error-floor·loss landscape·양자 바닥상태를 통합 기술.
4. 부호 품질 척도로 `EMD`(extrinsic message degree)와 그 근사 `ACE`를 사용, 최소 EMD를 키워 harmful trapping set을 제거(`harm=b/a`).
5. 부호 구성법: PEG+ACE와 Simulated Annealing+EMD로 short trapping set을 깨 QC-LDPC/MET QC-LDPC를 생성.
6. 복호는 marginalization(MAP/ML) 근사인 Belief Propagation으로 설명하며, 계산 어려운 sum-product 대신 normalized `min-sum`(고SNR/저온 Jacobian 근사)을 사용한다고 언급(§2460).
7. Information Geometry/Number Geometry lattice, KAM/FKAM 이론, gauge 대수, Bethe free energy·permanent로 trapping set·바닥상태 개수(=circulant 크기·automorphism)를 연결.
8. DNN 등가: ChordMixer/Mega/CDIL 등 long-range arena 구조를 Cage-graph/Repeat-Accumulate 등 (convolutional) LDPC 부호와 등가로 주장, QAOA depth `p`↔BP iteration 대응.
9. 실험: square matrix를 `M=log2 N`개의 sparse factor로 근사(SF 최적화, BFGS/fminunc), Hyperbolic Toric LDPC(PEG+ACE / QC-LDPC SA+EMD)가 F-norm에서 TSVD·SF-Chord를 다수 데이터셋(이미지·network·covariance)에서 능가(Table 1).
10. 한계: NAND/SSD·디코더 HW·BER/FER·throughput 수치 전무한 early-draft, 범위가 ECC 밖(ML/양자/화학)으로 광범위.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC(circulant `P^k`, exponent matrix) 부호구조 | `ecc_top.cpp` `Load_PCM()` | 우리도 QC-LDPC(base+shift)지만 논문은 부호를 ML 임베딩용으로 씀, 부호설계 이식은 §3 이식난이도 높음 |
| PEG+ACE / SA+EMD trapping-set 회피 부호구성 | 대응 없음 | Prime ECC는 H-matrix 고정, 부호구성 최적화 모듈 없음 |
| normalized min-sum BP 언급 | `decoder.cpp` `CNU_Update_New_Mag()` | 우리가 이미 보유(min1/min2), 신규성 없음 |
| Ising/DNN/tensor-network/quantum 등가 | 대응 없음 | ECC 복호·NAND HW와 무관 |

적용 가치: `낮음` - QC-LDPC와 trapping-set 용어를 공유하나 목적이 ML 임베딩·DNN·양자 이론이라, NAND binary LDPC 디코더/HW에 떼어 쓸 구체 기법이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2307.15778v2",
  "title": "Spherical and Hyperbolic Toric Topology-Based Codes on Graph Embedding for Ising MRF Models: Classical and Quantum Topology Machine Learning",
  "year": 2023,
  "venue": "arXiv cs.IT (early draft preprint)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "QC-LDPC/trapping-set/Ising-topology를 ML(행렬 factorization·DNN 구조 등가)에 응용하는 code-on-graph 프레임 제시",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "ECC 복호/NAND 무관, Ising·quantum·DNN·화학까지 초광범위 early-draft로 실험은 square-matrix factorization(F-norm) 뿐",
  "todo_check": "재사용 가능 요소는 이미 보유한 PEG+ACE/SA+EMD trapping-set 회피 부호구성법뿐, 신규 이식 가치 없음"
}
```
