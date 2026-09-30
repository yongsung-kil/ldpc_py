### arxiv:2605.23894v1 - A Two-Branch Finite-Field Construction for Regular CSS LDPC Bases (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.4 |
| 부호length | 10240 |
| 연판정 | 무관 |
| 핵심기여 | 유한체 위의 two-branch multiplicative-coset 구성으로 regular CSS(quantum) LDPC base matrix를 만들고 CPM lift로 girth≥8, 특정 weight-16 논리연산자 배제를 인증한 뒤 joint BP+후처리로 FER 측정 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | Quantum CSS(non-binary/두 개 sparse check matrix 쌍, commutation 제약) 코드로 binary classical LDPC와 근본적으로 다른 문제 설정이며, 순수 소프트웨어 시뮬레이션(디코더 iters=1000, damping 등)만 존재하고 HW 설계·NAND 타깃 언급 없음 |
| 추가확인 | girth 최적화(4-/6-cycle 제거) 및 유한체 기반 base matrix 구성 아이디어가 classical QC-LDPC H-matrix 설계에 참고 가치가 있는지 |

> 총평: Quantum LDPC(CSS) 코드의 대수적 base matrix 구성 및 girth 인증 논문으로, classical NAND binary LDPC와는 문제 설정이 근본적으로 달라 Prime ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. Quantum CSS 코드는 두 개의 sparse binary check matrix `H_X, H_Z`가 commutation 조건(`H_X H_Z^T=0`)을 만족해야 하며, 본 논문은 이를 만족하는 regular((J,L)-regular) base matrix를 유한체 위에서 구성한다.
2. 문제의식: 기존 quasi-cyclic/affine-permutation 등 CSS 구성법은 특정 (J,L) 조합에서 orthogonality와 short-cycle 회피를 동시에 만족시키기 어렵다. (예: column weight 3, row weight 10 조합)
3. 핵심 모델: 유한체 `F`의 곱셈 부분군 `M`의 translation을 이용한 two-branch(branch λ∈{0,1}) 배치 규칙(Definition 1)으로 `H_X, H_Z`의 nonzero 위치를 결정.
4. 핵심 기법 1단: coset 조건(Theorem 2, 3) - cross-branch coset 동일성으로 CSS orthogonality 보장, same-type coset 서로소 조건으로 4-cycle 배제.
5. 핵심 식 `L = 2|M|` (row weight는 부분군 크기의 2배), 유한 exhaustive search로 (J,L) 쌍마다 coefficient array `a^(λ), b^(λ)`를 탐색(Proposition 1).
6. 핵심 기법 2단(확장): CPM(circulant permutation matrix) lift 단계 - zero congruence(orthogonality 유지, Theorem 4) + nonzero congruence(6-cycle 비폐쇄, Theorem 5) + 특정 weight-16 논리연산자 배제(Theorem 6)를 동시에 만족하는 lift label 탐색(Section 2.7).
7. 구현 디테일: (3,10)-regular base를 F16 위에서 구성, 64-fold CPM lift로 `[[10240, 4108, 10≤d≤32]]` 코드 생성, 거리 하한은 weight 9 이하 완전 열거, 상한은 weight-32 명시적 논리연산자 witness로 인증.
8. 디코딩: joint log-domain BP(iters=1000, damping=0.3) + 결정론적 저복잡도 후처리 규칙(local linear solve, prefix-size search, syndrome-2 core repair 등, 후처리는 잔여 unsatisfied check 1~4개일 때만 exact/beam search).
9. 결과: depolarizing p=0.058, 1.8억 trial에서 BP+후처리 후 FER = 1.0×10^-7 (25건 실패 중 7건 후처리로 복구, 18건 잔존).
10. 한계: quantum CSS 전용(non-binary, 두 check matrix 쌍) 문제로 classical binary LDPC와 구조가 다르며, HW 미설계·순수 알고리즘/시뮬레이션 수준이고 다른 (J,L) 조합에 대한 lift/디코딩 실험은 future work로 남김.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 유한체 기반 CSS base matrix 구성 (H_X, H_Z) | `ecc_top.cpp` `Load_PCM()` | Prime ECC는 non-binary/CSS가 아닌 단일 binary QC-LDPC PCM 고정이라 직접 대응 안 됨 |
| girth 최적화(4-/6-cycle 배제), CPM lift | 대응 없음 | CSS commutation 제약 특유의 coset 조건으로 classical QC-LDPC lifting과 목적이 다름 |
| joint log-domain BP + 저복잡도 후처리 | `decoder.cpp` `LDPC_Decoder()` | 로그도메인 BP/후처리 개념 자체는 유사하나 quantum syndrome decoding 전용 규칙(local linear solve 등)이라 이식 난이도 높음 |
| non-binary/quantum LDPC 전반 | (대응 없음 예시) | 프로파일 §5에 명시된 "이식성 대체로 하" 대상 (non-binary LDPC 기법) |

적용 가치: **낮음** — Quantum CSS LDPC 특유의 commutation 제약과 non-binary/duplex 구조를 다루는 이론+시뮬레이션 논문으로, Prime ECC(binary QC-LDPC 고정, NAND 타깃)의 부호설계·디코더 레이어와 문제 설정 자체가 달라 이식 가치가 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.23894v1",
  "title": "A Two-Branch Finite-Field Construction for Regular CSS LDPC Bases",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": 0.4,
  "code_length": 10240,
  "soft_quant": "무관",
  "key_contribution": "유한체 two-branch multiplicative-coset 구성으로 regular CSS LDPC base matrix 생성, CPM lift로 girth≥8 및 weight-16 논리연산자 배제 인증, joint BP+후처리로 FER 1e-7 측정",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "Quantum CSS(non-binary, 두 check matrix 쌍) 코드로 binary classical LDPC와 문제 설정이 근본적으로 다르며 HW 설계나 NAND 타깃 언급 없음",
  "todo_check": "girth 최적화 및 유한체 기반 base matrix 구성 아이디어가 classical QC-LDPC H-matrix 설계에 참고 가치가 있는지"
}
```
