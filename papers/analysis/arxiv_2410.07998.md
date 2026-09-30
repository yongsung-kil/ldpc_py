### arxiv:2410.07998v1 - A Graphical Correlation-Based Method for Counting the Number of Global 8-Cycles on the SCRAM Three-Layer Tanner Graph (2024, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 4320 |
| 연판정 | 무관 |
| 핵심기여 | SCRAM 3층 Tanner graph의 global girth 하한(≥8) 유도 + global 8-cycle 개수를 세는 상관기반 그래프 알고리즘 |
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
| 한계,주의 | 6G Slotted ALOHA 랜덤액세스(다중접속) 전용 3층 Tanner graph 분석이라 NAND 단일 LDPC 부호설계/디코더와 무관 |
| 추가확인 | 없음 (도메인 상이로 이식 대상 아님) |

> 총평: 6G 랜덤액세스 SCRAM 결합디코더의 사이클 프로파일 분석 이론 논문으로 NAND binary LDPC ECC에 이식 가치 없음(이식성 하).

### B. 알고리즘 요약

1. 시스템은 6G 다중접속용 SCRAM(Slotted Coded Random Access Multiplexing): 각 사용자가 LDPC로 부호화 후 Slotted ALOHA로 공유채널에 전송, 충돌 해소와 LDPC 복호를 결합 수행.
2. 문제는 기존 순차 디코더(MUD 후 FEC bank)의 성능 한계, 그리고 SCRAM 3층 Tanner graph의 사이클 프로파일을 기존 LDPC 도구로 분석 시 사용자수·부호길이에 지수적 복잡도.
3. 모델: 변수노드(전송심볼) + SA 체크노드(슬롯) + LDPC 체크노드의 3층 그래프, complex AWGN 채널, BPSK/OFDM.
4. 결합복호(Algorithm 1): SA 체크노드는 충돌심볼 조합의 조건부확률로 LLR 계산, LDPC 체크노드는 고전 BP `tanh` 규칙, 변수노드는 양측 LLR 합산.
5. 핵심분석: 3층 그래프의 girth 유도. local cycle(단일 사용자 LDPC 서브그래프)과 global cycle(SA 체크노드 경유 사용자 간) 구분.
6. 확장: monomial 전파 추적(t=0~7 등)으로 global cycle 최소길이가 8임을 단계별로 증명, `gglobal ≥ 8`, `gSCRAM ≥ min(8, glocal)`.
7. 구현 디테일: 3층 Tanner graph를 hybrid matrix `HSCRAM`(SA 서브행렬 + LDPC 서브행렬)로 매핑해 기존 Full-Cycle/Half-Cycle 카운팅 알고리즘 재사용.
8. 제안 알고리즘: global 8-cycle 전용 상관기반 카운터 — 두 사용자 각각의 connected 변수노드쌍과 공유 SA 체크노드 2개를 찾아 순회, 열 element-wise 곱으로 공통 LDPC 체크노드 판정.
9. 결과: DVB-NGH `(4320,2160)` LDPC 4사용자 SCRAM(`Ns=8640`)에서 `C6=124800`, `C8=6234085` (순수 LDPC의 4배 6-cycle → 6-cycle은 개별 LDPC 서브그래프에만 존재).
10. 한계: 순수 그래프 이론 분석(HW 미설계, BER/PER 성능곡선 없음), 6G 다중접속 결합디코더 전용.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 개별 LDPC BP(`tanh`) 복호 | decoder.cpp `LDPC_Decoder()` | Prime ECC는 min-sum, 논문은 full-tanh 결합디코더라 대응 아님 |
| 3층 Tanner graph / SA 결합디코딩 | 대응 없음 | Slotted ALOHA 다중접속 전용 구조 |
| girth/cycle 프로파일 카운팅 | 대응 없음 | Prime ECC는 고정 QC-LDPC라 부호설계 사이클분석 모듈 없음 |
| hybrid matrix 매핑 | 대응 없음 | 다중사용자 랜덤액세스 전용 |

적용 가치: 낮음 — 6G Slotted ALOHA 랜덤액세스 결합디코더의 3층 Tanner graph 사이클분석 이론으로, NAND용 단일 binary QC-LDPC의 부호설계/디코더/HW 어디에도 대응이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2410.07998v1",
  "title": "A Graphical Correlation-Based Method for Counting the Number of Global 8-Cycles on the SCRAM Three-Layer Tanner Graph",
  "year": 2024,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "4320",
  "soft_quant": "무관",
  "key_contribution": "SCRAM 3층 Tanner graph의 global girth 하한(>=8) 유도 + global 8-cycle 개수를 세는 상관기반 그래프 알고리즘",
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
  "caveat": "6G Slotted ALOHA 랜덤액세스(다중접속) 전용 3층 Tanner graph 분석이라 NAND 단일 LDPC 부호설계/디코더와 무관",
  "todo_check": "없음 (도메인 상이로 이식 대상 아님)"
}
```
