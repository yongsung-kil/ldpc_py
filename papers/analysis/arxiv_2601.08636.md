### arxiv:2601.08636v1 - Quantum CSS LDPC Codes based on Dyadic Matrices for Belief Propagation-based Decoding (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.47~0.57 |
| 부호length | 257~1025 |
| 연판정 | 무관 |
| 핵심기여 | dyadic matrix(DPM) 기반 affine 치환으로 girth-6 고전 QD-LDPC와, CAMEL 조건(H'_X(H'_Z)^T=1)을 만족하는 quantum CSS QLDPC를 함께 구성하여 length-4 cycle을 단일 변수노드에 집중시킴 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | quantum stabilizer CSS 부호(GF(4) quaternary BP, CAMEL 4-path ensemble decoder) 전용이며 고전 binary LDPC가 아니라 Prime ECC(NAND binary QC-LDPC)와 부호 체계 자체가 상이 |
| 추가확인 | dyadic matrix affine 구성법(girth-6 보장)이 quantum 맥락을 제거한 순수 고전 QD-LDPC로서 QC-LDPC 대비 어떤 이점이 있는지 미상(논문은 quantum 응용에 초점) |

> 총평: quantum error correction용 CSS QLDPC 부호의 대수적 구성(dyadic matrix)과 quaternary CAMEL 앙상블 디코더 논문으로, GF(4) 기반 quantum 특화 기법이라 NAND용 고전 binary QC-LDPC ECC(Prime ECC 3.1)에는 이식 불가.

### B. 알고리즘 요약

1. Quantum stabilizer 코드의 CSS 프레임워크: 두 고전 이진 부호 `C1, C2`의 PCM `H_X, H_Z`가 직교조건 `H_X H_Z^T=0`을 만족하면 quaternary(GF(4)) PCM `[ωH_X, ω̄H_Z]`로 결합.
2. 기존 CSS QLDPC는 `H_X`, `H_Z` 직교 제약 때문에 Tanner graph의 length-4 cycle 제거가 어렵고, 이는 quaternary BP 디코딩 성능(error-floor)을 저해.
3. CAMEL 프레임워크(선행연구[14])는 모든 불가피한 4-cycle을 단일 변수노드(마지막 컬럼)에 몰아넣고, 그 노드 값을 4갈래로 추측하는 앙상블 BP(4-path)로 우회.
4. 본 논문 핵심기법: dyadic permutation matrix(DPM) 기반 exponent matrix `P`를 affine 치환 `p_{u,j}=a_u λ_j + b_u`(서로 다른 곱셈계수 `a_u`)로 구성 — 고전 QD-LDPC는 이 방식만으로 girth 6 보장(Theorem 1).
5. `(a_u+a_v)`가 F_{2^ℓ}에서 역원을 가지므로 `j → p_{u,j}+p_{v,j}` 매핑이 bijective가 되어 length-4 cycle이 발생하지 않는다는 대수적 증명(Lemma 1, Theorem 1).
6. Quantum 확장: `H'_X`, `H'_Z`를 각각 다른 affine 계수 집합으로 구성해 CAMEL 조건 `H'_X(H'_Z)^T = 1_{r×r}`(모든 행쌍의 내적이 홀수=1)을 만족시킴(Theorem 2), 이후 all-one column을 붙여 CSS PCM 완성.
7. HW/구현 트릭 없음 — 순수 대수적 구성(코드설계) + 표준 quaternary sum-product BP(flooding schedule, 최대 15 iteration).
8. 최적화 절차: 유한체 F_16/F_32 상에서 곱셈군의 원소를 multiplier 집합으로 선택(설계적 규칙, 학습 없음).
9. 결과: 제안 코드 D1(n=257,k=121,R=0.47)은 CAMEL 디코딩 시 참조코드 C1(같은 rate군) 대비 우수한 LER, error-floor 억제가 genie-aided 디코딩과 근접; D2(n=1025,R=0.57)는 plain quaternary BP만으로도 error-floor 없이 waterfall 개선.
10. 한계: 순수 시뮬레이션(Monte Carlo, depolarizing channel)뿐이며 HW 구현 없음, quantum stabilizer 코드 전용이라 고전 binary NAND ECC에는 직접 적용 불가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Quantum CSS/quaternary(GF(4)) PCM 구조 | 대응 없음 | Prime ECC는 binary(GF(2)) LDPC 전용, quantum stabilizer 개념 자체가 없음 |
| CAMEL 4-path 앙상블 quaternary BP 디코더 | 대응 없음 | non-binary(GF(4)) 디코딩이라 Prime ECC min-sum 파이프라인과 무관 |
| Dyadic matrix affine girth-6 구성법 | `ecc_top.cpp` `Load_PCM()` | 순수 고전(비양자) 맥락으로 좁히면 girth-6 대수적 구성 아이디어 자체는 QC-LDPC H-matrix 설계 참고 가능하나, Prime ECC는 특정 QC-LDPC 고정이라 재검증 부담 큼(§4 "높음" 난이도) |
| 4-cycle을 단일 변수노드에 집중시키는 코드설계 | 대응 없음 | Prime ECC PCM은 이미 확정된 QC 구조이며 quantum 맥락의 cycle-concentration 전략은 이식 대상 아님 |

적용 가치: **낮음** — quantum error correction 전용 GF(4) CSS 부호/디코더로, NAND 고전 binary QC-LDPC ECC(Prime ECC 3.1)와 부호 체계·디코딩 도메인이 근본적으로 달라 이식 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.08636v1",
  "title": "Quantum CSS LDPC Codes based on Dyadic Matrices for Belief Propagation-based Decoding",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": "0.47~0.57",
  "code_length": "257~1025",
  "soft_quant": "무관",
  "key_contribution": "dyadic matrix 기반 affine 치환으로 girth-6 고전 QD-LDPC와 CAMEL 조건을 만족하는 quantum CSS QLDPC를 함께 구성해 length-4 cycle을 단일 변수노드에 집중",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "quantum stabilizer CSS 부호(GF(4) quaternary BP, CAMEL 앙상블 디코더) 전용이며 고전 binary LDPC가 아님",
  "todo_check": "dyadic matrix affine 구성법을 quantum 맥락 없이 순수 고전 QD-LDPC로 봤을 때 QC-LDPC 대비 이점이 있는지 미상"
}
```
