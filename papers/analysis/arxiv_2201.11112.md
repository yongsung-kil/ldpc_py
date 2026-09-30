### arxiv:2201.11112v1 - A Number Theoretic Approach to Cycles in LDPC Codes (2022, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.431~0.978 |
| 부호length | 65~208 |
| 연판정 | 무관 |
| 핵심기여 | 순열행렬 기반 LDPC의 4/6/8-cycle 회피 조건을 Sidon(B2)-set 등 가법 정수론 개념과 등가로 연결 |
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
| 한계,주의 | 순수 girth 구성이론뿐, BER/디코더/HW 검증 전무하며 girth 상한이 12로 제한됨 |
| 추가확인 | 고정 순열 f의 여러 거듭제곱(non-circulant 포함)이 실제 QC 하드웨어 shift 구조와 정합되는지 |

> 총평: NAND ECC용 고rate QC-LDPC 부호 구성에 girth 조건을 정수론으로 다루지만, 이론에 그치고 girth≤12 제한·저rate 예제로 이식가치 낮음.

### B. 알고리즘 요약

1. 시스템/코드: 순열행렬 블록으로 이뤄진 `L×J` 블록 패리티행렬 `H`, 각 블록은 고정 순열 `f`의 거듭제곱 `f^{A_k i_l}` (QC-LDPC를 특수경우로 포함), 예제 rate 0.431~0.978 / length 65~208.
2. 문제: circulant permutation 기반 QC-LDPC는 girth·최소거리에 상한이 있어 반복복호 성능이 제한됨 → 더 큰 girth 구성이 필요.
3. 가정/모델: 채널·noise 모델 없음. 순전히 Tanner 그래프의 cycle 존재성을 대수적으로 다룸.
4. 핵심기법1: Fossorier의 cycle 판정(Thm 1)을 `f`의 거듭제곱 지수 집합 `I={0,i_1,..,i_r}`, `A={0,A_1,..}`에 대한 조건으로 재서술. 2k-cycle ⇔ 특정 지수합 `i=Σ(a·j)`에 대해 `f^i`가 fixed point를 가짐.
5. 핵심식 의미: `f`가 소수 order `m`인 m-cycle이면 `f^i`는 `i≡0 mod m`일 때만 fixed point → cycle 조건이 정수 지수합=0으로 환원.
6. 핵심기법2: 4-cycle 없음 ⇔ 모든 `t∈I∆`에서 `f^t` derangement (Thm 5); 8-cycle 없음 ⇔ `(I+)∆` 조건, 이는 `I`가 `B2(Sidon)-set`인 것과 등가 (Cor 2).
7. 구현 디테일: `L=2`이면 모든 `(4k+2)`-cycle(특히 6-cycle) 자동 부재, `I`가 B2-set이면 girth 12 달성. commuting 순열 사용 시 girth 상한은 12.
8. 최적화: 없음(학습/DE/GA 없음). 정수론 조건 만족하는 `I`, `m` 선택만.
9. 결과: 예) `I={0,1,4,6,13}`, `f=29-cycle`로 (145,88) girth-12 코드; irregular 확장(§6)으로 열블록 추가 시 rate를 1에 임의로 근접(예 rate 0.978)시키면서 cycle 구조 불변.
10. 한계: 이론뿐이며 BER 시뮬/디코더/HW 전무. commuting 순열 제약으로 girth≤12, 예제 코드가 짧고 저rate(0.43대)여서 NAND ECC급 고rate 실용성 미검증.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 순열행렬/거듭제곱 기반 H-matrix 구성 | ecc_top.cpp Load_PCM() | H-matrix 로드 지점이나, 순열-거듭제곱 구성은 Prime의 base+circulant shift와 상이 |
| girth/cycle 회피 부호설계 | 대응 없음 | Prime은 특정 QC-LDPC H가 고정, 부호설계 재구성은 이식난이도 최상(§4) |
| 디코더/양자화/조기종료 | 대응 없음 | 논문은 디코더·soft-info를 전혀 다루지 않음 |
```

적용 가치: **낮음** — 순수 girth 구성이론이고 디코더/HW/BER 검증이 없으며, Prime의 고정 QC-LDPC 부호를 재설계해야 하는 최고난이도 레이어에만 닿아 재검증 부담이 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:2201.11112v1",
  "title": "A Number Theoretic Approach to Cycles in LDPC Codes",
  "year": 2022,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "0.431~0.978",
  "code_length": "65~208",
  "soft_quant": "무관",
  "key_contribution": "순열행렬 기반 LDPC의 4/6/8-cycle 회피 조건을 Sidon(B2)-set 등 가법 정수론과 등가로 연결",
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
  "caveat": "순수 girth 구성이론뿐, BER/디코더/HW 검증 전무하며 girth 상한 12로 제한됨",
  "todo_check": "non-circulant 순열 거듭제곱 구성이 실제 QC HW shift 구조와 정합되는지"
}
```
