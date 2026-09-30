### arxiv:1501.05595v1 - Protograph-Based LDPC Code Design for Bit-Metric Decoding (2015, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.5~0.83 |
| 부호length | 16200~64800 |
| 연판정 | soft-4bit+ |
| 핵심기여 | BICM 고차 ASK 변조의 서로 다른 비트채널을 biAWGN surrogate로 근사하고 PEXIT+differential evolution으로 protograph base matrix를 최적화해 bit-metric decoding에 맞춘 LDPC 부호 설계. |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 고차 ASK(4/16/64-ASK) BICM 채널과 확률적 셰이핑을 전제로 한 부호 설계로 NAND의 binary hard/soft channel과 직결되지 않음; 순수 이론/시뮬(FER) 결과, HW 미설계, 100회 반복 시뮬로 iteration 효율성도 다루지 않음. |
| 추가확인 | 최적화된 base matrix의 실제 최종 부호율/길이가 NAND ECC급(~0.9) 고rate 대역과 겹치는지 확인 필요. |

> 총평: 고차 변조(BICM) 환경을 위한 protograph LDPC 부호 설계 논문으로, NAND binary LDPC ECC와는 채널·목적이 달라 이식 가치가 낮다.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템은 BICM(bit-interleaved coded modulation) 위에서 m-비트 레벨 고차 ASK(4/16/64-ASK) 변조를 사용하고, bit-metric decoding(BMD)으로 m개의 병렬 비트채널을 각각 복호한다.
2. 문제: LDPC 부호의 서로 다른 variable node가 서로 다른 비트채널(레벨별 신뢰도 상이)에 매핑될 때, 기존 MET(multi-edge-type) 코드 설계는 비트채널 3개 이상에서 EXIT 차트 최적화 시간이 급격히 증가.
3. 채널 모델은 AWGN 위의 m-ASK 성상이며, 각 비트레벨 `Bi`의 L-value `Li = log(P(Bi=0|y)/P(Bi=1|y))`로 정의되는 병렬 비트채널로 관측.
4. 핵심 기법: 각 비트채널을 rate-backoff `R*-R`이 동일한 biAWGN surrogate 채널(`σ_Bi`)로 근사, protograph base matrix `A ∈ {0,...,S}^(e×f)`에 differential evolution(DE)을 적용해 PEXIT 임계값을 최소화.
5. 핵심 식: surrogate 채널 조건 `Σ H(Bi|Li) = Σ H(B̃i|Ỹi)` (식 15) — 원 채널과 동일한 rate backoff를 갖도록 surrogate 분산 `σ_Bi`를 정함, PEXIT는 `(V_k,C_l)` 쌍별 extrinsic mutual information을 추적.
6. 확장: 확률적 셰이핑(probabilistic shaping, Böcherer 방식) 입력에도 동일 설계 절차 적용 - distribution matcher + systematic (m-1)/m rate 인코더로 capacity-achieving 분포 근사.
7. 부수 트릭: BRGC(binary reflected Gray code) 라벨링 사용, 최대 병렬 edge 수 `S`로 variable node degree(`e·S`) 및 탐색공간 크기 제어.
8. 최적화 절차: PEXIT 분석(협대역 EXIT를 protograph로 확장)으로 임계값 계산 후 differential evolution으로 base matrix 반복 탐색.
9. 결과: rate 1/2, 3/4 4-ASK 부호가 기존 MET 코드[Zhang&Kschischang]와 동등/약간 우수한 BER/FER 성능(블록길이 16200); 64-ASK 셰이핑 부호(블록길이 64800)는 스펙트럼 효율 4.2 bits/ch.use에서 채널용량 대비 0.69dB 이내(FER=10^-3).
10. 한계: 순수 알고리즘/시뮬 결과이며 HW 설계 없음, 100회 고정 반복 시뮬레이션만 수행해 iteration 효율/복잡도 논의 없음, 고차 ASK/BICM 특화 설계로 binary hard-decision NAND 채널과는 목적이 다름.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Protograph base matrix 설계(DE+PEXIT) | `ecc_top.cpp` `Load_PCM()` | 특정 QC-LDPC(z=32, N_b=129) 고정 구조라 이식 난이도 높음(§4 부호설계=높음), BICM 특화라 실익 낮음 |
| biAWGN surrogate LLR 설계 | `channel.cpp` `Set_R_Offset()`, `Set_LLR_Th()` | 채널이 AWGN 기반이라 형식적 유사성은 있으나 고차 ASK 비트채널 근사는 NAND read 채널과 무관 |
| PEXIT/DE 최적화 절차 | 대응 없음 | Prime ECC는 고정 H-matrix 시뮬레이터로 부호 최적화 도구 자체가 없음 |

> 적용 가치: 낮음 — BICM 고차 변조를 위한 protograph 설계 방법론으로, NAND binary QC-LDPC의 고rate 부호설계나 디코더/HW 개선과 직접 연결되는 요소가 없음.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1501.05595v1",
  "title": "Protograph-Based LDPC Code Design for Bit-Metric Decoding",
  "year": 2015,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": "0.5~0.83",
  "code_length": "16200~64800",
  "soft_quant": "soft-4bit+",
  "key_contribution": "BICM 고차 ASK 변조의 서로 다른 비트채널을 biAWGN surrogate로 근사하고 PEXIT+differential evolution으로 protograph base matrix를 최적화해 bit-metric decoding에 맞춘 LDPC 부호 설계.",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "고차 ASK(4/16/64-ASK) BICM 채널과 확률적 셰이핑을 전제로 한 부호 설계로 NAND의 binary hard/soft channel과 직결되지 않음; 순수 이론/시뮬(FER) 결과, HW 미설계, 100회 반복 시뮬로 iteration 효율성도 다루지 않음.",
  "todo_check": "최적화된 base matrix의 실제 최종 부호율/길이가 NAND ECC급(~0.9) 고rate 대역과 겹치는지 확인 필요."
}
```
