### arxiv:2206.11532v1 - Reducing the Error Floor of the Sign-Preserving Min-Sum LDPC Decoder via Message Weighting of Low-Degree Variable Nodes (2022, arXiv cs.IT / ECOC 형식)

| 카테고리 | 값 |
|---|---|
| 이식성 | 상 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.826 |
| 부호length | 17664 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 강양자화 SP-MS의 degree-3 VN에만 iteration-의존 CN-to-VN 가중(shift-and-add)으로 error floor 3자릿수↓ |
| HW설계 | O |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 상 |
| 한계,주의 | 시뮬만(FPGA/ASIC 미검증), 가중치가 random-search+SNR별 최적화라 코드/채널 의존, EPON 광통신 코드 대상 |
| 추가확인 | Prime ECC의 punctured degree 9/7 col 및 z=32 QC 구조에서 low-degree VN 가중 필요성과 weight 테이블 재최적화 |

> 총평: 강양자화 min-sum의 error floor를 저degree VN 한정 shift-and-add 가중으로 낮추는 HW-friendly 기법으로, Prime ECC의 hard/2SD/3SD min-sum 파이프라인에 iteration별 LLR/가중 테이블로 이식성 높음.

### B. 알고리즘 요약

1. 시스템: BPSK/AWGN, IEEE 802.3ca EPON irregular LDPC `N=17664`, `R=0.826`, 광통신용. LLR은 4bit 양자화(`α` scaling으로 채널LLR→In 매핑).
2. 문제: 저복잡도 SP-MS(Sign-Preserving MS)를 `q=2,3` bit(alphabet 4/8)로 강양자화하면 채널LLR(4bit)과 내부 메시지 alphabet 불일치로 error floor 발생(q=2 BER≈1e-3, q=3≈1e-6).
3. 원인 규명: floor는 EPON 코드의 degree-3 VN(전체의 약 72%) 때문 — low-degree VN은 incoming 메시지가 적어 나쁜 채널LLR을 극복 못 함.
4. 핵심 기법: SP-MS VN update(식2)에 iteration-의존 가중 `wn(ℓ)`를 CN-to-VN 메시지에 곱해 반복이 진행될수록 incoming 메시지 비중을 키움(`wn=1`이면 원 SP-MS).
5. 식 의미: `μ(v→c)`는 sign-preserving factor(erased 메시지 방지), `Ψ`는 offset `ϕv` 적용 후 alphabet `2^(q-1)-1`로 saturate.
6. 선택적 적용: 가중은 degree-3 VN에만 적용 → 복잡도 절감 + `α` 재최적화 불필요, 이론(conjecture) 증명 겸용.
7. HW 친화: weight를 최대 3개 power-of-two 합으로 제한(3bit 표현) → 곱셈을 shift-and-add로 대체, 첫 4 iteration은 w=1이라 나머지 8 iteration만 shift-add.
8. 최적화: weight vector는 random candidate 중 최저 BER/FER 선택, 단조 제약 `0<wn(ℓ)≤wn(ℓ+1)`, q=3은 SNR 2.8dB, q=2는 3.1dB에서 최적화(Tab.1).
9. 결과: degree-3 VN에 3bit weight 적용 시 error floor를 3자릿수 이상 감소(BER 그래프 ×5.2·10^3, ×3.4·10^3 등), max 12 iteration.
10. 한계: 시뮬만(HW-friendly 설계이나 FPGA/ASIC 미검증), weight가 코드·SNR 종속, floor 근본원인(더 낮은 BER)은 미해결로 향후과제.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SP-MS VN update 가중 wn(ℓ) | decoder.cpp `VN_Cal_HD()` 등, `Get_VNU_Table_Idx()` | iteration별 VN 처리에 저degree 한정 가중 삽입 — Prime ECC VN 루프에 직접 대응 |
| iteration-의존 weight 테이블 | ecc_data.h `PARAM_LLR`, decoder.cpp `Get_VNU_Table_Idx()` | Prime ECC의 iteration 구간별 LLR 테이블과 동일 메커니즘, weight 테이블 추가로 이식 |
| min-sum CN update/offset ϕv | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | SP-MS도 min1/min2+sign 계열, Prime ECC min-sun과 정합 |
| LLR 양자화 α scaling | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | 4bit LLR→저bit 메시지 매핑이 Prime ECC soft-read 양자화와 대응 |
| shift-and-add weight(power-of-2) | decoder.cpp `CNU_Update_New_Mag()` | HW-friendly 가중을 magnitude 양자화 테이블에 반영 가능 |

적용 가치: **높음** — 강양자화 min-sum의 error-floor를 저degree VN 한정 iteration별 shift-and-add 가중으로 낮추는 기법은 Prime ECC의 hard/2SD/3SD 저bit 파이프라인과 punctured 저degree col 구조에 직접 부합하며, weight 테이블만 추가하면 이식 가능.

### D. JSON 블록

```json
{
  "id": "arxiv:2206.11532v1",
  "title": "Reducing the Error Floor of the Sign-Preserving Min-Sum LDPC Decoder via Message Weighting of Low-Degree Variable Nodes",
  "year": 2022,
  "venue": "arXiv cs.IT (ECOC 형식)",
  "portability": "상",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.826,
  "code_length": "17664",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "강양자화 SP-MS의 degree-3 VN에만 iteration-의존 가중(shift-and-add)으로 error floor 3자릿수 감소",
  "hw_designed": "O",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "상",
  "caveat": "시뮬만(FPGA/ASIC 미검증), weight가 random-search+SNR/코드 종속, EPON 광통신 코드 대상",
  "todo_check": "Prime ECC punctured 저degree col·z=32 QC 구조에서 low-degree VN 가중 필요성과 weight 테이블 재최적화 확인"
}
```
