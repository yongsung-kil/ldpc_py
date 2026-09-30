### arxiv:1405.3775v1 - Quasi Cyclic LDPC Codes Based on Finite Set Systems (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.2~0.7 |
| 부호length | 90~1200000 |
| 연판정 | 무관 |
| 핵심기여 | Finite Set System(FSS)과 "inevitable walk" 개념으로 QC-LDPC mother matrix의 최대 달성 가능 girth를 결정론적으로 산출하고, 큰 girth·임의 column-weight 분포를 갖는 QC-LDPC 코드를 구성하는 두 알고리즘 제시 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 조합론적 부호 구성법, HW/복잡도 언급 전무, AWGN+SPA(soft, tanh 기반) 시뮬만 존재하며 다양한 code rate가 예제별로 흩어져 특정 NAND rate 대응이 불명확 |
| 추가확인 | 이 구성법으로 나온 mother matrix가 Prime ECC의 base matrix(N_b=129, VN degree 17) 규모/구조와 호환 가능한지, girth 확대가 실제 error-floor 개선에 기여하는 정도는 별도 검증 필요 |

> 총평: girth 최대화를 위한 순수 조합론적 QC-LDPC 구성 이론으로, 특정 부호(H-matrix)를 새로 설계하는 데는 참고 가치가 있으나 디코더/HW와 무관하고 기존 고정 QC-LDPC를 쓰는 Prime ECC에 이식하려면 부호 재설계·재검증 부담이 크다.

### B. 알고리즘 요약

1. 대상: QC-LDPC 코드(m-circulant matrix, base matrix + circulant permutation matrix 구조), 다양한 rate(0.2~0.7대)·length(90~1,200,000) 예제로 성능 비교.
2. 문제: 기존 PEG 알고리즘은 짧은 길이에서 우수하지만 중·대형 길이에서 계산복잡도가 크고 실제 girth가 목표에 못 미칠 수 있으며, QC 구조가 아니라서 인코딩/디코딩 복잡도가 큼. 기존 geometric/cylinder-type column-weight-2 코드는 girth 대비 rate가 낮음.
3. 채널/모델: AWGN + BPSK, iterative Sum-Product Algorithm(SPA)으로 디코딩(HW 세부 미언급).
4. 핵심 기법: 유한집합계(V,B) 쌍을 정의(FSS(v,b,t))하고, 각 block에 shift sequence `S`를 부여해 QC-LDPC parity-check matrix `H`를 생성(FSS-code `C_{m,B,S}`). Block-structure graph(BSG)의 closed walk 개념으로 girth를 특성화.
5. 핵심 식/의미: "inevitable walk"(길이 ℓ, 임의의 m·S 값에 무관하게 항상 BSG에 존재하는 closed walk)를 정의하고, `Theorem 1`: `g(B) = 2ℓ`(ℓ = B 내 최단 inevitable walk 길이)로 최대 달성 가능 girth를 결정론적으로 계산 — 기존(Kim et al.)의 고비용 부분행렬 검사 없이 girth 상한을 효율적으로 산출.
6. 확장 기법: Method I(재귀적 FSS 확장, `g(B) ≥ 6g'`)과 Method II(원하는 column-weight 분포 K와 목표 girth 2g를 만족하는 (V,B)를 순차 탐색으로 직접 구성)의 두 알고리즘.
7. 구현 디테일: shift sequence 탐색 시 값이 큰 경우(특히 column-weight 2) exhaustive search가 지수적으로 비싸져 휴리스틱(랜덤 shift 선택)으로 대체.
8. 최적화 절차: 알고리즘 II의 계산복잡도는 `O(b(k-1)^(g/2-2)(r-1)^(g/2-3) m^(b(k-1)))` (다항식 in m, 지수적 in k,b) — 사실상 그리디 탐색/백트래킹.
9. 결과: girth 20/18 FSS 코드가 QPEG·random-like 코드 대비 우수, cylinder-type(girth 10,12) 대비 약 0.6dB 코딩이득. Column-weight-2 FSS 코드(girth≥24~32)가 동일 girth의 기존 geometric/cylinder-type 코드보다 높은 rate 달성.
10. 한계: 순수 부호 구성/이론 논문으로 HW 설계·게이트카운트·throughput 전혀 없음, 디코더는 표준 tanh-SPA만 사용(min-sum/HW 근사 없음), 코드 성능은 girth에만 초점(trapping set·특정 error-floor 메커니즘 분석 없음).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC mother matrix (H-matrix) 구성/girth 최적화 | `ecc_top.cpp` `Load_PCM()` | 특정 QC-LDPC H-matrix를 새로 설계하는 것으로, 기존 고정 PCM_b를 교체해야 하므로 이식 난이도 높음 |
| shift-sequence 설계 (circulant shift 값 결정) | `ecc_data.h` `PCM_b` (base+shift) | 구조적으로 대응되나 z_sb=32 규모/HCU 비대칭 col 구조와 정합 검증 필요 |
| 디코딩 알고리즘 (tanh-SPA) | 대응 없음 | 논문은 표준 SPA만 사용, Prime ECC의 Min-Sum HW 근사와 무관 |
```

적용 가치: 낮음 — 순수 조합론적 girth-최적화 부호 구성법으로 디코더/HW 개선과 무관하며, 이식하려면 Prime ECC의 고정 QC-LDPC H-matrix를 완전히 재설계·재검증해야 해 부담이 크다.

### D. JSON 블록

```json
{
  "id": "arxiv:1405.3775v1",
  "title": "Quasi Cyclic LDPC Codes Based on Finite Set Systems",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.2~0.7",
  "code_length": "90~1200000",
  "soft_quant": "무관",
  "key_contribution": "Finite Set System과 inevitable walk 개념으로 QC-LDPC mother matrix의 최대 girth를 결정론적으로 산출하고 대형 girth·임의 column-weight 분포 코드를 구성하는 두 알고리즘 제시",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 조합론적 부호 구성법, HW/복잡도 언급 전무, AWGN+SPA 시뮬만 존재하며 rate가 예제별로 흩어져 특정 NAND rate 대응 불명확",
  "todo_check": "이 구성법의 mother matrix가 Prime ECC base matrix(N_b=129, VN degree 17) 규모/구조와 호환 가능한지, girth 확대의 실제 error-floor 기여도는 별도 검증 필요"
}
```
