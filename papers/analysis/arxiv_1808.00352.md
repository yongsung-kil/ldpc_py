### arxiv:1808.00352v2 - Counting Short Cycles of (c,d)-Regular Bipartite Graphs (2018, arXiv cs.DM)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 스펙트럼+차수분포로 bi-regular Tanner 그래프의 길이 <2g 짧은 사이클 수를 닫힌형 공식으로 산출 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 조합론(사이클 카운팅) 논문 - 부호설계 툴로의 직접 사용법·성능 실험 없음, HW/복호 무관 |
| 추가확인 | g+2/g+4/g+6 사이클 공식이 실제 PEG/QC 부호설계에서 error-floor 예측에 유용한지 별도 검토 필요 |

> 총평: LDPC 부호설계의 이론적 기반(짧은 사이클 열거)이나 NAND binary QC-LDPC 디코더·HW 이식과는 무관한 순수 수학 논문으로 정독가치 낮음.

### B. 알고리즘 요약

1. 대상은 `(c,d)`-정규 이분 그래프 `Bc,d` (LDPC 부호의 Tanner 그래프), VN 차수 c·CN 차수 d, |U|=n, |V|=m.
2. 풀려는 문제: 길이 girth `g`보다 크고 `2g`보다 작은 짧은 사이클 수 `Ni`를 알고리즘 없이 닫힌형 공식으로 구하는 것 (짧은 사이클이 error performance를 좌우하므로).
3. 기반 항등식 `Ni = [Σ λi^j − Ωi − Ψi]/2i` (Theorem 2.3): 인접행렬 고유값 거듭제곱합에서 cycle-free walk 수 `Ωi`와 cycle 포함 닫힌보행 수 `Ψi`를 뺀다.
4. 핵심 기법: cycle 포함 닫힌보행(CWWC)을 초기정점이 사이클 안(`Φ`)/밖(`Λ`)인 경우로 분해하고, 각 walk를 유일한 서브보행 곱 `W=W0W1...Wi`로 표현.
5. 각 서브보행 길이를 `2sj`로 두고 partition `s0+...+si=k` 위 합으로 CWWC 개수를 표현 (Lemma 3.7, 4.5).
6. 필요한 재료 `bc,2k`, `tc,2k`(닫힌 cycle-free walk 수)는 선행연구 Blake-Lin[1]에서 이미 알려짐 → 본 논문 공식은 partition과 이 알려진 값만으로 결정.
7. 사이클 밖 초기정점의 경우 거리 `l` 별 정점 수 `|Nl(v0)|`를 차수 곱 `(c-2)(d-1)^⌈⌉(c-1)^⌊⌋` 등으로 세어 결합.
8. 결과로 `Ψg+2`, `Ψg+4`, `Ψg+6`의 명시적 다항식(c,d,Ng,Ng+2,Ng+4 함수)을 유도 (Theorem 4.10/4.11, Lemma 4.12~4.14).
9. 성능 수치·시뮬레이션 없음 - 선행 Dehghan-Banihashemi[4] 대비 "더 간단한 증명"이라는 정성적 기여만.
10. 한계: 순수 조합론 결과로 HW·복호 무설계, bi-regular(정규) 그래프 한정 - irregular/protograph 확장 미제시.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 짧은 사이클 열거 공식 (부호구조 분석) | 대응 없음 | 사이클 카운팅은 부호설계 사전분석 도구로, Prime ECC 코드베이스에 해당 모듈 없음 |
| Tanner 그래프 / H-matrix 구조 | ecc_top.cpp Load_PCM() | H-matrix 로드부와만 개념적 접점, 사이클 분석 기능은 미보유 |
```

적용 가치: **낮음** - 순수 수학(bi-regular 그래프 사이클 열거) 논문으로 NAND binary QC-LDPC 디코더/HW/부호설계 이식에 직접 사용할 코드·기법이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1808.00352v2",
  "title": "Counting Short Cycles of (c,d)-Regular Bipartite Graphs",
  "year": 2018,
  "venue": "arXiv cs.DM",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "스펙트럼+차수분포로 bi-regular Tanner 그래프의 길이 <2g 짧은 사이클 수를 닫힌형 공식으로 산출",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 조합론(사이클 카운팅) 논문 - 부호설계 툴로의 직접 사용법·성능 실험 없음, HW/복호 무관",
  "todo_check": "g+2/g+4/g+6 사이클 공식이 실제 PEG/QC 부호설계에서 error-floor 예측에 유용한지 별도 검토 필요"
}
```
