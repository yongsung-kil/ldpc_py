### arxiv:1004.5217v1 - Analysis of Quasi-Cyclic LDPC codes under ML decoding over the erasure channel (2010, arXiv/ISIT-class preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.667 |
| 부호length | 3000~60000 |
| 연판정 | 무관 |
| 핵심기여 | QC 구조 행/열 치환으로 pseudo-band 변환 → ML(GE) 복호 복잡도를 O(k√k)로 축소 |
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
| 한계,주의 | BEC(패킷 소실) 전용 ML/Gaussian elimination 기법 — NAND의 BSC/AWGN·min-sum 반복복호와 채널·복호 모델이 다름 |
| 추가확인 | 없음(이식 무관); band 변환 아이디어가 QC-LDPC 인코딩 GE에 재활용 가능한지 정도만 |

> 총평: BEC 상 QC-LDPC의 ML 복호 복잡도 축소 부호설계 논문. NAND binary LDPC(연판정 min-sum) 이식성 거의 없음.

### B. 알고리즘 요약

1. 대상: 이진 소실채널(BEC) AL-FEC용 QC-LDPC, base matrix 5×15, rate `R=2/3`, 소스노드 degree 5의 RRA(staircase) 구조, 확장인자 `z`로 길이 가변.
2. 문제: 유한 길이 LDPC에서 IT(반복) 복호보다 ML 복호가 정정능력 우수하나, GE(Gaussian Elimination) 기반 ML 복호가 `O(k^2)`로 비쌈.
3. 핵심 관찰: QC 행렬 `H`(circulant shift)는 행/열 단순 치환으로 "숨은" pseudo-band 구조가 드러난다.
4. 치환식: `i=xi·z+yi`, `j=xj·z+yj` → `i'=xi+yi·a`, `j'=xj+yj·b`로 재배치, 결과 band 폭 `p=a(M+1)`, `q=b(M+1)` (`M`=base 최대 shift값).
5. 의미: band 폭이 좁을수록(=`M`이 `z`보다 작을수록) FE/BS 각 단계가 `O(q)`로 줄어 전체 `O((2q+b)m)` — 비구조 대비 `m/(2q+b)`배 이득.
6. 부호설계: band 폭이 `z`에 따라 스케일하도록 `M=C·zR/b`로 설정(Studholme-Blake 추정: 폭 `~2√k`면 full-rank 확률 유지) → ML 복잡도 `O(k√k)`.
7. degree-1 열 회피: staircase 마지막 원소를 다시 z×z staircase로 확장.
8. 실험: base matrix 고정, non-negative 항 무작위 선택으로 band/unconstrained/constant-band/protograph 4개 앙상블 비교, 500회 평균.
9. 결과: band QC-LDPC가 ML 하에서 이상부호 대비 오버헤드 0.5%(정정능력 unconstrained와 근접)이면서 복잡도만 `O(k√k)`로 축소. error-floor는 10^-5(실용상 충분).
10. 한계: BEC 전용, HW 미설계(순수 복잡도 이론+시뮬), 반복복호(min-sum) 성능 개선 아님.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC base+circulant 부호구조 | ecc_top.cpp `Load_PCM()` | 표면적으로만 동일(QC-LDPC) — 대상 채널·복호가 달라 실이식 무관 |
| ML(GE) pseudo-band 복호 | 대응 없음 | Prime ECC는 min-sum 반복복호만, GE/ML 소실복호기 없음 |
| RRA staircase 인코딩 | encoder.cpp `LDPC_encoder_4KB()` | Prime ECC는 dual-diagonal — staircase와 유사하나 이식 이득 없음 |

적용 가치: **낮음** — BEC용 ML 복호 복잡도 축소는 NAND(BSC/AWGN, soft min-sum 반복복호) 파이프라인과 채널·복호 모델이 근본적으로 달라 이식 대상 아님.

### D. JSON 블록

```json
{
  "id": "arxiv:1004.5217v1",
  "title": "Analysis of Quasi-Cyclic LDPC codes under ML decoding over the erasure channel",
  "year": 2010,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": 0.667,
  "code_length": "3000~60000",
  "soft_quant": "무관",
  "key_contribution": "QC 구조 행/열 치환으로 pseudo-band 변환하여 ML(GE) 복호 복잡도를 O(k√k)로 축소",
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
  "caveat": "BEC(패킷 소실) 전용 ML/GE 기법 — NAND의 BSC/AWGN·min-sum 반복복호와 채널·복호 모델이 다름",
  "todo_check": "band 변환 아이디어를 QC-LDPC 인코딩 GE에 재활용 가능한지 정도만"
}
```
