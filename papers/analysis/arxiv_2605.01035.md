### arxiv:2605.01035v1 - A Scalable FPGA Architecture for Real-Time Decoding of Quantum LDPC Codes Using GARI (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 144 |
| 연판정 | soft-4bit+ |
| 핵심기여 | GARI 변환 후 quantum LDPC(bivariate bicycle code)의 correlated error(X/Y/Z)를 처리하는 자원 재사용형 FPGA 디코더 아키텍처 제안 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 122393 LUT / 111697 REG / 704 BRAM (단일 코어, VU29P) |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | quantum LDPC(비-CSS 상호작용 X/Y/Z error, GARI 변환 특유 구조) 전용이라 binary NAND LDPC 부호 구조와 근본적으로 다름 |
| 추가확인 | 크로스바 라우팅/타일 매핑 아이디어가 자원 재사용 관점에서 일반 병렬 LDPC HW에 참고될 여지가 있는지 |

> 총평: quantum LDPC(GARI 변환) 전용 FPGA 디코더 아키텍처로, 부호 구조와 CNU 스케줄링이 NAND binary QC-LDPC와 근본적으로 달라 이식성은 낮음.

### B. 알고리즘 요약

1. 대상은 `[[144,12,12]]` bivariate bicycle quantum LDPC 코드이며, X/Z/Y 세 종류 상관 오류(correlated error)를 다루는 detector error model을 decoding 대상으로 함.
2. 기존 X/Z 독립 디코딩은 Y-error로 인한 상관관계 때문에 성능이 저하되는 문제를 해결하려 함.
3. GARI(Graph Augmentation and Rewiring for Inference) 변환으로 detector error model `D_XYZ`를 4-cycle 없는 구조로 재작성, `D_X, D_Z, U, V` 서브행렬로 분리(식 (1)-(2)).
4. 아키텍처는 두 유닛으로 구성: `D_X, D_Z` 유닛(직렬 스케줄 BP)과 `U, V` 유닛(완전 병렬, 체크 간 독립).
5. `D_X, D_Z`는 메모리 기반 직렬 BP 디코더(변수당 메모리 할당, 체크당 순차 처리)로 정규화 min-sum(normalized min-sum) 규칙 사용.
6. `U, V` 유닛은 체크 간 완전 독립이므로 병렬 처리 가능하며, `D_X,D_Z` 처리 시간과 맞도록 병렬도(타일 수 18개)를 조정해 idle/과잉자원 방지.
7. eY 메시지를 U→V로 라우팅하기 위해 태그 기반 크로스바(binary radix sort 유사, K=⌈log2(J)⌉ 스테이지) 구조를 도입해 controller-less 라우팅 구현.
8. 학습/최적화 절차는 없고, 변수-타일 매핑은 greedy/heuristic search(NP-hard 문제의 근사해)로 수행.
9. VU29P FPGA에서 단일 코어 274 MHz, iteration당 1728 cycle, 평균 2.28회 반복 시 14.4 μs 지연(단일 디코더), 24-디코더 앙상블(3-코어×8 FPGA) 구성 시 라운드당 596 ns 달성 - 기존 GARI 구현 대비 자원 6분의 1.
10. 한계: FPGA 구현만 존재(ASIC 없음), 코드 특정적 자원 추정(범용화 어려움), 낮은 논리 오류율에서의 정확도 평가는 향후 과제로 남김.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| normalized min-sum CNU 연산 | `decoder.cpp` `CNU_Update_New_Mag()` | 이미 보유한 기법과 개념적으로 유사하나 quantum 특유 X/Y/Z 체크 구조 전제로 재검증 필요 |
| 메모리 기반 직렬 BP 스케줄링 | `decoder.cpp` `LDPC_Decoder()` | 스케줄링 개념은 참고 가능하나 D_X/D_Z/U/V 분리 구조는 binary QC-LDPC와 무관 |
| GARI 부호 변환(H-matrix 재구성) | `ecc_top.cpp` `Load_PCM()` | 대응 없음 (quantum non-CSS 상관오류 모델 전용, binary QC-LDPC 구조와 무관) |
| 크로스바 기반 메시지 라우팅 | 대응 없음 | GT.cpp의 edge 선택과 목적이 다름(HW 자원축소 vs U/V 타일 간 통신) |

적용 가치: 낮음 - quantum LDPC(비-CSS 상관오류, GARI 변환) 전용 구조로 NAND binary QC-LDPC 부호/디코더 설계와 직접적 접점이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.01035v1",
  "title": "A Scalable FPGA Architecture for Real-Time Decoding of Quantum LDPC Codes Using GARI",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "144",
  "soft_quant": "soft-4bit+",
  "key_contribution": "GARI 변환 후 quantum LDPC(bivariate bicycle code)의 correlated error(X/Y/Z)를 처리하는 자원 재사용형 FPGA 디코더 아키텍처 제안",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "122393 LUT / 111697 REG / 704 BRAM (단일 코어, VU29P)",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "quantum LDPC(비-CSS 상호작용 X/Y/Z error, GARI 변환 특유 구조) 전용이라 binary NAND LDPC 부호 구조와 근본적으로 다름",
  "todo_check": "크로스바 라우팅/타일 매핑 아이디어가 자원 재사용 관점에서 일반 병렬 LDPC HW에 참고될 여지가 있는지"
}
```
