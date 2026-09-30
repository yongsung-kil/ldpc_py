### arxiv:2507.10185v1 - High Girth Spatially-Coupled LDPC Codes with Hierarchical Structure (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5~0.8 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | HQC(2단 lifting)+CRM으로 작은 lifting factor로 target girth 달성하는 QC SC-LDPC 구성 알고리즘 |
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
| 한계,주의 | SC-LDPC(convolutional) 전용 구성법, Prime ECC의 block QC-LDPC와 구조 상이, HW·복호성능 미검증 |
| 추가확인 | block HQC girth 최적화 부분만 떼어 고rate block QC-LDPC H-matrix 재구성에 쓸 수 있는지 |

> 총평: girth 최적화된 SC-LDPC 저복잡도 구성법으로 이론상 우수하나 spatially-coupled 구조가 Prime ECC의 block QC-LDPC와 달라 순수 부호설계 이식성은 낮음.

### B. 알고리즘 요약

1. 대상은 time-invariant QC SC-LDPC (regular `(dv,dc)`, `dv=3` 기준, design rate `rd=1-dv/dc` = 0.5~0.8), 복제 factor `L`·coupling width `w` 구조.
2. 문제: 짧은 cycle(작은 girth)이 error floor를 유발하나, 고rate SC 부호는 protograph가 크고 조밀해 girth 최적화 구성이 어려움.
3. 핵심 관찰: type-I QC 부호의 cycle은 다항식행렬 `H(x)`의 닫힌경로에서 `Σᵢ(-1)ⁱsᵢ ≡ 0 mod S` 조건으로 판정 가능.
4. SC 부호의 convolutional 주기성을 이용해 전체 `HSC` 대신 cycle relevant matrix(CRM) `HS[w,ℓ]`만 검사 → cycle 탐색을 국소화.
5. HQC(hierarchical QC): 2단 lifting으로 `H(x,y)` 이변수 다항식화, `Sy`(y-lifting)·`Sx`(x-lifting)로 분해해 cycle enumeration 지수적 감소.
6. cycle 조건이 `Σx≡0 mod Sx` 그리고 `Σy≡0 mod Sy` 이중 조건으로 분리됨 (식 아래 유도).
7. 최적화: 미지 exponent를 랜덤 초기화 후, x/y별 cost table `Ca,s = Σ wᵢNᵢ` (가중치 `w4=5³,w6=5²,w8=5,w10=1`)로 greedy 갱신 (Alg.1).
8. SC 구성 두 방식: Alg.2(block 구성 후 spread) vs Alg.3(CRM 기반 modified HQC) — Alg.3는 exponent 중복 multiplicity `κ` 고려하고 첫 replication만 순회.
9. 결과: Alg.3가 Alg.2 대비 lifting size `Smin`을 약 절반으로 감소, 고rate `rd=0.8` (3,15)/(4,20)에서 girth-10을 실용적 batch size(예 36880)로 달성; girth-10이 girth-6보다 BER 우수.
10. 한계: HW 미설계, 복호기·throughput·정정능력 정량 미검증, 성공이 확률적("try and check"), SC 부호 전용 구성법.

### C. Prime ECC 관련 모듈 핀포인트

대상이 code-design이므로 디코더 성능(C섹션 성능 카테고리)은 N/A. 부호구조 로드 관점의 대응만 기재.

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC 부호 H-matrix/protograph 구성·로드 | ecc_top.cpp `Load_PCM()` | Prime ECC는 특정 block QC-LDPC 고정, SC 구조 미지원이라 재검증 부담 큼 |
| 부호용 PCM 생성 (circulant/lifting) | encoder.cpp `Generate_PCM_encoding()` | circulant lifting 개념은 공유하나 dual-diagonal·block 구조와 상이 |
| SC convolutional 구조/CRM | 대응 없음 | Prime ECC는 spatially-coupled 미지원 |

적용 가치: **낮음** — SC-LDPC 전용 high-girth 구성법으로, block binary QC-LDPC로 고정된 Prime ECC에 그대로 이식 불가하며 부호 교체는 재검증 부담이 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:2507.10185v1",
  "title": "High Girth Spatially-Coupled LDPC Codes with Hierarchical Structure",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": "0.5~0.8",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "HQC(2단 lifting)+CRM으로 작은 lifting factor로 target girth 달성하는 QC SC-LDPC 구성 알고리즘",
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
  "caveat": "SC-LDPC(convolutional) 전용 구성법, Prime ECC의 block QC-LDPC와 구조 상이, HW·복호성능 미검증",
  "todo_check": "block HQC girth 최적화 부분만 떼어 고rate block QC-LDPC H-matrix 재구성에 쓸 수 있는지"
}
```
