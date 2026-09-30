### arxiv:2406.19664v1 - Recent Advances in Deep Learning for Channel Coding: A Survey (2024, arXiv/IEEE preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 미상 |
| 핵심기여 | DL 기반 채널코딩(부호설계+복호) 기법을 model-free/model-based로 분류·정리한 서베이 |
| HW설계 | X |
| 검증수준 | 미상 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 서베이라 단일 이식 기법 없음; 6G/무선 특화 + NN 전면대체 계열이 다수 |
| 추가확인 | 인용된 개별 원논문(예: neural NMS error-floor 제거 [332], 양자화 FAID [284]) 중 binary LDPC용만 별도 정독 |

> 총평: DL 채널코딩 전반을 폭넓게 정리한 서베이로 개별 이식 기법은 없음 — 후속 논문 발굴용 인덱스로만 가치.

### B. 알고리즘 요약

1. 대상은 특정 알고리즘이 아니라 **DL for channel coding 서베이** — LDPC/polar/turbo에 대한 DL 기반 부호설계와 복호를 총망라한다.
2. 풀려는 문제: 전통적 수학모델 기반 부호설계·복호가 실제 환경 mismatch와 6G급 복잡도에 한계 → data-driven(DL) 대안 정리.
3. 범위: (1) DL 부호설계, (2) DL 채널복호, (3) end-to-end 학습 중 앞의 둘에 집중(전면 transceiver 대체는 비현실적이라 제외).
4. §II DL 기초(MLP/CNN/RNN/GNN/Transformer/Diffusion, 학습법 transfer/meta/curriculum 등) 배경 정리.
5. §III 부호설계: irregular LDPC의 degree distribution `λ(x),ρ(x)` 최적화, polar frozen-bit 설계를 DL/RL/GNN로 대체·보강.
6. §IV 복호: model-free(MLP/Transformer/syndrome-loss) vs neural BP(가중 BP `weighted MS`, NOMS/NMS, GNN 디코더).
7. 핵심 흐름은 BP/MS를 **deep unfolding**하여 에지별 스케일/오프셋을 학습 파라미터화(neural MS/NMS)하는 것.
8. HW/복잡도 절감 계열: 가중치 양자화, weight sharing(레이어·degree 단위), pruning, TT/TR 텐서분해로 파라미터·연산 축소.
9. 결과는 개별 인용값(예: [332] neural NMS로 error-floor 제거, [682] syndrome loss로 1.1 dB 개선) 나열 — 서베이 자체의 실험 없음.
10. 저장장치 관련은 STT-MRAM용 neural RBMS/BF/MS [241][242]만 언급, NAND flash는 무관.
11. 한계: 단일 재현 대상 없음, 무선/6G 지향, NN 전면대체가 다수라 HW 고전 binary LDPC 파이프라인 직접 이식 대상 아님.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Neural BP / MS 디코더(학습 파라미터) | 대응 없음 (프로파일 §6 "NN/딥러닝 디코더") | Prime ECC는 non-learning min-sum, NN 계열 미대응 |
| LDPC degree distribution DL 최적화 | ecc_top.cpp `Load_PCM()` (H-matrix) | 부호구조 고정, DL 재설계는 재검증 부담 큼 |
| LLR/메시지 양자화 학습(FAID 등) | channel.cpp `Set_LLR_Th()` | 개념 일치하나 서베이는 학습기반, 이식은 원논문 필요 |
| 조기종료(CRC-aided) 언급 | partial_CRC.cpp `partial_crc_HW_T4()` | 이미 보유(중복) |

적용 가치: **낮음** — 서베이라 단일 이식 대상이 없고, 다루는 기법 대부분이 NN 전면대체/무선 특화로 Prime ECC의 고전 binary QC-LDPC 파이프라인과 대응이 약하다. 개별 원논문 발굴용 인덱스로만 활용.

### D. JSON 블록

```json
{
  "id": "arxiv:2406.19664v1",
  "title": "Recent Advances in Deep Learning for Channel Coding: A Survey",
  "year": 2024,
  "venue": "arXiv (cs.IT) preprint",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "미상",
  "key_contribution": "DL 기반 채널코딩(부호설계+복호) 기법을 model-free/model-based로 분류·정리한 서베이",
  "hw_designed": "X",
  "verification": "미상",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "서베이라 단일 이식 기법 없음; 6G/무선 특화 + NN 전면대체 계열이 다수",
  "todo_check": "인용된 개별 원논문 중 binary LDPC용만(neural NMS error-floor 제거, 양자화 FAID 등) 별도 정독"
}
```
