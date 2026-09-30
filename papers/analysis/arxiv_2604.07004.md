### arxiv:2604.07004v1 - Channel Estimation and LDPC Decoding for Bursty Phase Noise (2026, arXiv (eess.SP), ECOC'25 확장판)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 0.826 |
| 부호length | 17664 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Wiener-Gilbert-Elliott 버스트 위상잡음 채널을 BCJR/VA/SOVA로 상태추정해 burst-aware LLR을 계산하고, 채널추정-LDPC복호 반복(IBA)으로 BER/PER을 최대 2자릿수 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 표준 IEEE 802.3ca LDPC(부호 자체는 미변경, encoder/decoder 알고리즘도 표준 그대로)를 사용하며 개선은 순수 채널추정+LLR 전처리 레이어; 위상잡음/differential coding/QAM 등 광통신·무선 특유 가정이라 NAND read channel(진폭 임계값 기반)과 물리적으로 이질적 |
| 추가확인 | NAND의 read-retry/에러패턴이 버스트성(예: WL간 간섭, RTN)을 갖는 경우 GE 모델+BCJR 상태추정 아이디어가 LLR 보정에 참고될 수 있는지 채널모델 재정의 필요 |

> 총평: 위상잡음 버스트 채널 특화 채널추정+LLR 전처리 기법으로 LDPC 디코더 자체(부호설계·min-sum 알고리즘)는 손대지 않으며 광통신/무선 위상잡음 가정에 강하게 결합되어 있어 NAND binary LDPC로의 직접 이식성은 낮음.

### B. 알고리즘 요약

1. 시스템: IEEE 802.3ca 표준 LDPC(길이 17664bit, 정보 14592bit, rate≈0.826)를 QPSK/16QAM/64QAM로 전송, 버스트 위상잡음+AWGN이 있는 광/무선 채널.
2. 문제: 기존 LDPC 디코더는 AWGN만 가정해 시간상관을 갖는 burst 위상잡음(오실레이터 불안정, 진동, 온도변화 등)에서 성능 저하, 특히 패킷 단위 재전송 구조상 PER 급증.
3. 핵심 가정/모델: 위상잡음을 Gilbert-Elliott(GE) 2상태(Good/Bad) 마르코프로 변조된 Wiener 프로세스로 모델링(`θ_k = θ_{k-1}+w_k`, `w_k~N(0,σ_zk^2)`), differential encoding 후 차분위상잡음은 상태별 분산을 갖는 zero-mean Gaussian으로 근사.
4. 핵심 기법 1단(채널상태추정): 2상태 trellis에서 VA/SOVA/BCJR로 상태확률 `P(z_k)` 추정, BCJR이 forward-backward recursion(`α_k`, `β_k`)으로 가장 정확.
5. 핵심 식: burst-aware LLR은 상태확률로 가중평균한 우도 `p(y_k|x_k)=Σ_zk P(z_k)p(y_k|x_k,z_k)`(식28)로 계산 - 상태별 분산차(`σ_G^2 ≪ σ_B^2`)를 반영해 나쁜 상태 구간의 신뢰도를 낮춤.
6. 확장(IBA): 디코더 출력 LLR을 심볼확률로 변환해 채널추정기로 피드백하는 외부 반복(outer iteration)을 도입, 채널추정-복호 간 정보교환으로 상태추정 정확도 향상.
7. 부수 트릭: bias `δ`(effective noise variance 배율)를 modulation별로 최적화(QPSK -3dB, 16/64QAM -2dB, IBA 반복시 δ'=5dB), BCJR은 windowed(윈도우 100)로 구현해 수치안정성 확보.
8. 최적화 절차: Monte-Carlo 시뮬로 δ, δ'를 그리드서치, 외부반복 3회 후 성능 포화 관찰.
9. 결과: 64QAM에서 IBA가 baseline 대비 BER 4e-3 기준 1.4dB, PER 1e-2 기준 3dB 이상 이득; 심한 버스트(σ_B²=1) 조건에서 BER/PER 최대 2자릿수 감소.
10. 한계: LDPC 부호설계·디코더 내부(min-sum/sum-product) 알고리즘 변경 없음(표준 코드 그대로), HW 구현·gatecount 없음, differential coding으로 인한 고유 SNR 손실 존재, 광통신/무선 위상잡음 채널에 특화되어 NAND read channel과 물리적 정합성 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| burst-aware LLR 계산(채널상태 가중 우도) | `channel.cpp` `Set_R_Offset()`, `Set_LLR_Th()` | soft-read LLR/threshold 설계 레이어에 해당하나 위상잡음 특유 모델이라 NAND RBER 채널과 직접 대응 어려움 |
| LDPC 디코딩 루프(변경 없음, 표준 그대로) | `decoder.cpp` `LDPC_Decoder()` | 논문이 디코더 내부를 건드리지 않으므로 관련성 낮음 |
| 채널상태추정(VA/SOVA/BCJR, 2-state trellis) | 대응 없음 | Prime ECC에는 별도 채널 상태추정기(마르코프 trellis) 모듈 없음 |
| outer iteration(채널추정-복호 피드백) | 대응 없음 | Prime ECC는 단일 디코더 루프이며 외부 채널추정 피드백 루프 없음 |

> 적용 가치: 낮음 - burst-aware LLR 보정 개념 자체는 흥미로우나 위상잡음/differential coding/QAM 특유 채널모델에 강결합되어 있고 부호·디코더 알고리즘 개선이 없어 Prime ECC(NAND binary QC-LDPC)에 이식할 요소가 제한적임.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.07004v1",
  "title": "Channel Estimation and LDPC Decoding for Bursty Phase Noise",
  "year": 2026,
  "venue": "arXiv (eess.SP), ECOC'25 확장판",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": 0.826,
  "code_length": 17664,
  "soft_quant": "soft-4bit+",
  "key_contribution": "Wiener-Gilbert-Elliott 버스트 위상잡음 채널을 BCJR/VA/SOVA로 상태추정해 burst-aware LLR을 계산하고, 채널추정-LDPC복호 반복(IBA)으로 BER/PER을 최대 2자릿수 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "표준 IEEE 802.3ca LDPC(부호 자체는 미변경, encoder/decoder 알고리즘도 표준 그대로)를 사용하며 개선은 순수 채널추정+LLR 전처리 레이어; 위상잡음/differential coding/QAM 등 광통신·무선 특유 가정이라 NAND read channel(진폭 임계값 기반)과 물리적으로 이질적",
  "todo_check": "NAND의 read-retry/에러패턴이 버스트성(예: WL간 간섭, RTN)을 갖는 경우 GE 모델+BCJR 상태추정 아이디어가 LLR 보정에 참고될 수 있는지 채널모델 재정의 필요"
}
```
