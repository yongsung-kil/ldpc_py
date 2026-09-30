### arxiv:2503.01738v1 - Automorphism Ensemble Decoding of Quantum LDPC Codes (2025, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 양자코드 automorphism으로 syndrome을 변환한 병렬 BP 앙상블(AutDEC)로 Tanner graph short cycle 완화, BP-OSD-0급 정확도를 낮은 시간오버헤드로 달성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 양자 CSS 코드(QRM/Bivariate Bicycle) 타깃, automorphism·syndrome변환(UA)이 short-cycle 완화 목적이라 고rate NAND QC-LDPC엔 이득 불명 |
| 추가확인 | 앙상블 자체는 classical QC-LDPC에도 존재([24],[42]) — NAND용 BP 앙상블 효과는 별도 검증 필요 |

> 총평: 양자 LDPC용 automorphism 앙상블 BP 디코더로, 병렬 BP·조기종료 개선 아이디어는 흥미로우나 quantum Tanner short-cycle 특화·HW 미설계라 NAND binary QC-LDPC 이식성 하.

### B. 알고리즘 요약

1. 대상: 큰 automorphism 군을 갖는 양자 CSS 코드 (QRM `[[15,1,3]]`, Bivariate Bicycle `[[72,12,6]]`~`[[144,12,12]]`), code-capacity·circuit-level 잡음.
2. 문제: 양자 LDPC는 Tanner graph에 short cycle이 많아 BP가 자주 실패하고, OSD 등 후처리는 시간오버헤드(cubic)가 큼 → throughput/backlog 문제.
3. 핵심: 코드 automorphism `A`(부호 span 보존 permutation) 집합으로 syndrome을 변환(`s_A = U_A·s`, `U_A H_X = H_X A`)하고 각 변환 syndrome을 별도 BP 디코더에 병렬 투입.
4. 핵심식: `U_A H_X = H_X A` — permutation `A`가 유도하는 `r×r` 가역행렬 `U_A`가 check matrix·syndrome을 동시에 변환. 짧은 사이클이 다른 위치로 이동해 BP 수렴을 도움.
5. 후보 정렬: 수렴한 corrections 중 code-capacity는 최소무게, circuit-level은 DEM prior 확률로 가장 그럴듯한 정정 선택.
6. 병렬성: 앙상블 BP를 병렬 실행하므로 시간오버헤드는 단일 BP와 동일 (`AutBP-N`, N=5/17/36).
7. 구현: Bliss/igraph로 Tanner graph automorphism 계산(작은 코드는 code automorphism, 큰 코드는 check-matrix automorphism), min-sum scaling factor 1, parallel schedule.
8. 결과: QRM에서 BP는 threshold 없으나 AutBP-5는 threshold 확보 + BP+OSD급; BB `[[144,12,12]]`에서 AutBPOSD0가 OSD-0보다 동등~약간 우수.
9. Bivariate Bicycle DEM automorphism 탐색 시간: `[[72,12,6]]` 0.002s ~ `[[756,16,≤34]]` 0.139s (Apple M3).
10. 한계: proof-of-concept Python(순차 실행), HW/FPGA 미설계, 양자 코드·잡음모델 전용, classical binary LDPC/NAND 실험 전무.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 병렬 BP(min-sum) 앙상블 디코더 | decoder.cpp LDPC_Decoder() | min-sum은 공통이나 앙상블/automorphism 변환 계층은 우리 구조에 없음 |
| automorphism syndrome 변환(U_A) | 대응 없음 | quantum CSS short-cycle 완화용, 고정 고rate QC-LDPC H-matrix에 이득 불명 |
| 후보 정렬(최소무게/prior) | 대응 없음 | 앙상블 출력 선택 로직, 단일 디코더 파이프라인과 무관 |

적용 가치: 낮음 — 병렬 BP 앙상블 아이디어는 classical QC-LDPC에도 존재하나, 본 논문은 quantum Tanner short-cycle 완화에 특화되고 HW 미설계라 NAND binary QC-LDPC 디코더에 직접 떼어 쓸 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2503.01738v1",
  "title": "Automorphism Ensemble Decoding of Quantum LDPC Codes",
  "year": 2025,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "양자코드 automorphism으로 syndrome을 변환한 병렬 BP 앙상블(AutDEC)로 Tanner graph short cycle 완화, BP-OSD-0급 정확도를 낮은 시간오버헤드로 달성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "양자 CSS 코드(QRM/Bivariate Bicycle) 타깃, automorphism·syndrome변환(UA)이 short-cycle 완화 목적이라 고rate NAND QC-LDPC엔 이득 불명",
  "todo_check": "앙상블 자체는 classical QC-LDPC에도 존재([24],[42]) — NAND용 BP 앙상블 효과는 별도 검증 필요"
}
```
