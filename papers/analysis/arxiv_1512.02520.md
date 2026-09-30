### arxiv:1512.02520v1 - Study of Structured Root-LDPC Codes and PEG Techniques for Block-Fading Channels (2015, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.33~0.5 |
| 부호length | 900~1024 |
| 연판정 | 무관 |
| 핵심기여 | block-fading 채널에서 full diversity를 보장하는 root-check 구조를 QC/IRA/IRAA/Controlled-Doping 형태로 PEG 기반 설계하는 알고리즘 제안, PEG-LDPC 대비 FER 최대 7.5dB 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | block-fading(무선/OFDM) 채널의 다중 페이딩 다이버시티 확보가 목적으로 NAND 채널 모델과 무관, 부호 rate가 1/F(≤0.5)로 NAND ECC 대비 매우 낮음, root-check identity/dual-diagonal 구조는 fading diversity 특화 설계 |
| 추가확인 | QC-PEG 알고리즘 자체(순수 girth 최대화 PEG 로직)는 root-check 제약을 제거하면 일반 QC-LDPC H-matrix 설계에 재사용 가능한지 |

> 총평: block-fading(무선) 채널에서 다이버시티 확보를 위한 Root-LDPC 부호설계(QC/IRA/IRAA/Controlled-Doping)와 PEG 알고리즘 제안 논문으로, NAND 저장 채널과 무관한 낮은 rate(1/F)의 페이딩 특화 구조라 이식성이 낮음.

### B. 알고리즘 요약

1. 시스템은 block-fading 채널(코드워드 내 `F`개 독립 Rayleigh 페이딩 블록, `r_t = h_f s_t + n_{g,t}`), 부호 rate는 Singleton bound에 따라 최대 diversity를 위해 `R=1/F`(F=2,3,4)로 고정.
2. 풀려는 문제는 non-ergodic block-fading 채널에서 표준 LDPC/PEG-LDPC는 full diversity(outage 한계 근접)를 달성하지 못하는 점 - root-check 구조로 정보 노드가 다른 페이딩 블록의 parity에 identity 연결되도록 강제해 최소 1개 fading이 충분히 크면 복구 가능하게 함.
3. 채널 모델은 BPSK + Rayleigh 페이딩 계수 `h_f` + AWGN, outage 확률 `P_out = P(I<R)`로 성능 정의.
4. 핵심 기법은 root-check identity sub-matrix를 H에 강제 배치(`H=[I H1i|H2i I|...]` 형태)하고, 나머지 edge는 PEG(Progressive Edge Growth) 알고리즘으로 girth를 최대화하며 채우는 QC-PEG-Root-LDPC/IRA-PEG-Root-LDPC/IRAA-PEG-Root-LDPC/PEG-CDRC(Controlled Doping) 4가지 구조 변형.
5. 핵심 식은 diversity population evolution(DPE) 안정상태 파라미터 `p_∞`(반복복호 후 parity bit가 회복되는 비율) - uncontrolled doping은 `p_∞≈7.82%`에 그치지만 controlled doping은 permutation matrix `P_i`와 dual-diagonal `DD` 배치로 `p_∞=100%`까지 개선.
6. 확장 기법으로 IRA(rate 1/2)/IRAA(rate 1/2~1/3, puncture로 rate 가변)/Controlled-Doping(50% doping) 등 인코딩 복잡도-성능 트레이드오프 다른 변형 제시, indicator vector `z_i`로 PEG expansion에서 특정 서브행렬 배치를 제약.
7. 구현 디테일로 각 rate/F별 indicator vector(`z_1,...,z_F`)를 명시적으로 정의해 root-check identity 위치와 upper/lower triangular parity 구조를 PEG 알고리즘에 반영, dual-diagonal parity(`H_p`)로 저복잡도 인코딩(RA 계열) 확보.
8. 최적화 절차는 PEG 트리 확장(depth `l`까지 minimum-weight check node 탐색) - 별도 학습/DE 최적화는 없음, 기존 PEG를 root-check 제약에 맞게 변형.
9. 결과: F=2, R=1/2에서 PEG-based Root-LDPC가 PEG-LDPC 대비 FER~10^-3에서 7.5dB 이득, F=3에서 QC-PEG-Root-LDPC가 QC-PEG-LDPC 대비 3.5dB, F=4에서 QC-PEG-Root-LDPC가 2.5dB 이득; 중~고 SNR에서 평균 반복횟수 2회 미만으로 감소.
10. 한계: block-fading(무선/OFDM) 채널 전용이며 NAND 저장 채널 모델과 무관, rate가 1/F(≤0.5)로 NAND ECC(고rate) 대비 매우 낮음, HW 구현/합성 결과 없이 시뮬레이션(FER)만 제시.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-PEG 기반 H-matrix 구성(girth 최대화) | ecc_top.cpp `Load_PCM()` | H-matrix 구성 단계와 개념적으로 연결되나 Prime ECC는 특정 QC-LDPC 고정 - 이식 난이도 높음(프로파일 §4) |
| Root-check identity / dual-diagonal 구조 | encoder.cpp `LDPC_encoder_4KB()`, `Generate_PCM_encoding()` | dual-diagonal 인코딩 개념은 유사하나, root-check는 fading-diversity 전용 구조로 NAND에는 무의미 |
| Iterative message-passing 디코더 | decoder.cpp `LDPC_Decoder()` | SPA 기반 일반 디코더로만 겹치며, 논문 고유 기여(root-check 구조)는 디코더 알고리즘 자체가 아님 |

> 적용 가치: 낮음 - block-fading(무선) 채널의 diversity 확보가 목적인 저rate(1/F) Root-LDPC 부호설계로, NAND 고전 binary QC-LDPC(고rate, AWGN/RBER 채널)와 목표·채널모델·rate가 모두 달라 직접 이식 대상이 아님. PEG 기반 girth 최대화 로직 자체만 일반적 참고 가치.

### D. JSON 블록

```json
{
  "id": "arxiv:1512.02520v1",
  "title": "Study of Structured Root-LDPC Codes and PEG Techniques for Block-Fading Channels",
  "year": 2015,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": 0.4,
  "code_length": "900~1024",
  "soft_quant": "무관",
  "key_contribution": "block-fading 채널에서 full diversity를 보장하는 root-check 구조를 QC/IRA/IRAA/Controlled-Doping 형태로 PEG 기반 설계하는 알고리즘 제안, PEG-LDPC 대비 FER 최대 7.5dB 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "block-fading(무선/OFDM) 채널의 다중 페이딩 다이버시티 확보가 목적으로 NAND 채널 모델과 무관, 부호 rate가 1/F(≤0.5)로 NAND ECC 대비 매우 낮음, root-check identity/dual-diagonal 구조는 fading diversity 특화 설계",
  "todo_check": "QC-PEG 알고리즘 자체(순수 girth 최대화 PEG 로직)는 root-check 제약을 제거하면 일반 QC-LDPC H-matrix 설계에 재사용 가능한지"
}
```
