### arxiv:2509.25580v2 - Neural-Model-Augmented Hybrid NMS-OSD Decoders for Near-ML in Short Block Codes (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.87 |
| 부호length | 15~127 |
| 연판정 | soft-4bit+ |
| 핵심기여 | NMS를 1차로 두고 실패분만 OSD로 넘겨 near-ML 달성, CNN 기반 DIA·SWA·UDE 신경모델로 OSD TEP 수를 대폭 감축 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | HW 미검증(SW만), OSD의 Gaussian elimination이 GPU/HW 가속 난이·q=6 soft 필요, DIA/SWA/UDE 3개 NN 학습·튜닝 부담 |
| 추가확인 | NMS만으로 커버되는 NAND 고rate QC-LDPC에서 OSD 후단이 실제로 필요한 waterfall 영역인지, OSD의 HW latency/면적 |

> 총평: NMS가 대부분을 처리하고 소수 실패분만 OSD로 near-ML을 노리는 하이브리드로 발상은 좋으나, OSD의 GE·serial 특성과 3개 NN 학습·soft-heavy 요구가 NAND QC-LDPC HW 파이프라인에 부담이라 이식성은 중.

### B. 알고리즘 요약

1. 대상은 short linear block code(LDPC (128,64)/(49,36), BCH (63,45)~(127,99), RS binary image (15,13)~(31,29)), rate 0.5~0.87, AWGN+BPSK.
2. 문제: 유한길이 LDPC/HDPC에서 NMS는 짧은 cycle로 ML 대비 gap이 있고, OSD는 near-ML이나 TEP 수가 블록길이에 지수증가 → 둘을 순차 결합해 throughput과 near-ML을 동시에 취하려 함.
3. 모델: `SNR=-10log10(2Rσ2)`, LLR `lvi=2yi/σ2`; NMS는 flooding으로 완전병렬, OSD는 `H(2)=[I|Q2]` GE 후 TEP 탐색.
4. 핵심 기법1: 직렬 하이브리드 — 고throughput NMS가 대부분 복호, 실패 프레임만 OSD로 전달(`Chb=Cn+FnCo`).
5. 핵심 기법2 (DIA): NMS의 posterior LLR trajectory(길이 `Im+1`)를 1D-CNN으로 처리해 OSD용 bit reliability를 정제 → LDPC에서 특히 효과 큼.
6. 핵심 식: OSD 최적후보 선택 `c=argmin Σ 1(cˇi≠ci)|yi(2)|`(식6), 신뢰도 낮은 순 정렬로 MRB/LRB 분리.
7. 부수 기법 (ALMLT decoding path): Hamming weight 대신 평균신뢰도 기반 고정 TEP 순서, 경험적 counter 갱신으로 online 적응(`lw=β·lt` 버퍼).
8. 부수 기법 (SWA/UDE): SWA CNN이 sliding window로 TEP 탐색 조기종료(soft margin `sm`); UDE CNN이 패리티는 만족하나 오복호된 NMS false positive를 잡아 OSD로 전달.
9. 결과: LDPC (128,64)에서 `Iat`가 4500→600으로 급감하며 near-ML, MRB(4) 대비 0.15dB 이내이나 TEP 6.7×10^5→10^4 수준; NMS `Ian`은 SNR↑에서 9.31→1.94 iter.
10. 한계: SW 시뮬만, HW/양자화/메모리 매핑 미검증, OSD의 GE·serial이 GPU/TPU 가속 난이, 3개 보조 NN 학습·튜닝 필요.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| NMS(min-sum) 1차 복호 | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 이미 보유한 min-sum과 동일 계열, α normalization만 추가 여지 |
| posterior LLR 기반 reliability 정제(DIA), 신뢰도 정렬 | decoder.cpp `Get_VNU_Table_Idx()`, `ecc_data.h` `PARAM_LLR` | 적응형 LLR 테이블과 취지 유사하나 CNN·OSD 후단은 대응 없음 |
| UDE detector (패리티 만족 오복호 검출) | full_CRC.cpp, `partial_CRC.cpp` | Prime ECC는 CRC로 오복호를 걸러 유사 목적, NN 기반 UDE는 대응 없음 |
| OSD / SWA / ALMLT decoding path | 대응 없음 | OSD 후처리·TEP 탐색 구조 자체가 Prime ECC에 부재 |

적용 가치: **중간** — NMS 1차 + 실패분 OSD near-ML 발상과 CRC 이후 후처리 아이디어는 참고가치가 있으나, OSD의 Gaussian elimination·serial TEP 탐색과 3개 NN이 NAND QC-LDPC HW 파이프라인·soft 제약과 정합성이 낮다.

### D. JSON 블록

```json
{
  "id": "arxiv:2509.25580v2",
  "title": "Neural-Model-Augmented Hybrid NMS-OSD Decoders for Near-ML in Short Block Codes",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.5~0.87",
  "code_length": "15~127",
  "soft_quant": "soft-4bit+",
  "key_contribution": "NMS를 1차로 두고 실패분만 OSD로 넘겨 near-ML 달성, CNN 기반 DIA·SWA·UDE 신경모델로 OSD TEP 수를 대폭 감축",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "HW 미검증(SW만), OSD의 Gaussian elimination이 GPU/HW 가속 난이·q=6 soft 필요, DIA/SWA/UDE 3개 NN 학습·튜닝 부담",
  "todo_check": "NMS만으로 커버되는 NAND 고rate QC-LDPC에서 OSD 후단이 실제로 필요한 waterfall 영역인지, OSD의 HW latency/면적"
}
```
