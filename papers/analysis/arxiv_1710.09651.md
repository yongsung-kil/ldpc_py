### arxiv:1710.09651v2 - Protograph LDPC Codes with Block Thresholds: Extension to Degree-1 and Generalized Nodes (2018, arXiv cs.IT / draft)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.1~0.33 |
| 부호length | 5000~64800 |
| 연판정 | 무관 |
| 핵심기여 | degree-1/일반화 노드 허용 시 block-error threshold=bit-error threshold 조건 유도 및 저rate 근capacity 부호 설계 |
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
| 한계,주의 | 저rate(1/10~1/3) BEC/BIAWGN 통신용 이론 부호 - NAND 고rate ECC와 정반대, DGLDPC는 non-binary 성분부호 |
| 추가확인 | 없음 (부호구성·성분부호가 Prime ECC의 고정 binary QC-LDPC와 무관) |

> 총평: BEC/BIAWGN용 저rate protograph 부호의 block-error threshold 이론·구성 논문으로, NAND 고rate binary QC-LDPC ECC와 rate/구조/채널 모두 어긋나 이식가치 없음.

### B. 알고리즘 요약

1. 대상: BEC/BIAWGN 채널의 저rate(1/3~1/10) protograph LDPC/DGLDPC 부호를 near-capacity로 설계.
2. 문제: 기존 block-error threshold 조건(`[6]`)은 degree-1 변수노드를 금지해 저rate 부호에서 capacity와 큰 gap 발생(rate-1/8 protograph, gap 0.3).
3. 핵심: protograph density evolution에서 erasure 확률 `x^t`의 double-exponential 감소가 성립하는 edge 집합을 규명 -> block=bit threshold 등가 조건.
4. degree-1 노드 처리: `RED(G)` 서브그래프(E1=degree-1 edge, E2=degree-2 cycle을 재귀 제거)를 정의하고 `E_RED(G)=D_xy` (Theorem 1)로 double-exp 성립 edge 집합 확정.
5. 의미: 정보비트 노드 `V_I ⊂ V_D`이면 `P_B ≤ kO(exp(-βn^α))` -> blocklength 증가 시 block error 확률 0 수렴 (Theorem 2).
6. DGLDPC 확장: 성분부호 최소거리로 `E1v/E1c/E2` 정의(Lemma 3,4), degree-2 cycle 있어도 조건 성립 가능 -> 더 유연한 최적화.
7. 성분부호: 표준노드는 repetition/SPC, 일반화노드는 (7,4) Hamming 및 dual 등 선형부호 사용.
8. 최적화: differential evolution(mutation `M=B_r1+0.5(B_r2-B_r3)`, crossover pc=0.88, 최대 N=6000세대)으로 block-threshold 최대화, cyclic PEG로 lifting.
9. 결과: rate-1/8 BEC threshold 0.866(capacity gap 0.009), rate-1/3 BIAWGN blocklength 64800에서 5G/PBRL/AR4A 대비 우수 FER (5G 대비 0.1dB↑).
10. 한계: 순수 이론·시뮬(HW 미설계), 저rate 통신부호 대상, 5G/wiretap 응용 지향.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph/DGLDPC 부호구성·differential evolution 최적화 | ecc_top.cpp Load_PCM() (H-matrix 로드) | 대응 낮음 - Prime ECC는 고정 binary QC-LDPC, 저rate protograph 구성법 무관 |
| block-error threshold 조건(density evolution 이론) | 대응 없음 | 부호설계 이론일 뿐 디코더/HW에 닿지 않음 |
| DGLDPC 성분부호(일반화 노드, non-binary MAP) | 대응 없음 | Prime ECC는 binary min-sum 전용 |
```

적용 가치: 낮음 - 저rate BEC/BIAWGN 통신용 protograph threshold 이론으로 NAND 고rate binary QC-LDPC ECC와 rate·구조·채널이 모두 상이하다.

### D. JSON 블록

```json
{
  "id": "arxiv:1710.09651v2",
  "title": "Protograph LDPC Codes with Block Thresholds: Extension to Degree-1 and Generalized Nodes",
  "year": 2018,
  "venue": "arXiv cs.IT (draft)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": "0.1~0.33",
  "code_length": "5000~64800",
  "soft_quant": "무관",
  "key_contribution": "degree-1/일반화 노드 허용 시 block-error threshold=bit-error threshold 조건 유도 및 저rate 근capacity 부호 설계",
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
  "caveat": "저rate(1/10~1/3) BEC/BIAWGN 통신용 이론 부호 - NAND 고rate ECC와 정반대, DGLDPC는 non-binary 성분부호",
  "todo_check": "없음 (부호구성·성분부호가 Prime ECC의 고정 binary QC-LDPC와 무관)"
}
```
