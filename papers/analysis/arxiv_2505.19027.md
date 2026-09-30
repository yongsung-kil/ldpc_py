### arxiv:2505.19027v1 - High Throughput QC-LDPC Decoder With Optimized Schedule Policy in Layered Decoding (2025, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.33~0.5 |
| 부호length | 2112~8448 |
| 연판정 | 무관 |
| 핵심기여 | 파이프라인 layered 복호의 idle cycle 최소화를 비대칭 TSP로 정식화하되 성능 좋은 스케줄 특성(저degree·puncture 우선)을 그래프에 반영해 idle time과 복호성능 동시 최적화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | HW 미구현(gatecount/throughput 수치 없음), 5G NR BG1 대상, SO path latency t가 작을 때만 무손실 보장 |
| 추가확인 | Prime ECC의 dual-update/z=32 파이프라인·HCU 구조에서 layer 재배치가 그대로 성립하는지, common-degree 계산 방식 정합 여부 |

> 총평: QC-LDPC layered 복호의 스케줄 순서를 TSP로 최적화해 memory conflict(idle cycle)와 복호성능을 함께 잡는 순수 알고리즘 기법으로, NAND용 QC-LDPC 파이프라인 디코더 스케줄러에 이식 시도 가치 있음(중).

### B. 알고리즘 요약

1. 시스템: 5G NR QC-LDPC(BG1), rate `1/3`(K=8448)·`1/2`(K=2112), layered BP(LBP) 파이프라인 복호, SO data path latency `t∈{4,9}`.
2. 문제: 파이프라인 layered 복호에서 인접 layer 간 memory conflict로 idle cycle이 삽입되어 throughput 저하, 기존 연구는 idle 최소화만 보고 복호성능 영향은 무시.
3. 핵심 모델: 한 iteration의 idle cycle 수 `nidle`를 layer degree `dci`와 인접 layer 공통 degree `dc_{ci-1,ci}`로 계산: `max(t-(dci - dc_{ci-1,ci}),0)` 합.
4. 핵심 기법 1단: 최소 idle 스케줄 탐색을 비대칭 TSP로 정식화 - 노드=layer, edge weight=전이 idle cycle, Hamiltonian cycle 최소화(differential evolution 또는 대칭 TSP 변환으로 해결).
5. 핵심 기법 2단: 좋은 복호성능 스케줄 특성(저degree 우선, punctured VN 연결 적은 것 우선)을 반영해 layer를 `(di,pi)` 그룹으로 라벨링.
6. 그래프 수정: 라벨 `i→j`가 `i+1=j`, `i=j`, `i=P,j=1` 조건이 아니면 edge weight를 `+∞`로, P→1 edge엔 큰 상수 `H`를 더해 라벨 오름차순 갱신 강제.
7. 근사식: `c1,cm`을 공통 degree 작게 고르면 `nidle≈n'idle`, t가 작을 때 저degree 먼저 갱신이 최소 idle 달성(Proposition 1, 균일 랜덤 연결·`t≤dmin` 가정).
8. 결과(성능): idle만 최소화한 스케줄은 BLER 성능이 크게 열화, idle&performance 정책은 LD/nest 대비 성능 유지하며 idle 대폭 감소.
9. 결과(idle, Table I): t=4에서 nidle - nest 19/10, LD 15/9, idle 2/2, idle&performance 6/4 (R=1/3/R=1/2), t=9에서도 성능 정책이 nest·LD보다 idle 적음.
10. 한계: RTL/gatecount/throughput 등 실제 HW 지표 미제시, 시뮬만, 성능-idle 무손실은 t 작을 때 확률적 보장.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| layered(LBP) 스케줄 순서 / 이터레이션 루프 | decoder.cpp `LDPC_Decoder()` | Prime ECC의 dual-update(even/odd 교대) layer 스케줄에 idle-aware 순서 적용 여지 |
| memory conflict / pipeline idle cycle | 디코더 HW 모델(z=32, pipeline 6-stage) | Prime ECC 6-stage 파이프라인의 read/write 충돌 회피 스케줄로 매핑 가능 |
| QC-LDPC layer degree / H-matrix 구조 | ecc_top.cpp `Load_PCM()` | layer degree·common degree 산출은 로드된 PCM 구조 기반 |

적용 가치: **중간** — CN min-sum 연산 자체는 안 바꾸고 layer 갱신 순서만 재배치해 파이프라인 idle을 줄이는 저침습 기법이라 Prime ECC 스케줄러에 검토할 가치가 있으나, 우리 dual-update·HCU·z=32 구조 정합과 HW 검증이 필요하다.

### D. JSON 블록

```json
{
  "id": "arxiv:2505.19027v1",
  "title": "High Throughput QC-LDPC Decoder With Optimized Schedule Policy in Layered Decoding",
  "year": 2025,
  "venue": "arXiv [cs.IT]",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.33~0.5",
  "code_length": "2112~8448",
  "soft_quant": "무관",
  "key_contribution": "파이프라인 layered 복호의 idle cycle 최소화를 비대칭 TSP로 정식화하되 성능 좋은 스케줄 특성을 그래프에 반영해 idle time과 복호성능 동시 최적화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "중",
  "caveat": "HW 미구현(gatecount/throughput 수치 없음), 5G NR BG1 대상, SO path latency t가 작을 때만 무손실 보장",
  "todo_check": "Prime ECC의 dual-update/z=32 파이프라인·HCU 구조에서 layer 재배치가 그대로 성립하는지, common-degree 계산 방식 정합 여부"
}
```
