### arxiv:1108.1572v1 - Optimal Rate for Irregular LDPC Codes in Binary Erasure Channel (2011, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.30~0.64 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | BEC에서 최적 rate irregular LDPC degree distribution 설계를, 이산화 없는 exact 반무한 제약을 SDP(LMI)로 재정식화해 다항시간 내점법으로 정확해 도출 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC(erasure) 전용 degree distribution 최적화 이론이며 unstructured irregular 대상, NAND용 고정 binary QC-LDPC 구조·AWGN/RBER와 정합되지 않음 |
| 추가확인 | (없음 - QC-LDPC/실채널 확장 여부는 논문에서 다루지 않음) |

> 총평: BEC 최적 rate irregular LDPC degree distribution의 SDP 정식화라는 순수 부호구성 최적화 논문으로, NAND binary QC-LDPC 디코더/HW 이식 관점에서 재사용할 요소가 없음.

### B. 알고리즘 요약

1. 대상 문제: BEC(erasure rate `ε`)에서 capacity에 근접하는 최적 rate irregular LDPC 앙상블의 variable-node degree distribution `λ(x)` 설계.
2. 풀려는 문제: 기존 방법(EOS/GA, Differential Evolution, LP 이산화)은 완화·근사·수렴 미보장으로 suboptimal → 완화 없이 정확해를 구하는 실용적·다항시간 방법 필요.
3. 핵심 제약: DE로부터의 zero-error 조건 `λ(1-ρ(1-x)) ≤ x/ε, ∀x∈[0,ε]`을 만족하며 rate 최대화(=`Σλ_i` 최대화).
4. 핵심 기법: 이 제약을 다항식 `P(x)=x-λ(1-ρ(1-εx)) ≥ 0, ∀x∈[0,1]` 형태로 보고, 비음성 다항식의 semidefinite representability를 이용해 LMI로 변환.
5. 핵심 식 의미: affine map `P(x)→(1+x²)^q P(x²/(1+x²))`로 `[0,1]` 구간 제약을 `x∈ℝ` 전역 비음성으로 옮겨 SDP 표현 가능하게 함(이산화 불필요 → exact).
6. 정리: 문제(5)가 `Π_l = Σ_{i+j=l} B_ij`, `B⪰0` 형태의 SDP와 동치(Theorem 1)임을 증명, Lemma 1로 `Π_t` 계수 유도.
7. 구현: SeDuMi/CVX 등 SDP 솔버 또는 내점법으로 다항시간 해결. Example로 `f(x)=ax²+bx+c≥0`을 SDP로 예시.
8. 학습/최적화: 별도 학습 없음 - 결정론적 볼록최적화(SDP interior-point).
9. 결과: 정규 check `ρ(x)=x^3~x^7`에 대해 `R=0.296~0.644`, capacity 대비 `δ=1-R/C≈0.035~0.048`; 기존 LP/DE 결과 대비 5개 기준(최대차수·rate·threshold·degree-2 비율·δ)에서 대체로 우수.
10. 한계: BEC erasure 채널 전용, 디코더/양자화/HW 없음, QC 구조 없는 unstructured irregular 앙상블, blocklength·구현 검증 없음(degree distribution 수치만).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BEC degree distribution SDP 최적화 | 대응 없음 | Prime ECC는 고정 binary QC-LDPC(base+circulant)이며 degree distribution 재설계·최적화 모듈 없음 |
| DE 기반 threshold 제약 | 대응 없음 | 부호설계 단계 이론 도구로 코드베이스 대응 없음 |
| irregular unstructured 앙상블 구성 | H-matrix 로드(ecc_top.cpp) | Prime ECC의 QC 구조·고정 H-matrix와 상이하여 직접 이식 불가 |

적용 가치: **낮음** — BEC 전용 degree distribution 최적화 이론이라 NAND용 고정 binary QC-LDPC 디코더/HW/양자화 어느 레이어에도 떼어 붙일 산출물이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1108.1572v1",
  "title": "Optimal Rate for Irregular LDPC Codes in Binary Erasure Channel",
  "year": 2011,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": "0.30~0.64",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "BEC에서 최적 rate irregular LDPC degree distribution 설계를, 이산화 없는 exact 반무한 제약을 SDP(LMI)로 재정식화해 다항시간 내점법으로 정확해 도출",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC(erasure) 전용 degree distribution 최적화 이론이며 unstructured irregular 대상, NAND용 고정 binary QC-LDPC 구조·AWGN/RBER와 정합되지 않음",
  "todo_check": "없음 - QC-LDPC/실채널 확장 여부는 논문에서 다루지 않음"
}
```
