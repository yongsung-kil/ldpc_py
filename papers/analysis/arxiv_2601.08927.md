### arxiv:2601.08927v2 - Two-dimensional Entanglement-assisted Quantum Quasi-cyclic Low-density Parity-check Codes (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | p^4 (예: p=3 -> 81) |
| 연판정 | 무관 |
| 핵심기여 | 2-D QC-LDPC의 2g-cycle 존재조건 정리 + girth>4/>6 텐서적층 구성, 이를 기반으로 EA quantum LDPC 2계열 도출 |
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
| 한계,주의 | 순수 구성/이론(erasure만), 타깃은 TDMR/양자저장, binary NAND 복호성능·HW 무관 |
| 추가확인 | 없음 (NAND binary LDPC 이식 관점에서 활용 여지 없음) |

> 총평: 2-D 텐서적층 QC-LDPC의 girth 보장 이론 + EA 양자 LDPC 구성으로, NAND binary QC-LDPC 복호/HW에 떼어 쓸 요소가 없어 이식성 하.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 2-D 저장/전송(TDMR, 3D NAND 언급은 배경뿐)에서 2-D burst 오류·erasure를 다루는 2-D classical QC-LDPC와 이를 기반으로 한 2-D EA quantum LDPC 부호 구성.
2. 문제: 기존 2-D LDPC 구성은 girth 6에 한정되고 2g-cycle 일반 조건이 없으며, 양자 LDPC는 2-D burst erasure를 명시적으로 다루지 못함.
3. 모델: p×p×p 항등 텐서 `I3-D`와 세 축 순열연산자 `P,Q,R`(X/Y/Z-shift)로 permutation tensor를 정의, 이를 i,j,k 방향으로 적층해 parity-check tensor `H2-D` 구성.
4. 핵심기법 1: 임의 closed path의 2g-cycle 존재조건을 shift 함수 `a(i,j,k),b(i,j,k)`의 mod-p 합 조건으로 특성화(Theorem 1).
5. 핵심식 의미: `x=z+a (mod p)`, `y=z+b (mod p)`로 nonzero 위치를 표현, cycle 폐합 = 두 shift 차분합이 0 (mod p).
6. 핵심기법 2: p가 홀수 소수/합성수에 따라 shift (8)식으로 girth>4 두 계열 구성, generalized Behrend sequence로 girth>6 계열 추가(shift (22)식).
7. 랭크/rate: 레이어 내적(Lemma 4)으로 `gfrank = p^2+(w-1)(p^2-1)` 도출, 부호 파라미터 `[p^4,(p^2-w+1)(p^2-1)]`(Theorem 3).
8. 양자 확장: 위 2-D classical 부호로 EA quantum LDPC 2계열 구성 - 두 부호 사용 시 unassisted 그래프 4-cycle-free에 ebit 1개, 단일 부호 사용 시 자체 4-cycle-free([[p^4,...]] 파라미터).
9. 결과: 모든 계열이 최소 p×p burst erasure 정정능력 보유(순수 조합론적 보장), 성능 시뮬레이션·BER 곡선 없음.
10. 한계: 전적으로 이론(정리·증명)만이며 HW·복호기·양자 잡음 하 실측 없음, binary NAND soft-decision LDPC와 무관.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 2-D 텐서적층 QC 부호구성 | 대응 없음 | Prime ECC는 1-D binary QC-LDPC 고정, 2-D 텐서 구조 미대응 |
| EA quantum LDPC 구성 | 대응 없음 | 양자 부호, binary NAND ECC와 무관 |
| girth/2g-cycle 존재조건 이론 | 대응 없음 | H-matrix는 `ecc_top.cpp` `Load_PCM()`로 고정 로드, 재설계 대상 아님 |
| burst erasure 정정 | 대응 없음 | Prime ECC는 random/RBER 채널 대상, 2-D burst erasure 미대응 |
```

적용 가치: **낮음** - 2-D 텐서/양자 LDPC 순수 구성이론으로, NAND용 1-D binary QC-LDPC 복호기·HW·양자정정 어느 레이어에도 이식할 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.08927v2",
  "title": "Two-dimensional Entanglement-assisted Quantum Quasi-cyclic Low-density Parity-check Codes",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "p^4 (e.g. p=3 -> 81)",
  "soft_quant": "무관",
  "key_contribution": "2-D QC-LDPC의 2g-cycle 존재조건 정리 + girth>4/>6 텐서적층 구성, 이를 기반으로 EA quantum LDPC 2계열 도출",
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
  "caveat": "순수 구성/이론(erasure만), 타깃은 TDMR/양자저장, binary NAND 복호성능·HW 무관",
  "todo_check": "없음 (NAND binary LDPC 이식 관점에서 활용 여지 없음)"
}
```
