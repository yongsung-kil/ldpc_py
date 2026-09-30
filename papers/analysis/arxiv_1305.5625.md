### arxiv:1305.5625v2 - Memory Efficient Quasi-Cyclic Spatially Coupled LDPC Codes (2013, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | SC-LDPC |
| 부호rate | 0.488 |
| 부호length | 103200 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 주기적 time-variant QC 구성으로 SC-LDPC 회로(circulant)를 재사용(reuse-T)하여 파리티체크 행렬 저장 메모리(BRAM)를 대폭 절감하면서 girth/BER 성능을 유지하는 구성법 제안 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상(등록/LUT/슬라이스 수치는 표에 있으나 공정 미표기) |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | BI-AWGN 채널·sum-product(soft) 디코더 기준 시뮬레이션이며, reuse-1/2는 girth 저하로 성능이 나쁘고 reuse-3만 유효; NAND용 QC-LDPC(짧은 length, 상대적으로 정형화된 H-matrix)와 달리 SC-LDPC는 매우 긴 코드(100K+)를 전제로 함 |
| 추가확인 | reuse-3 QC SC-LDPC의 성능 유지 결과가 hard-decision/저비트 soft-read(NAND read) 환경에서도 유지되는지, 그리고 Prime ECC의 고정 QC-LDPC(non-SC) 구조에 SC 방식 자체를 도입할 실익이 있는지 확인 필요 |

> 총평: SC-LDPC 특유의 circulant 재사용을 통한 메모리 절감형 부호 구성법 + FPGA 검증이나, 매우 긴 코드 길이·SC 구조 전제로 NAND 이식은 부호설계 레벨의 재작업이 필요.

### B. 알고리즘 요약

1. (dl, dr)-regular LDPC 프로토그래프를 L번 연결한 SC-LDPC 체인을 기반으로, 각 circulant 위치를 QC(quasi-cyclic) 방식으로 구성하는 `(dl, dr, L)` SC-LDPC 코드 (`N = nb*M*L`, `r = [nbL - nc(L+dl-1)]/(nbL)`).
2. 기존 대형 SC-LDPC(길이 100K+)는 H-matrix 저장에 BRAM이 많이 필요한 것이 HW 구현의 병목이었고, PEG 기반 구성은 전체 행렬을 저장해야 해 QC보다 더 비효율적.
3. 채널은 BI-AWGN, decoder는 sum-product(최대 1000 iteration), circulant는 girth-4를 피하도록 구성.
4. 핵심 기법: circulant 열을 L번 독립적으로 두지 않고 주기 `T`(1, 2, 3)로 재사용(reuse-T)하여 저장해야 할 고유 circulant 수를 `nb*dl*T`로 제한 — 예제에서 reuse-1/2/3은 각 6/12/18개 circulant만 필요.
5. `∆xk,xj(l) = pxk,l - pxj,l` 및 cycle 조건 `Σ∆xk,xk+1(lk) = 0 mod M` — circulant shift 값이 만드는 cycle 존재 조건식.
6. reuse-T에 따른 inevitable cycle 정리: reuse-1은 girth 상한 6, reuse-2는 girth 상한 8, reuse-3은 girth 상한 10 (Lemma 1~3, shift 값과 무관하게 항상 존재하는 cycle 증명).
7. 부수 트릭: girth-4를 피하도록 circulant shift 값을 선택하는 구성 알고리즘, 특수 Cyclic Shift Unit으로 QC 행렬을 실시간 생성(전체 행렬 미저장).
8. 최적화 절차 없음(closed-form 구성 + girth 회피 탐색); density evolution으로 threshold만 별도 계산.
9. 결과: reuse-3는 BER 10^-6까지 non-periodic(무재사용) QC SC-LDPC와 동등 성능을 유지하면서, 100K 코드 기준 BRAM을 PEG 대비 최대 43배 절감, 동작 클럭 최대 40% 향상(Kintex-7 FPGA, reuse-3는 BRAM 자체 불필요).
10. 한계: 매우 긴 코드(≥100K bit) 전제, BI-AWGN·sum-product(soft) 환경만 시뮬레이션, NAND 특유의 hard/저비트 soft-read 환경이나 실제 실측(ASIC)은 다루지 않음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC circulant 재사용 기반 H-matrix 구성(reuse-T) | `ecc_top.cpp` `Load_PCM()` | Prime ECC는 이미 QC(`PCM_b` base+shift) 구조지만 SC-LDPC 체인 구조는 아님 — 부호설계 레벨 재작업 필요, 이식 난이도 높음 |
| Cyclic Shift Unit(circulant 실시간 생성, 메모리 절감) | 대응 없음 | Prime ECC HW 모델(z=32 lifting, HCU/GT)과는 다른 메모리 절감 접근(circulant 재사용) — 직접 대응 모듈 없음 |
| girth/inevitable cycle 분석 | 대응 없음 | H-matrix 설계 검증 단계 관련이나 Prime ECC 코드베이스 내 대응 모듈 없음(부호설계는 `Load_PCM()`에서 로드만) |

> 적용 가치: 중간 — SC-LDPC 자체는 Prime ECC의 non-SC QC-LDPC 구조와 다르지만, "circulant 재사용을 통한 H-matrix 메모리 절감" 아이디어는 향후 부호설계/HW 메모리 최적화 검토 시 참고할 여지가 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:1305.5625v2",
  "title": "Memory Efficient Quasi-Cyclic Spatially Coupled LDPC Codes",
  "year": 2013,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "SC-LDPC",
  "code_rate": 0.488,
  "code_length": 103200,
  "soft_quant": "soft-4bit+",
  "key_contribution": "주기적 time-variant QC 구성으로 SC-LDPC 회로(circulant)를 재사용(reuse-T)하여 파리티체크 행렬 저장 메모리(BRAM)를 대폭 절감하면서 girth/BER 성능을 유지하는 구성법 제안",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "BI-AWGN 채널·sum-product(soft) 디코더 기준 시뮬레이션이며, reuse-1/2는 girth 저하로 성능이 나쁘고 reuse-3만 유효; NAND용 QC-LDPC와 달리 SC-LDPC는 매우 긴 코드(100K+)를 전제로 함",
  "todo_check": "reuse-3 QC SC-LDPC의 성능 유지 결과가 hard-decision/저비트 soft-read(NAND read) 환경에서도 유지되는지, Prime ECC의 고정 QC-LDPC(non-SC) 구조에 SC 방식 도입 실익이 있는지 확인 필요"
}
```
