### arxiv:2604.04066v1 - Quasi-BP for BCH Codes and its Optimization (2026, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.50~0.94 |
| 부호length | 127~255 |
| 연판정 | soft-4bit+ |
| 핵심기여 | BCH 등 HDPC 부호에 자동동형 기반 input dilation+merging으로 병렬 quasi-BP 복호 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | 대상이 dense HDPC(BCH) 부호이며 δ1δ2 배 복잡도 증가, HW 미설계, LDPC용 아님 |
| 추가확인 | GitHub 소스의 자동동형/dilation 구현이 QC-LDPC 구조에 무의미한지 재확인 |

> 총평: BCH(HDPC) 전용 병렬 BP 복호로, NAND용 binary QC-LDPC와 부호 계열이 달라 이식 가치 낮음.

### B. 알고리즘 요약

1. 시스템: AWGN+BPSK, `c=mG` GF(2), BCH(127,64/99)·BCH(255,239) 고밀도 부호를 대상으로 함(rate 0.50~0.94, length 127~255).
2. 문제: BCH 같은 HDPC 부호는 dense H로 Tanner 그래프에 짧은 사이클이 많아 표준 soft BP가 잘 안됨.
3. 가정: 채널 잡음분산 `σ²` 기지(known noise variance)를 전제로 LLR `l=2y/σ²` 계산.
4. 핵심기법1(quasi-BP): H에 잉여행 추가(redundancy factor `δ1`)와 BCH 자동동형(automorphism) 활용 input dilation(`δ2`)으로 메시지 집합 확장.
5. VN 업데이트 Phase One: 들어온 메시지를 blockwise cyclic reversion `ϕ⁻¹`로 정렬 후 merging weight `β`로 합쳐 MI 성장 가속 (식12).
6. Phase Two: 갱신된 `Lν`를 `δ2`배로 dilate해 check 노드로 분산 dispatch (식13); CN 업데이트는 표준 BP `tanh` 그대로(식4).
7. 최적화: 단일 파라미터 `β`를 최종 iteration 출력 MI `I_E,C` 최대화로 bisection line search; `lmax`는 S-EXIT 교차점+2로 선택.
8. 분석도구: scattered EXIT(S-EXIT) 차트로 유한길이 MI 분포 추적, `Ee[·]<τ`(τ=0.7) 로 FER를 4000회만으로 근사.
9. 결과: BCH(127,64)에서 NMS보다 0.6dB 우위, 동rate LDPC(128,64) NBP와 0.1dB 차; BCH(255,239)는 ML과 0.6dB.
10. 한계: iteration당 복잡도 약 `δ1δ2`배 증가, HW 미설계(GPU/TPU 언급뿐), 잡음분산 기지 전제, ML과 여전히 >1dB gap.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| quasi-BP 이터레이션 루프 | decoder.cpp `LDPC_Decoder()` | dense HDPC 전용 스케줄이라 QC-LDPC 루프에 그대로 이식 불가 |
| CN `tanh` full-BP 업데이트 | 대응 없음 | Prime ECC는 min-sum 근사 사용, full-tanh Sum-Product 미보유 |
| 잡음분산 기반 LLR `2y/σ²` | channel.cpp `Set_LLR_Th()` | 표준 LLR로 이미 보유, 신규성 없음 |
| input dilation / automorphism | 대응 없음 | BCH cyclic 자동동형 의존, QC-LDPC 구조에 대응 없음 |
| S-EXIT 파라미터 최적화 | local_opt.cpp | LLR 자동최적화와 개념적 유사이나 대상·지표 상이 |

적용 가치: **낮음** — 대상이 dense HDPC(BCH)이고 CN이 full-tanh BP, 부호구조가 NAND용 binary QC-LDPC와 근본적으로 달라 이식 실익이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.04066v1",
  "title": "Quasi-BP for BCH Codes and its Optimization",
  "year": 2026,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "127~255",
  "soft_quant": "soft-4bit+",
  "key_contribution": "BCH 등 HDPC 부호에 자동동형 기반 input dilation+merging으로 병렬 quasi-BP 복호",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "동등",
  "recommend": "하",
  "caveat": "대상이 dense HDPC(BCH) 부호이며 δ1δ2 배 복잡도 증가, HW 미설계, LDPC용 아님",
  "todo_check": "GitHub 소스의 자동동형/dilation 구현이 QC-LDPC 구조에 무의미한지 재확인"
}
```
