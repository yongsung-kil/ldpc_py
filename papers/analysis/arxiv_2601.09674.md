### arxiv:2601.09674v2 - Counting and Entropy Bounds for Structure-Avoiding Spatially-Coupled LDPC Constructions (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | CLLL로 4-cycle 등 구조회피 QC-SC-LDPC의 feasible (P,L) 설계공간 크기 하한 + MT 알고리즘 출력 다양성(Rényi 엔트로피) 하한 유도 |
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
| 한계,주의 | 순수 카운팅/엔트로피 이론(설계공간 크기만), 실제 부호·복호·HW·BER 없음, SC-LDPC 대상 |
| 추가확인 | 없음 (설계공간 존재성 정량화일 뿐 이식 대상 알고리즘 없음) |

> 총평: 구조회피 QC-SC-LDPC 설계공간의 크기·다양성을 CLLL/MT 엔트로피로 정량화한 순수 조합론적 이론으로, NAND binary QC-LDPC 부호/복호/HW에 떼어 쓸 실체가 없어 이식성 하.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 Type-I protograph 기반 QC-SC-LDPC 부호로, all-one `(γ,κ)` base matrix를 edge spreading(partition matrix `P`)과 Z-lifting(shift matrix `L`)으로 결합해 구성.
2. 문제: 큰 coupling memory에서 낮은 error floor를 얻으려면 short cycle 등 유해구조를 제거해야 하는데, 이런 제약을 만족하는 설계가 "몇 개나" 존재하는지 정량 하한이 없음.
3. 모델: cycle 활성화 조건을 protograph 단계 `sum P(ik,jk)=sum P(ik,jk+1)`와 lifting 후 `sum L ≡ sum L (mod Z)`(Lemma 1)로 국소화, 유해구조 회피를 CSP로 정식화(Proposition 1).
4. 핵심기법 1: 각 edge 변수 `Xi,j=(P(i,j),L(i,j))`에 non-uniform 분포를 두고 quantitative Clique LLL(CLLL)을 적용해 feasible `(P,L)` 쌍 개수의 명시적 하한 유도(Theorem 1).
5. 핵심식 의미: bad-event 확률이 dependency graph 조건을 만족하면 solution space가 `exp(Θ(γκ))`로 지수적으로 큼을 보장.
6. 핵심기법 2: row/column permutation 동치류로 quotient한 non-equivalent 해의 개수 하한(`#N ≥ ... / (γ!κ!)`, Theorem 2).
7. 핵심기법 3: Moser-Tardos(MT) resampling 출력분포 `DMT`의 Rényi 엔트로피 하한(Lemma 3~5)으로 MT가 낼 수 있는 서로 다른 해 개수 `#MT ≥ exp(Hα(DMT))` 하한 유도(Theorem 3).
8. 특수화: 4-cycle(C4) 제거에 대해 closed-form 하한(Corollary 3~5) 도출, 지배항은 `[Z(mt+1)]^{γκ}`에 degree 의존 penalty.
9. 결과: `(γ,κ)=(3,5)` 수치 예로 부등식 검증(Appendix E), MT를 CPO의 특수경우로 증명(Proposition 2)해 OO-CPO 설계의 잠재력을 이론적으로 뒷받침.
10. 한계: 전적으로 이론(counting/엔트로피 하한)만이며 구체 부호 생성·복호기·HW·BER/error-floor 실측이 없음, 대상도 SC-LDPC(WD 복호).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-SC-LDPC edge spreading / lifting 설계공간 카운팅 | 대응 없음 | Prime ECC는 block QC-LDPC(H 고정), SC-LDPC coupling·설계공간 탐색 미대응 |
| 4-cycle/유해구조 회피 CSP·CLLL 이론 | 대응 없음 | H-matrix는 `ecc_top.cpp` `Load_PCM()`로 고정 로드, 부호탐색 파이프라인 없음 |
| MT resampling 부호구성 알고리즘 | 대응 없음 | Prime ECC에 부호 자동설계/탐색 모듈 없음 |
```

적용 가치: **낮음** - 구조회피 QC-SC-LDPC 설계공간의 크기·다양성 정량화 이론으로, 특정 block QC-LDPC가 고정된 Prime ECC의 복호기·HW·부호로딩 어느 레이어에도 이식할 알고리즘 실체가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.09674v2",
  "title": "Counting and Entropy Bounds for Structure-Avoiding Spatially-Coupled LDPC Constructions",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "CLLL로 4-cycle 등 구조회피 QC-SC-LDPC의 feasible (P,L) 설계공간 크기 하한 + MT 알고리즘 출력 다양성(Rényi 엔트로피) 하한 유도",
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
  "caveat": "순수 카운팅/엔트로피 이론(설계공간 크기만), 실제 부호·복호·HW·BER 없음, SC-LDPC 대상",
  "todo_check": "없음 (설계공간 존재성 정량화일 뿐 이식 대상 알고리즘 없음)"
}
```
