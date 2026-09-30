### arxiv:2212.06985v3 - Local Probabilistic Decoding of a Quantum Code (2023, Quantum)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 3D toric(양자 CSS/LDPC) 코드에 flip/p-flip(확률적 국소 flip)+BP 하이브리드(p-BP)로 O(1) 병렬 국소 디코딩, threshold ~5.46% 달성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 양자 CSS/토릭 코드 전용(syndrome degeneracy·stabiliser 절반 오류 대응)으로 고전 binary NAND LDPC와 무관 |
| 추가확인 | 없음 (양자 QEC 도메인, 이식 대상 아님) |

> 총평: 3D toric 양자 코드의 국소 확률적 디코더(flip/p-flip+BP) 연구 — 양자 QEC 특유의 degeneracy/stabiliser 문제를 다뤄 고전 binary NAND QC-LDPC ECC에 이식 대상이 아님.

### B. 알고리즘 요약

1. 시스템: 3D toric code(3DTC, `[[3L^3,3,L]]`)의 X-오류 복호를 dual lattice에서 고전 디코딩 2문제로 환원(CSS).
2. 문제: 양자 코드 syndrome은 degenerate — stabiliser 절반 무게 오류 등은 고전 디코더가 두 등가 보정 중 못 고름, 보통 수정/조합 필요.
3. 모델: phenomenological noise(qubit X-error `p` = Z-stabiliser 측정오류 `q`), 1000/500 code cycle 후 logical Z 다수결 판정.
4. 핵심 기법 flip: 각 bit에서 `|UNSAT(b)|>|SAT(b)|`이면 flip(Sipser-Spielman), 병렬판은 O(1) 시간; 3DTC X-오류 syndrome이 looplike라 효과적.
5. 관찰: 최저무게 uncorrectable 오류가 correctable에 Hamming 거리상 더 가까워, 추가 noise가 이를 correctable로 바꿀 확률이 높음(threshold ~2.6%).
6. p-flip: `|SAT|=|UNSAT|`인 tie bit를 확률 0.5로 flip → uncorrectable 오류를 확률적으로 정정(4DTC 국소 recovery와 거의 동일).
7. BP: Tanner graph에서 `tanh` 기반 message-passing(식2~4), 단 국소 BP는 고정 iteration 후 `li<0` bit 보정(정확 수렴 기대 안 함), 측정오류는 factor당 변수노드 추가로 흡수.
8. 스케줄 최적화: nA(적용횟수)·λp(p-flip 상대빈도) 튜닝(Table 1); p-BP는 BP 20iter 후 p-flip→flip×2→p-flip→flip×2.
9. 결과: BP 단독 ~5.1%, p-BP ~5.46% threshold — BP+OSD(~7.1%, O(n^3)) 대비 3/4 수준이나 완전 국소·O(1) 병렬 런타임; CUDA/GPU 시뮬.
10. 한계: HW 미설계·GPU 시뮬만, sustainable threshold 미증명, 양자 QEC 전용(고전 NAND 무관).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP(`tanh` full Sum-Product) 메시지 전달 | 대응 없음 | 우리는 min-sum 근사 사용, full-`tanh` Sum-Product는 프로파일상 대응 없음 |
| flip/p-flip 국소 확률적 디코더 | 대응 없음 | 고전 bit-flip류이나 양자 syndrome degeneracy 대응이 목적, NAND용 아님 |
| 양자 CSS/toric 코드 구조 | 대응 없음 | non-binary/양자 LDPC — 판정 필터상 이식성 하 |

적용 가치: 낮음 — 양자 3D toric 코드용 국소 디코더 연구로, binary NAND QC-LDPC 부호설계/디코더/HW 어느 계층에도 대응이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2212.06985v3",
  "title": "Local Probabilistic Decoding of a Quantum Code",
  "year": 2023,
  "venue": "Quantum",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "미상",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "3D toric 양자 CSS/LDPC 코드에 flip/p-flip+BP 하이브리드(p-BP)로 O(1) 병렬 국소 디코딩, threshold ~5.46%",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "하",
  "caveat": "양자 CSS/토릭 코드 전용(syndrome degeneracy·stabiliser 절반 오류)으로 고전 binary NAND LDPC와 무관",
  "todo_check": "없음 (양자 QEC 도메인, 이식 대상 아님)"
}
```
