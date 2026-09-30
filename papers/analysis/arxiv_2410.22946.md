### arxiv:2410.22946v1 - KALAM: toolKit for Automating high-Level synthesis of Analog computing systeMs (2024, arXiv eess.SY)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | regular |
| 부호rate | 0.25 |
| 부호length | 32 |
| 연판정 | 무관 |
| 핵심기여 | factor graph 입력을 Margin Propagation 아날로그 회로 SPICE netlist로 자동 합성하는 툴(KALAM) |
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
| 한계,주의 | 아날로그 MP 회로 EDA 툴 논문, binary QC-LDPC 디지털 디코더와 무관, LDPC는 데모 사례일 뿐 |
| 추가확인 | 없음(NAND ECC 이식 여지 없음) |

> 총평: 아날로그 Margin Propagation 회로를 factor graph에서 SPICE netlist로 자동 합성하는 EDA 툴 논문으로, LDPC는 여러 데모 중 하나에 불과하며 NAND용 디지털 binary QC-LDPC ECC에는 이식 가치가 없다.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: Margin Propagation(MP) 아날로그 컴퓨팅 회로의 고수준 합성 자동화 툴 KALAM(Python 기반).
2. 문제: MP 아날로그 설계는 확장성·모듈성이 좋으나 디지털 같은 자동 합성/검증 프레임워크 부재로 채택이 저조.
3. 모델: 시스템을 factor graph(변수노드 V, factor노드 F, 식 1의 결합확률 분해)로 표현.
4. 기법 5단 흐름: (1)factor graph 생성 -> (2)computational graph(변수 소거·수식 단순화) -> (3)아날로그 회로 매핑(MP 표준셀 라이브러리) -> (4)netlist 생성 -> (5)SPICE 기능 검증.
5. 핵심: MP 표준셀로 비선형 monotonic 함수를 piecewise-linear spline 근사, spline 수↑=정확도↑·면적 penalty.
6. LDPC 데모: [2]의 MP 기반 LDPC 디코더(SPA 메시지 식 2/3)를 툴로 재현, `(32,8)` regular(변수노드 degree 3, factor노드 degree 4).
7. 부호 확장: 32-bit -> 64/96-bit는 protograph 기법으로 확장, netlist runtime 32/39/51ms.
8. 다른 데모: Bayesian network 5종(정확도 SW와 거의 동일), IRIS ANN(SW 90.5% vs netlist 90%).
9. 결과: LDPC netlist의 BER/FER가 SW 결과와 강하게 일치, 전체 netlist 생성 <1s.
10. 한계: 아날로그 MP 회로 자동화 툴이 본질이며 LDPC는 검증 사례일 뿐, 디지털 ECC 디코더 알고리즘/HW 개선 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MP 아날로그 SPA LDPC 디코더 | 대응 없음 | 아날로그 연속시간 MP 회로로, 우리 디지털 min-sum bit-exact 시뮬과 패러다임 불일치 |
| factor graph -> SPICE netlist 자동합성 툴 | 대응 없음 | EDA 자동화 흐름으로 ECC 알고리즘/부호설계와 무관 |
| protograph 부호 확장 | 대응 없음 | 언급뿐이며 QC-LDPC H-matrix 구성법 제시 없음 |

적용 가치: **낮음** - 아날로그 MP 회로 합성 EDA 툴로, NAND용 디지털 binary QC-LDPC ECC의 부호설계/디코더/HW 어느 레이어에도 이식할 요소가 없다.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:2410.22946v1",
  "title": "KALAM: toolKit for Automating high-Level synthesis of Analog computing systeMs",
  "year": 2024,
  "venue": "arXiv eess.SY",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "regular",
  "code_rate": 0.25,
  "code_length": "32",
  "soft_quant": "무관",
  "key_contribution": "factor graph 입력을 Margin Propagation 아날로그 회로 SPICE netlist로 자동 합성하는 툴(KALAM)",
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
  "caveat": "아날로그 MP 회로 EDA 툴 논문, binary QC-LDPC 디지털 디코더와 무관, LDPC는 데모 사례일 뿐",
  "todo_check": "없음(NAND ECC 이식 여지 없음)"
}
```
