### arxiv:1706.01703v1 - Analytical lower bounds for the size of elementary trapping sets of variable-regular LDPC codes with any girth and irregular ones with girth 8 (2017, arXiv/IEEE Trans. Commun. draft)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | girth·column weight(γ)만으로 (a,b) elementary trapping set 크기 하한을 해석적으로 유도 (탐색 불필요) |
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
| 한계,주의 | 순수 조합그래프 이론(Turan·extremal graph)으로 부호 구성·복호·HW 없음; 하한만 제공 |
| 추가확인 | Prime ECC의 특정 QC-LDPC(γ=17, z=32)에서 girth와 ETS 하한이 error-floor 검증에 실제로 유용한지 |

> 총평: variable-regular/irregular LDPC의 ETS 크기 하한을 girth·γ로 해석적으로 준 순수 이론 논문. error-floor 관련성은 있으나 구성·복호·HW 부재로 직접 이식성 낮음.

### B. 알고리즘 요약

1. 대상: binary variable-regular LDPC(column weight `γ`, row weight `λ`) 및 girth 8 irregular LDPC의 Tanner graph 구조 분석.
2. 문제: error floor의 주범인 elementary trapping set(ETS, check degree 1·2)의 최소 크기를 기존엔 exhaustive search로만 구함.
3. 모델: (a,b) ETS = 변수노드 `a`개, 홀수차 check `b`개. dominant ETS 조건 `b/a < 1`. ETS를 normal graph(만족 check를 edge로 치환)로 변환.
4. 핵심기법: normal graph에 degree-sum `b = aγ − 2|E|`와 extremal graph theory(Turan, triangle-free `|E| ≤ a²/4`)를 결합해 하한 유도.
5. 핵심식: girth 8 → normal graph는 triangle-free → `b/a = γ − a/2 < 1` → `a ≥ 2γ−1`, `b ≥ γ` (tight, `K_{γ-1,γ}` 구조로 증명).
6. 확장: irregular(min degree `δ`)는 regular γ=δ ETS에서 a−b 차이만큼 degree-1 check 추가로 하한 도출(column weight ⊂{2..6}).
7. 일반화: girth 10 → `a ≥ (γ−1)²+1` (γ=3→7, γ=4→12); girth `2(2k+1)`→ `a ≥ (γ−2)k+1`; girth `2(2k+2)`→ `a ≥ 2(γ−2)k+1`.
8. 학습/최적화: 없음(해석적 정리·증명뿐).
9. 결과: 문헌의 search 기반 γ=3,4,5 수치와 하한 일치, 존재/비존재 표(Table I~III) 제공. search 시작 크기로 활용 가능.
10. 한계: 부호 구성법·복호 알고리즘·HW·시뮬 전무. 하한값만 제공하여 실제 부호 설계는 별도.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| ETS/trapping set 크기 하한 (error-floor) | ecc_top.cpp `Load_PCM()` | H-matrix 설계 시 girth·γ로 최소 ETS 예측하는 참고 이론뿐 |
| girth·column weight 구조 분석 | `ecc_top.cpp` `Load_PCM()` | 우리 부호(γ=17, z=32)는 고정이라 하한 재계산 여지 낮음 |
| 수렴실패/error-floor 추적 | `corner.cpp` | 수렴실패 케이스가 ETS인지 개념적 연결뿐, 알고리즘 접점 없음 |
| 복호 알고리즘 | 대응 없음 | 논문에 복호/디코더 요소 자체 없음 |

적용 가치: **낮음** — girth와 column weight로 elementary trapping set 최소 크기를 준 순수 그래프이론 하한 논문이라 error-floor 개념 참고는 되지만, 부호 구성·복호·HW 요소가 없어 Prime ECC에 떼어 이식할 알고리즘이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1706.01703v1",
  "title": "Analytical lower bounds for the size of elementary trapping sets of variable-regular LDPC codes with any girth and irregular ones with girth 8",
  "year": 2017,
  "venue": "arXiv/IEEE Trans. Commun. draft",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": "미상",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "girth·column weight(γ)만으로 (a,b) elementary trapping set 크기 하한을 해석적으로 유도 (탐색 불필요)",
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
  "caveat": "순수 조합그래프 이론(Turan·extremal graph)으로 부호 구성·복호·HW 없음; 하한만 제공",
  "todo_check": "Prime ECC의 특정 QC-LDPC(γ=17, z=32)에서 girth와 ETS 하한이 error-floor 검증에 실제로 유용한지"
}
```
