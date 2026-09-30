### arxiv_1105.2624v1 - A Flexible LDPC code decoder with a Network on Chip as underlying interconnect architecture (2011, arXiv [cs.AR])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.83 |
| 부호length | 576~64800 |
| 연판정 | soft-4bit+ |
| 핵심기여 | NoC(torus mesh) 기반 완전 유연 LDPC 디코더 + Zero-Overhead 정적 라우팅으로 이기종 코드 온더플라이 전환 |
| HW설계 | O |
| 검증수준 | ASIC합성 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | 부분 |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | 이기종 임의 H-matrix 유연성 목적이라 고정 QC-LDPC엔 barrel-shifter가 더 효율적, NoC 오버헤드 불필요 |
| 추가확인 | early stopping이 avg iter 3~5회 수준으로 감소시킨 근거(Fig.8)—NAND 고rate 코드로 재현되는지 |

> 총평: WiMAX/WiFi/DVB-S2용 임의 이기종 LDPC를 지원하는 NoC 유연 디코더 HW로, 고정 binary QC-LDPC를 쓰는 Prime ECC엔 유연성 오버헤드가 불필요해 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: 다중 이기종 LDPC(WiMAX/WiFi/DVB-S2)를 하나의 디코더가 지원, PE들을 2D torus mesh NoC로 연결.
2. 문제: QC-LDPC 전용 barrel-shifter 상호연결은 임의 구조 H를 못 다룸, 완전 유연 디코더용 저비용 인터커넥트 필요.
3. 복호 알고리즘: layered decoding + normalized min-sum, LLR `L(q_mj)=L(q_j^old)-R_mj^old`, first/second minimum `A1/A2`, 정규화 `α`.
4. 핵심 식: `R_mj^new = -s_mj·A1_mj/α` (또는 `A2_mj/α`), 정규화 `α≥1`로 min-sum 근사 열화 보상.
5. NoC 접근: 각 노드=1 PE, 5포트(4방향+로컬), 입력 FIFO+crossbar, PE 수 << parity constraint 수라 순차 처리.
6. Zero-Overhead NoC(ZONoC): H 구조가 사전에 알려져 있으므로 라우팅 경로를 정적으로 유도해 라우팅 메모리에 저장, 동적 라우팅 제거.
7. PE 구조: pipeline 실행, WAG 메모리(쓰기 주소 생성), CNT/CMP(읽기 주소), L(q_j)/R_mj 메모리, MINIMUM EXTRACTION+COMPARE.
8. 구성: Metis 그래프 분할(recursive k-way)로 parity constraint를 PE에 클러스터링(메시지 |C| 6~34% 절감), cycle-accurate 시뮬로 라우팅/FIFO 길이 도출, circular buffer로 코드 무중단 전환.
9. 결과: 130nm 합성(5x5 WiMAX/4x4 WiFi/8x8 DVB-S2), 8.1 양자화·α=1.15, worst-case throughput 70Mb/s+ 표준 충족, early stopping으로 avg iter 감소(Fig.8).
10. 한계: 유연성이 목적이라 area 오버헤드(재구성 14.5% 등), NAND/자기 무관, 정정능력 개선 없음(순수 아키텍처).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| layered normalized min-sum 복호 | `decoder.cpp` `LDPC_Decoder()`, `CNU_Update_New_Mag()` | min-sum·first/second min은 이미 보유, 중복 |
| NoC torus mesh 인터커넥트 | 대응 없음 | Prime ECC는 z=32 고정 QC-LDPC(barrel-shift 계열), NoC 불필요 |
| WAG/CNT 주소생성·메모리 조직 | 디코더 HW 모델(z=32, HCU, GT) | 임의 H용 주소생성이라 고정 circulant 구조와 정합 안됨 |
| early stopping | `partial_CRC.cpp` `partial_crc_HW_T4()`, `full_CRC.cpp` | 조기종료는 이미 보유(Partial+Full CRC) |

적용 가치: **낮음** — NoC 유연성은 이기종 임의 H를 위한 것으로 고정 binary QC-LDPC인 Prime ECC엔 오버헤드만 추가되며, min-sum·early stopping 등 핵심 요소는 이미 보유.

### D. JSON 블록

```json
{
  "id": "arxiv:1105.2624v1",
  "title": "A Flexible LDPC code decoder with a Network on Chip as underlying interconnect architecture",
  "year": 2011,
  "venue": "arXiv [cs.AR]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.5~0.83",
  "code_length": "576~64800",
  "soft_quant": "soft-4bit+",
  "key_contribution": "NoC(torus mesh) 기반 완전 유연 LDPC 디코더 + Zero-Overhead 정적 라우팅으로 이기종 코드 온더플라이 전환",
  "hw_designed": "O",
  "verification": "ASIC합성",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "부분",
  "latency": "동등",
  "recommend": "하",
  "caveat": "이기종 임의 H-matrix 유연성 목적이라 고정 QC-LDPC엔 barrel-shifter가 더 효율적, NoC 오버헤드 불필요",
  "todo_check": "early stopping이 avg iter 3~5회 수준으로 감소시킨 근거(Fig.8)—NAND 고rate 코드로 재현되는지"
}
```
