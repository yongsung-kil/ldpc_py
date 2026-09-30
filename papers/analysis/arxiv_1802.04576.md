### arxiv:1802.04576v1 - Polar-Coded Forward Error Correction for MLC NAND Flash Memory (2018, SCIENCE CHINA Information Sciences)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 직접 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 0.875 |
| 부호length | 8192 |
| 연판정 | soft-2~3bit |
| 핵심기여 | MLC NAND용 polar code 기반 pre-check(binary/quantized-soft/pure-soft 3디코더) + SMMI 양자화 경계 + Gray 매핑 최적성 증명 |
| HW설계 | O |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 부호가 polar code(SC decoder)이며 LDPC는 비교 baseline일 뿐 → binary LDPC 디코더에 직접 이식 불가 |
| 추가확인 | SMMI/Gray 매핑·soft-read 경계 설계 개념은 채널 LLR 양자화 관점에서만 참고 가능(polar 종속성 배제 필요) |

> 총평: NAND 타깃이지만 코어가 polar code라 Prime ECC(binary QC-LDPC)엔 디코더·부호 모두 대응 없음. SMMI 양자화 경계·Gray 매핑 개념만 채널 LLR 설계에 간접 참고.

### B. 알고리즘 요약

1. 대상: 2-bit/cell MLC NAND, 4-Gaussian 전압분포 모델, `(8192,7168)` polar code(rate 0.875), baseline은 동일 크기 QC-LDPC bit-flipping.
2. 문제: soft LDPC(min-sum/BP)는 복잡도 높음 → polar code로 `O(N log N)` 저복잡도 대체 제안.
3. pre-check scheme: cell 왜곡 수준(`PE` threshold)에 따라 binary-input / quantized-soft / pure-soft 3개 SC polar decoder를 SSD 수명단계별로 선택.
4. LLR-based min-sum SC 복호(식 1~4), `uˆi`는 LLR 부호로 결정, frozen bit는 0.
5. Lemma 1: polar codeword는 0/1 개수 동일한 balanced code → `p(bi=1)/p(bi=0)=1`, Bayes로 LLR 정의(식 9~11).
6. binary-input decoder: 전압검출기의 1-bit hard 결과를 부호비트로 사용, LLR magnitude 무시 → adder-subtractor 없이 단일 XOR·조합논리 PE로 구현(2-bit 2's complement).
7. SMMI: MSB/LSB 별도로 상호정보 `I(X;Y)=H(Y)-H(Y|X)` 최대화해 양자화 경계 `q_i` 산출(탐색 없이). MMI[23]를 비트단위로 개선.
8. quantized-soft: constant-ratio 경계식(식 12~13) 재유도([11] 오류 정정), Q-function으로 LLR 계산(식 17~18).
9. 결과: binary-input polar가 hard-decision bit-flipping LDPC보다 우수, sensing 늘리면 quantized-soft가 더 많은 오류정정. Gray 매핑이 최적(Appendix A 증명). 복잡도 `N log N/2` 2-bit 덧셈+XOR로 LDPC LBP보다 낮음.
10. 한계: HW는 PE 구조 제시뿐(gatecount/throughput 없음), 시뮬만, 코어가 polar code라 LDPC 파이프라인과 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC polar decoder (binary/soft) | 대응 없음 | polar/turbo류는 프로파일 상 "대응 없음" |
| SMMI 양자화 경계 / soft-read | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | 채널 LLR threshold 설계 관점에서만 개념 참고 |
| Gray 매핑 / MLC 전압모델 | 대응 없음 | NAND 매핑은 컨트롤러 상위단, 디코더 코드 무관 |

적용 가치: **낮음** — 부호가 polar code라 Prime ECC의 binary QC-LDPC 디코더/인코더/부호설계 어디에도 이식 불가. SMMI·soft-read 경계 최적화 아이디어만 채널 LLR 양자화 설계에 간접 참고 여지.

### D. JSON

```json
{
  "id": "arxiv:1802.04576v1",
  "title": "Polar-Coded Forward Error Correction for MLC NAND Flash Memory",
  "year": 2018,
  "venue": "SCIENCE CHINA Information Sciences (arXiv cs.AR)",
  "portability": "하",
  "nand_relevance": "직접",
  "target": "other",
  "code_type": "기타",
  "code_rate": 0.875,
  "code_length": "8192",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "MLC NAND용 polar code 기반 pre-check(binary/quantized-soft/pure-soft 3디코더) + SMMI 양자화 경계 + Gray 매핑 최적성 증명",
  "hw_designed": "O",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "부호가 polar code(SC decoder)이며 LDPC는 비교 baseline일 뿐 → binary LDPC 디코더에 직접 이식 불가",
  "todo_check": "SMMI/Gray 매핑·soft-read 경계 설계 개념은 채널 LLR 양자화 관점에서만 참고 가능(polar 종속성 배제 필요)"
}
```
