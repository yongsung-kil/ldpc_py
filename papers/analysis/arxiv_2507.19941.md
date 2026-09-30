### arxiv:2507.19941v1 - Adaptive Learned Belief Propagation for Decoding Error-Correcting Codes (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.43~0.96 |
| 부호length | 128~4260 |
| 연판정 | soft-4bit+ |
| 핵심기여 | WBP/WMS 가중치를 수신어마다 적응 결정 - 병렬 WMS(이산 가중치 탐색, 최소 신드롬 선택) + 2단(CNN이 가중치 예측) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 중 |
| 한계,주의 | 오프라인 학습된 가중치 분포/CNN 필요, 정적 WBP 재훈련·분포이동 취약, HW 미설계·시뮬만 |
| 추가확인 | 병렬 WMS(2SD/3SD 저비트 LLR) 적용 시 이득 유지 여부, per-word 가중치 스케줄을 우리 적응형 LLR 테이블/normalized MS로 근사 가능한지 |

> 총평: min-sum(WMS) 가중치를 수신어마다 적응시켜 정적 WBP 대비 BER 최대 1자릿수·최대 0.8dB 개선하는 복호기로, 병렬 WMS 변형은 동일 복잡도·latency로 Prime ECC min-sum에 이식 여지가 있어 정독 가치 중.

### B. 알고리즘 요약

1. 대상: `(n,k)` binary linear code(BCH `(63,36)`, polar, 다수 QC-LDPC regular/irregular rate 0.43~0.96), AWGN(BPSK, `L(y)=4rρy`) + 비선형 광섬유(16-QAM WDM, 내부 QC-LDPC + 외부 SC-QC-LDPC 연접) 채널.
2. 문제: 정적 WBP(오프라인 학습 가중치)는 짧은 블록·저rate·고SNR에서만 유효하고 저BER·장블록에서 sample complexity 폭증으로 일반화 실패.
3. WBP 기반: Tanner graph를 `T` iteration으로 unroll한 RNN에서 CN/VN 메시지에 가중치 `γ_{v,c}^t, β_{c,v}^t` 부여(식9~10), WMS는 `tanh` 근사 min-sum + 가중치.
4. 핵심 기여: 가중치를 수신어 `y`마다 온라인 결정하는 적응형 WBP `γ=g(y)`로 오류확률 최소화(식13), 정적 복호기는 `g`가 상수인 특수경우.
5. 변형1 병렬 복호기: `γ^t`를 이산집합에서 취해 `ν`개 WMS를 동시 실행, 신드롬 Hamming weight 최소인 `i*=argmin‖s_i‖`를 선택(식14). 탐색 깊이 `T1=5` 후 `T2` iteration 이어감.
6. 가중치 분포: `Γ^t`가 근사 가우시안 → `x_k^t=θ^t+√2σ^t·erfc^{-1}(...)`(식16)로 이산점 배치, 정적 WBP를 오프라인 학습해 경험적 CDF 추정.
7. 변형2 2단 복호기: CNN(`Conv1-Conv2-Dense`, ReLU)이 `L(y)`를 입력받아 가중치 벡터 `γ̄`를 예측(quantile loss `ξ=0.75` 학습), 병렬 복호기의 지수 복잡도 없이 임의 가중치 산출.
8. 학습: active learning으로 결정경계 근처 예제 표집(acquisition = Hamming distance), Adam, 가중치 pruning(`τ_prun`)으로 CNN 복잡도 1/4 감축.
9. 결과: AWGN에서 적응형 WMS가 정적 대비 BER 최대 1자릿수↓·`C1`에서 0.32dB gain(BER 1e-4), 동일 복잡도. 광섬유 연접에서 적응형 WBP가 NNMS 대비 0.8dB coding gain(동일 복잡도·동일 latency).
10. 한계: HW 미설계·시뮬만, 오프라인 학습된 분포/CNN 의존, 분포이동 시 재훈련 필요(본문서 미해결), 블록↑일수록 이득 감소.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| WMS 가중 min-sum CN 업데이트 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | min-sum magnitude에 iteration별 스케일 가중치 적용 지점과 직접 대응 |
| iteration별 적응 가중치 `γ^t` | ecc_data.h `PARAM_LLR`, decoder.cpp `Get_VNU_Table_Idx()` | 우리 iteration 구간별 LLR threshold 테이블과 유사 구조, 가중치 스케줄로 치환 검토 |
| 병렬 WMS + 최소 신드롬 선택 | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | 서로 다른 스케일로 병렬 복호 후 신드롬 최소 선택 로직 추가 형태로 이식 가능 |
| 신드롬 조기종료 | partial_CRC.cpp `partial_crc_HW_T4()`, full_CRC.cpp | 병렬 후보 판정 기준(신드롬 weight)과 우리 CRC 종료가 연동될 수 있음 |
| 2단 CNN 가중치 예측 | 대응 없음 | Prime ECC는 NN 미보유, CNN 추론 블록은 신규 이식 부담 |

적용 가치: **중간** — 병렬 WMS(iteration별 가중치 스위핑 후 최소 신드롬 선택)는 우리 min-sum 파이프라인과 적응형 LLR 테이블 구조에 비교적 낮은 부담으로 이식해 waterfall/error-floor를 개선할 여지가 있으나, 2단 CNN 변형과 오프라인 가중치 분포 학습은 NN 미보유·soft-4bit+ 전제라 추가 검증이 필요하다.

### D. JSON 블록

```json
{
  "id": "arxiv:2507.19941v1",
  "title": "Adaptive Learned Belief Propagation for Decoding Error-Correcting Codes",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.43~0.96",
  "code_length": "128~4260",
  "soft_quant": "soft-4bit+",
  "key_contribution": "WBP/WMS 가중치를 수신어마다 적응 결정 - 병렬 WMS(이산 가중치 탐색, 최소 신드롬 선택) + 2단(CNN이 가중치 예측)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "중",
  "caveat": "오프라인 학습된 가중치 분포/CNN 필요, 정적 WBP 재훈련·분포이동 취약, HW 미설계·시뮬만",
  "todo_check": "병렬 WMS(2SD/3SD 저비트 LLR) 적용 시 이득 유지 여부, per-word 가중치 스케줄을 우리 적응형 LLR 테이블/normalized MS로 근사 가능한지"
}
```
