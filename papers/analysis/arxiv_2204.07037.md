### arxiv:2204.07037v2 - Low-Density Parity-Check Codes: Tracking Non-Stationary Channel Noise Using Sequential Variational Bayesian Estimates (2023, arXiv eess.SP)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 220 |
| 연판정 | soft-4bit+ |
| 핵심기여 | LDPC를 cluster graph로 표현하고 gamma prior 기반 순차 Bayesian 추론으로 비정상(non-stationary) SNR을 on-the-fly 추적 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | AWGN/BPSK·5G NR 채널 가정, cluster graph + VMP/LBU 추론은 min-sum HW 파이프라인과 이질적, non-stationary 채널이 NAND에 부적합 |
| 추가확인 | cluster graph 추론 대비 표준 min-sum + SNR 추정의 상대 이득이 NAND의 fixed/known-RBER 환경에서 존재하는지 |

> 총평: 5G 무선 채널의 SNR mismatch를 겨냥한 Bayesian 추론 기법으로, NAND의 고정형 min-sum QC-LDPC 파이프라인에 이식 가치가 낮다.

### B. 알고리즘 요약

1. 시스템: 5G NR base graph 2, 확장인자 11, shortened `N=220`, `K=110`, rate `R=0.5`, BPSK/AWGN. 정확도용 예시는 (16,8) irregular.
2. 문제: AWGN 디코딩은 채널 noise variance(SNR)를 알아야 하는데, 과·과소추정 시 성능 저하하고 무선 SNR은 시간에 따라 non-stationary.
3. 모델: 채널 precision `γ`에 gamma prior(conjugate)를 부여, 수신 `xn`을 conditional Gaussian likelihood `f(xn|bn,γ)`로 모델링.
4. 핵심기법 1단: LDPC를 factor graph 대신 cluster graph로 표현(LTRIP 알고리즘으로 RIP 만족), 각 cluster가 parity-check 제약.
5. 핵심식: gamma cluster ↔ conditional Gaussian cluster 사이 VMP로 `⟨γ⟩,⟨log γ⟩` 기대값을 주고받아 `γ`를 sufficient statistics로 갱신.
6. 핵심기법 2단: parity-check cluster 간에는 LBU(loopy belief update, sepset belief 갱신)를, Gaussian↔parity 간에는 hybrid message passing을 사용.
7. 구현 트릭: 큰 cardinality parity cluster를 하위 계층으로 격리하는 layered message schedule, KL divergence 기반 cluster 비활성화, sparse table.
8. 순차학습: 매 packet의 posterior gamma를 다음 packet의 prior로 쓰되, scaling factor `S×N/(ν/2-1)`로 자연파라미터를 재조정해 과거 추정을 지수적으로 forget → non-stationary 추적.
9. 결과: stationary 실험에서 perfect-knowledge PGM과 BER·iteration이 거의 동일; drive-test에서 fixed-precision 대비 약 1.5배 낮은 BER, iteration 약 1.02배 감소.
10. 한계: HW 미설계, 시뮬만, AWGN/5G 무선 특화, time-constant를 prior로 수동 지정해야 함.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SNR/precision 추정 + soft-info | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | LLR/threshold 설정과 개념적으로 닿으나 gamma 추론은 대응 없음 |
| parity-check 메시지 패싱(LBU) | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 우리는 min-sum, 논문은 belief-update 추론 → 알고리즘 이질 |
| cluster graph SNR 추론 전체 | 대응 없음 | NN/full-belief-propagation류로 min-sum 파이프라인에 대응 모듈 없음 |

적용 가치: 낮음 - non-stationary 무선 SNR 추적용 cluster graph Bayesian 추론이라 fixed-RBER binary min-sum QC-LDPC NAND 엔진과 정합성이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2204.07037v2",
  "title": "Low-Density Parity-Check Codes: Tracking Non-Stationary Channel Noise Using Sequential Variational Bayesian Estimates",
  "year": 2023,
  "venue": "arXiv eess.SP",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "220",
  "soft_quant": "soft-4bit+",
  "key_contribution": "LDPC를 cluster graph로 표현하고 gamma prior 기반 순차 Bayesian 추론으로 non-stationary SNR을 on-the-fly 추적",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "악화",
  "recommend": "하",
  "caveat": "AWGN/BPSK·5G NR 가정, cluster graph 추론이 min-sum HW와 이질적, non-stationary 채널이 NAND에 부적합",
  "todo_check": "NAND fixed/known-RBER 환경에서 SNR 추정의 상대 이득 존재 여부"
}
```
