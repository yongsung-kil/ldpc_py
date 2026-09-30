### arxiv:2012.15297v2 - Trapping Sets of Quantum LDPC Codes (2020/2021, arXiv (Quantum journal))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.03~0.13 |
| 부호length | 254~900 |
| 연판정 | 무관 |
| 핵심기여 | 양자 QLDPC 부호(CSS 계열)의 syndrome 기반 반복복호 실패를 classical-type TS와 symmetric stabilizer TS 두 종류로 체계화하고, QC 구성법·column-layered 스케줄로 error-floor를 후처리 없이 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 대상이 QLDPC(양자 stabilizer, GF(4)/CSS 부호)이며 degenerate error·symmetric stabilizer 등 양자 고유 실패 모드 분석이라 binary NAND LDPC의 trapping-set 개념과 직접 대응되지 않음 |
| 추가확인 | column-layered(serial) 스케줄이 symmetric stabilizer TS를 깨는 메커니즘이 classical binary LDPC의 일반 trapping-set(예: (a,b) TS)에도 유사하게 적용 가능한지, 또는 이미 고전 LDPC 문헌(FAID, layered decoding)에 포함된 결과인지 확인 필요 |

> 총평: 양자 QLDPC의 trapping-set 이론을 체계화한 연구로, error-floor를 후처리 없이 스케줄만으로 개선하는 아이디어는 흥미로우나 부호 모델이 CSS/GF(4) 양자 stabilizer 전용이라 binary NAND LDPC로의 직접 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 CSS 계열 QLDPC 부호(bicycle, generalized bicycle, hypergraph-product(HP) 코드), stabilizer matrix `H_b = [H_X|H_Z]`, syndrome `σ=[σX,σZ]`을 이용한 syndrome 기반 반복복호(Gallager-B/BP/MSA).
2. 풀려는 문제: 유한길이 QLDPC 복호기가 짧은 cycle과 대칭적 degenerate error(고전 부호엔 없는 개념) 때문에 error-floor를 겪고, 기존 완화책(OSD 후처리)은 복잡도가 코드 차원에 3차로 증가해 HW 비현실적.
3. 핵심 가정: syndrome 기반 반복복호기 `D_s`가 X/Z 오류를 독립 BSC(교차확률 `2p/3`)로 처리한다고 가정, symplectic inner product(SIP) 제약 `H_X H_Z^T + H_Z H_X^T = 0`으로 Tanner graph에 불가피한 cycle 존재.
4. 핵심 기법 1단: 고전 trapping set 정의(Def.1, `(a,b)` TS)를 syndrome 복호 시나리오로 일반화한 `quantum trapping set(QTS)`(Def.4) 정의, classical-type TS와 `symmetric stabilizer TS`(Def.5: 홀수차수 check 없이 두 대칭 부분그래프로 분할 가능) 두 클래스로 분류.
5. 핵심 통찰: symmetric stabilizer 위의 두 degenerate error 패턴 `e, f`가 대칭적 update rule을 쓰는 복호기에서 동시에 수렴 시도되어 `e⊕f`(stabilizer)로 진동, 복호 실패를 일으킴(Lemma 1,2).
6. 확장 1: QC 구성 constituent 코드로 HP 코드를 만들어 (4,2)/(4,4)/(5,1) 등 저weight harmful TS를 제거 → 무작위 구성 대비 error-floor 영역 FER 약 1자릿수 개선(flooding BP, 100 iteration).
7. 확장 2: column-layered(serial) MSA 스케줄로 symmetric stabilizer의 대칭성을 깨뜨려 A1[[254,28]] 코드에서 flooding 대비 error-floor 영역 FER 2자릿수 개선(동일 iteration 수 `l_max=20`), 별도 post-processing/random perturbation 없이 달성(random perturbation 방식은 총 1700 iteration 필요한 것과 대비).
8. 학습/최적화 절차 없음(TS 탐색은 고전 LDPC의 sub-graph 탐색 알고리즘 재사용, GA/NN 아님).
9. 결과 수치: HP 코드 QC 구성 시 FER 약 1자릿수(p≈0.005) 개선, A1[[254,28]] layered MSA 시 error-floor 2자릿수 개선(동일 iteration으로 latency 개선 효과).
10. 한계: 순수 컴퓨터 시뮬레이션(HW 미설계, gate count/throughput 없음), GF(4)/CSS 양자 stabilizer 부호 전용이며 degenerate error·symmetric stabilizer는 고전 binary LDPC에 존재하지 않는 개념.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Quantum trapping set(QTS)/symmetric stabilizer 정의·탐색 | 대응 없음 | 양자 stabilizer·degenerate error 고유 개념, binary QC-LDPC에 대응 구조 없음 |
| QC 구성으로 harmful TS 제거 (부호설계) | `ecc_top.cpp` `Load_PCM()` | 저weight trapping-set 회피라는 "부호설계 시 TS 배제" 아이디어 방향성만 참고 가능 |
| column-layered(serial) MSA 스케줄 | `decoder.cpp` `LDPC_Decoder()` (Dual-Update 옵션) | 이미 Dual-Update(odd/even 교대) 스케줄 보유, serial 스케줄 개념 자체는 중복 |
| Min-sum algorithm(MSA) 반복복호 | `decoder.cpp` `CNU_Update_New_Mag()` | 개념(MSA)은 이미 보유, 본 논문의 기여는 QLDPC 특화 스케줄·부호설계이지 MSA 자체 개선 아님 |

> 적용 가치: 낮음 — 양자 CSS/QLDPC 전용 trapping-set 이론이며 symmetric stabilizer/degenerate error는 binary NAND LDPC에 대응 개념이 없고, layered 스케줄·QC 부호설계 아이디어는 이미 Prime ECC가 유사 기법(Dual-Update, QC-LDPC)을 보유해 중복.

### D. JSON 블록

```json
{
  "id": "arxiv:2012.15297v2",
  "title": "Trapping Sets of Quantum LDPC Codes",
  "year": 2020,
  "venue": "arXiv (Quantum journal)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": "0.03~0.13",
  "code_length": "254~900",
  "soft_quant": "무관",
  "key_contribution": "양자 QLDPC 부호(CSS 계열)의 syndrome 기반 반복복호 실패를 classical-type TS와 symmetric stabilizer TS 두 종류로 체계화하고, QC 구성법·column-layered 스케줄로 error-floor를 후처리 없이 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "대상이 QLDPC(양자 stabilizer, GF(4)/CSS 부호)이며 degenerate error·symmetric stabilizer 등 양자 고유 실패 모드 분석이라 binary NAND LDPC의 trapping-set 개념과 직접 대응되지 않음",
  "todo_check": "column-layered(serial) 스케줄이 symmetric stabilizer TS를 깨는 메커니즘이 classical binary LDPC의 일반 trapping-set(예: (a,b) TS)에도 유사하게 적용 가능한지, 또는 이미 고전 LDPC 문헌(FAID, layered decoding)에 포함된 결과인지 확인 필요"
}
```
