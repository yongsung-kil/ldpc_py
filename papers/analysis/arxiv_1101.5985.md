### arxiv_1101.5985v1 - Multi-Edge type Unequal Error Protection LDPC Codes (2011, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 4096 |
| 연판정 | 무관 |
| 핵심기여 | Multi-edge type 분석으로 보호클래스 간 체크노드 연결프로파일을 LP 최적화해, 반복 증가에도 UEP 등급이 사라지지 않도록 유지 |
| HW설계 | X |
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
| 한계,주의 | 목적이 codeword 내 차등보호(UEP)로 NAND ECC(균등 최대정정)와 목표가 상반; HW 미설계, AWGN 시뮬만 |
| 추가확인 | 없음 (UEP는 NAND ECC 요구와 무관) |

> 총평: 통신용 UEP-LDPC 부호설계 이론 논문. MET 밀도진화 기반 클래스 연결프로파일 LP 최적화로 UEP 유지를 노리며, NAND 균등보호 고rate QC-LDPC와 목표가 달라 이식 가치 없음.

### B. 알고리즘 요약

1. 시스템: AWGN 채널, irregular LDPC, `n=4096`, rate 1/2, `dvmax=30`, `me=3` 보호클래스(C1=정보 20%, C2=정보 80%, C3=패리티).
2. 문제: irregular LDPC의 변수노드 차수 차이로 생기는 UEP 등급이 반복 복호가 늘면 사라짐 → 원하는 클래스별 성능차를 반복 후에도 유지하고 싶음.
3. 모델: 표준 BP, 메시지 LLR을 대칭 가우시안(분산=2×평균)으로 가정하고 밀도진화를 상호정보 `I` 궤적으로 추적.
4. 핵심 기법: multi-edge type(MET) 프레임으로 클래스별 edge type을 구분, 변수노드 다항 `L(r,x)`·체크노드 `R(x)`와 edge-perspective `λ^(j)(x)`, `ρ_d^(j)`로 표현.
5. 핵심 식: 클래스별 상호정보 진화 식 (12),(13)와 요약 `I_l^{Cj}=F(λ^(j),ρ_d^(j),σ²,...)` (식 14) — 다른 클래스에서 유입되는 정보량이 성능차를 좌우.
6. 확장: check-regular 가정, 체크노드의 edge degree vector `d=(d1,...,dme)`, `Σdi=dcmax`로 클래스 간 연결량을 조절(예 d=(4,0)은 고립→UEP 강, d=(2,2)는 연결→UEP 약화).
7. 구현: 파라미터 `maxρ_d^(j)`(체크노드 타입 상한)로 연결정도 규제, 저복잡도 체계적 인코딩 위해 하삼각형 PCM 구성, PEG 변형으로 목표 차수 실현.
8. 최적화: LP — 목적함수는 클래스 내 평균 체크노드 차수 최소화, 제약 C1~C4(단조증가 상호정보 등), 덜 보호된 클래스→가장 보호된 클래스 순차 최적화(Fig.2).
9. 결과: `maxρ_d^(2)`=0.35/0.55/0.75로 C1·C2 BER 성능차를 단일 파라미터로 조절(Fig.3), 50 반복에서도 UEP 유지(기존 [3]/[5]에서 불가/미관측).
10. 한계: 순수 부호설계 이론+AWGN 시뮬, HW·복잡도·throughput 없음; 목표가 UEP(차등보호)라 NAND 균등 ECC와 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MET 연결프로파일/차수분포 부호설계 | ecc_top.cpp `Load_PCM()` | H-matrix 로드에 닿으나 UEP-irregular라 고rate QC-LDPC와 비정합 |
| 밀도진화/상호정보 최적화(LP) | 대응 없음 | Prime ECC는 고정 QC-LDPC로 코드설계 도구 부재 |
| 하삼각형 체계적 인코딩 | encoder.cpp `Generate_PCM_encoding()` | 인코딩 구조 개념만 유사, dual-diagonal과 다름 |
| UEP 보호클래스 개념 | 대응 없음 | NAND ECC는 코드워드 균등보호 |

적용 가치: **낮음** — 목적(codeword 내 차등보호)이 NAND 균등 최대정정 ECC와 상반되고, non-QC irregular 부호설계 이론이라 Prime ECC의 고정 binary QC-LDPC에 떼어 쓸 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1101.5985v1",
  "title": "Multi-Edge type Unequal Error Protection LDPC Codes",
  "year": 2011,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "4096",
  "soft_quant": "무관",
  "key_contribution": "Multi-edge type 분석으로 보호클래스 간 체크노드 연결프로파일을 LP 최적화해 반복 증가에도 UEP 등급 유지",
  "hw_designed": "X",
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
  "caveat": "목적이 codeword 내 차등보호(UEP)로 NAND ECC(균등 최대정정)와 목표가 상반; HW 미설계, AWGN 시뮬만",
  "todo_check": "없음 (UEP는 NAND ECC 요구와 무관)"
}
```
