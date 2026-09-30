### arxiv:2310.12657v1 - 4-Cycle Free Spatially Coupled LDPC Codes with an Explicit Construction (2023, arXiv preprint (cs.IT))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.485 |
| 부호length | 60000 |
| 연판정 | 무관 |
| 핵심기여 | good sequence로 최소 coupling width의 4-cycle free SC-LDPC를 명시적으로 구성 |
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
| 한계,주의 | 블록 QC-LDPC가 아닌 convolutional SC-LDPC + sliding window 디코딩 전제로 Prime ECC 구조와 이질적 |
| 추가확인 | SC-LDPC 자체를 채택할 계획이 없다면 이식 대상 아님, girth-6 수준 부호의 NAND 정정력 부족 여부 |

> 총평: NAND용 고정 블록 binary QC-LDPC와 계열이 다른 SC-LDPC 구성법이라 Prime ECC 이식 대상이 아니며, SW 디코딩 전제·girth-6 저rate 특성상 실이식 가치 낮음.

### B. 알고리즘 요약

1. 대상: 비음정수 행렬 `E`의 incidence matrix로 구성하는 **SC-LDPC (spatially coupled) convolutional 부호**, sliding window(SW) 디코딩용 (rate `~1-p/q`).
2. 문제: SC-LDPC는 coupling width `w`가 클수록 SW 디코딩 latency가 커지므로, girth-6(4-cycle free)를 만족하는 **최소 `w`** 구성이 과제; 기존 [5] 방식은 heuristic + check-and-flip이라 base matrix 커지면 비효율.
3. 모델: base matrix `B`를 `w+1`개 component matrix `B=ΣBi`로 분해해 PCM `H(L)` (블록 대각 convolutional 구조) 구성, `bi,j`=간선 수.
4. 기법1 (4-cycle 판정): `E`가 4-cycle free ⇔ 임의 `2×2` 부분행렬에서 `ei2,j1-ei1,j1 ≠ ei1,j2-ei2,j2` (Def 1), `I`가 구간이면 `H(E)` 4-cycle free ⇔ `E` 4-cycle free (Thm 3.1).
5. 핵심식 (good sequence): 수열 `a_n`이 `a_{n1-n2+n3}+a_{n1}-a_{n2}+a_{n3} ≠ 0` (`n2-n1<p, n3-n2<q`) 조건 만족 시, `e_{i,j}=a_{j-i+p}`로 두면 `E`가 자동으로 4-cycle free (Thm 3.3).
6. 기법2 (비연속 인덱스): `I`가 구간이 아닐 때는 representative block matrix `BR(E)`의 `2×2` 부분행렬 조건으로 4-cycle 판정 확장 (Thm 3.5).
7. 구현: back-tracking depth-first(Algorithm 1)로 최소 MOE(=coupling width `w`) good sequence 탐색.
8. 학습/최적화: 없음 (결정론적 조합 탐색), MOE 최소화가 최소 coupling width에 대응.
9. 결과: Table I에서 대부분 [8] Lemma 4의 최소 `w` 하한과 일치, [5]보다 `(p,q)=(5,10)`에서 우수; 예시로 `E`(4)를 `m=100` APM로 lift해 rate 0.485, length 60000 부호 생성, SW(`W=12,20`)/flooding 디코딩 BER에서 [5]의 QC SC-LDPC(girth 6,8) 대비 소폭 우수.
10. 한계: 순수 부호 구성법 — 디코더/HW 미설계, girth-6(4-cycle free) 수준만 보장, BER 곡선값 등 세부 수치는 그림에만 존재.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-LDPC PCM / base matrix 구성 | `ecc_top.cpp` `Load_PCM()` | 우리는 블록 binary QC-LDPC 고정, convolutional SC 구조 미지원이라 직접 대응 아님 |
| 4-cycle free 지수행렬 구성 (good sequence) | 대응 없음 | H-matrix 설계 오프라인 이론, 런타임 모듈 없음 |
| sliding window 디코딩 | 대응 없음 | Prime ECC는 블록 flooding/dual-update 디코더, SW 디코딩 미보유 |
| APM lifting | 대응 없음 | Prime ECC는 CPM(binary QC) 고정, APM 미사용 |

적용 가치: **낮음** — SC-LDPC convolutional 부호 + SW 디코딩이라는 다른 부호 계열의 구성법으로, 블록 binary QC-LDPC 고정인 Prime ECC에 떼어다 쓸 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2310.12657v1",
  "title": "4-Cycle Free Spatially Coupled LDPC Codes with an Explicit Construction",
  "year": 2023,
  "venue": "arXiv preprint (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": 0.485,
  "code_length": "60000",
  "soft_quant": "무관",
  "key_contribution": "good sequence로 최소 coupling width의 4-cycle free SC-LDPC를 명시적으로 구성",
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
  "caveat": "블록 QC-LDPC가 아닌 convolutional SC-LDPC + sliding window 디코딩 전제로 Prime ECC 구조와 이질적",
  "todo_check": "SC-LDPC 자체를 채택할 계획이 없다면 이식 대상 아님, girth-6 수준 부호의 NAND 정정력 부족 여부"
}
```
