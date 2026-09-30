### arxiv:2310.07129v2 - The impact when neural min-sum variant meets ordered statistics decoding of LDPC codes (2024, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.83 |
| 부호length | 128~1056 |
| 연판정 | soft-4bit+ |
| 핵심기여 | neural min-sum(NMS-1) + 적응형 OSD post-processing 하이브리드에 DIA(CNN)·TEP 그룹화·iteration diversity를 결합해 저복잡도·채널불변으로 ML FER에 근접 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | NN 학습(NMS 가중치+CNN DIA)+직렬 OSD(TEP 수천~수십만 탐색) 기반 short/moderate 부호 전용 - NAND 고rate·HW min-sum 파이프라인과 부적합 |
| 추가확인 | 채널불변(σ² 불요) 정규화 min-sum 가중치 학습 결과가 NAND 고rate QC-LDPC min-sum 성능에 기여하는지(OSD 제외) |

> 총평: NMS+OSD 하이브리드로 short 부호에서 ML급 FER을 저비용으로 달성하나, NN 학습+직렬 OSD라 NAND HW min-sum에 이식 불가로 이식성 하.

### B. 알고리즘 요약

1. 시스템: binary LDPC, BPSK+AWGN, `li = 2yi/σ²`; 대상 부호 CCSDS(128,64), WiMAX-like(384,192), 802.16(1056,880), rate 0.5~0.83, block 128~1056(short~moderate).
2. 문제: min-sum은 BP 대비 성능손실, OSD는 ML급이나 채널분산 `σ²` 필요·직렬처리 병목; 두 방법을 하이브리드해 저복잡도·고throughput·채널불변·ML근접 FER을 동시 추구.
3. 모델: 복호 실패시 MRB(most reliable basis) 상 hard-decision과 정답의 불일치를 authentic error pattern으로 정의, OSD가 이를 TEP 탐색으로 복원.
4. 핵심 기법1(NMS 설계): GNN permutation-invariance 관점에서 `x_v→c = ζ1·li + Σ...`, `x_c→v = ζ3·s·ϕ`(min-term)로 파라미터화; NMS-1(ζ3만 학습, ζ1=ζ2=1)이 최적 - 모든 NMS 변형이 성능 무차별.
5. 핵심 식: OSD 최적추정 `c = argmin Σ 1(č_i≠ĉ_i)|y_i|` (Eq.9) - 후보 부호어 중 비트반전 신뢰도합 최소 선택.
6. 핵심 기법2(적응형 OSD): TEP를 order pattern으로 그룹화(균등분할 / GE swap 수 `ρs` 기반 동적분할 `0,d1,d2,d3)`), 우선순위는 authentic error pattern 통계로 경험적 결정.
7. 구현 디테일: DIA(Decoding Information Aggregation)를 2~4층 CNN(파라미터<200)으로 구현해 새 비트신뢰도 합성, MRB 오류를 앞쪽에 집중; auxiliary criterion으로 TEP 리스트 축소.
8. 학습: NMS는 누적 cross-entropy loss+Adam(lr 0.01, 0.95 decay), 채널불변이라 min-sum은 `y_i`만 필요; iteration diversity - 실패 궤적을 여러 그룹으로 분할해 작은 DIA 모델 다수로 diversity gain.
9. 결과: (128,64) NMS-OSD(Gr=200)이 ML 대비 0.2dB 이내; (384,192) Gr=80이 BP보다 0.4dB 우위(FER=1e-3); TEP 탐색수 conventional order-3 대비 (384,192)에서 100만→7738~13451로 대폭 감소.
10. 한계: TensorFlow/Colab 시뮬만(HW 미설계), NN 학습 의존, OSD 직렬탐색이 부호길이·rate 증가시 급증(1056,880에서 dynamic-TEP도 ML 대비 0.25dB+ gap), short~moderate 부호 한정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| neural min-sum(NMS-1=정규화 MS) | [decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | min-sum 자체는 이미 보유(중복), NN 학습 가중치 도입은 구조상 부적합 |
| ζ3 min-term scaling(정규화 계수) | ecc_data.h `PARAM_LLR`, decoder.cpp `Get_VNU_Table_Idx()` | scaling 개념은 대응 가능하나 학습기반이라 magnitude 양자화 테이블과 접목 부담 |
| OSD post-processing(GE+TEP 탐색) | 대응 없음 | 직렬 ML근사 후처리로 NAND HW 파이프라인에 없음 |
| DIA(CNN 신뢰도 합성)/NN 디코더 | 대응 없음 | 딥러닝 디코더는 프로파일상 명시적 대응 없음 |
| 조기종료(c·H'=0) | partial_CRC.cpp `partial_crc_HW_T4()`, full_CRC.cpp | 조기종료 개념은 유사하나 Prime ECC는 CRC 기반으로 이미 보유 |

적용 가치: **낮음** - min-sum은 이미 보유 기법이고 핵심 신규성인 NN 학습·직렬 OSD·CNN DIA는 NAND HW min-sum 코드베이스에 대응 요소가 없어 이식 불가.

### D. JSON 블록

```json
{
  "id": "arxiv:2310.07129v2",
  "title": "The impact when neural min-sum variant meets ordered statistics decoding of LDPC codes",
  "year": 2024,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.5~0.83",
  "code_length": "128~1056",
  "soft_quant": "soft-4bit+",
  "key_contribution": "neural min-sum(NMS-1) + 적응형 OSD post-processing 하이브리드에 DIA(CNN)·TEP 그룹화·iteration diversity를 결합해 저복잡도·채널불변으로 ML FER에 근접",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "NN 학습(NMS 가중치+CNN DIA)+직렬 OSD(TEP 수천~수십만 탐색) 기반 short/moderate 부호 전용 - NAND 고rate·HW min-sum 파이프라인과 부적합",
  "todo_check": "채널불변(σ² 불요) 정규화 min-sum 가중치 학습 결과가 NAND 고rate QC-LDPC min-sum 성능에 기여하는지(OSD 제외)"
}
```
