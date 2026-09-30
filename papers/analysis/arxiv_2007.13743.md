### arxiv:2007.13743v2 - Super-simple (v, 5, 2) directed designs and their smallest defining sets with its application in LDPC codes (2020, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 미상 |
| 부호length | 42~3406(예제별 상이, 블록 수 기준) |
| 연판정 | 무관 |
| 핵심기여 | super-simple (v,5,2) directed design의 존재성을 재귀·직접 구성으로 증명하고, 이를 이용해 girth≥6(예제는 8)인 trade-based irregular LDPC 부호의 parity-check 행렬을 구성 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 조합 설계론(design theory) 순수 수학 논문으로 BER/error-floor/복호 성능 실험이 전무하며, 부호 예제도 매우 작은 length(42~3406) 위주라 실용 NAND ECC rate/length와 무관 |
| 추가확인 | girth-8 보증 특성이 error-floor 개선에 실질적으로 기여하는지 정량 검증 필요(본문엔 이론적 girth 증명만 존재) |

> 총평: LDPC는 부록성 응용 사례로만 등장하는 조합 설계론(directed design) 논문으로, 정정능력·HW·복잡도 관련 실험이 전혀 없어 NAND ECC 이식 관점에서 가치가 낮음.

### B. 알고리즘 요약

1. 논문 본론은 조합 설계론: super-simple `(v,5,2)` directed design(DGDD/DD)의 존재를 `v≡0,1 (mod 5), v≥15` 전 범위에 대해 재귀 구성(Weighting, Construction 1/2)과 직접 구성(소규모 v)으로 증명.
2. 풀려는 문제는 "최소 정의집합(smallest defining set)이 전체 블록의 절반 이상"인 super-simple 방향 설계의 존재성이며, LDPC는 마지막 5절에서 응용 예시로만 다룸.
3. 채널/노이즈 모델 없음(수학적 조합 구조 논문, 통신 채널 가정 없음).
4. LDPC 부호 구성: 설계의 블록 `b1,...,bn`을 열로, 순서쌍 `(xi,xj)` (xi<xj)를 행으로 하는 `(2v)×n` 지시 행렬 `A`를 만들고, 0행/0열 제거 후 parity-check 행렬 `C`(또는 그 전치) 획득.
5. 핵심 결과(Proposition 2,3 / Theorem 1): cyclical trade의 최소 volume과 Tanner 그래프 cycle 길이가 대응하며, super-simple 성질(임의 두 블록 교집합 ≤2점)이 4-cycle 없음을 보장 → girth≥6, defining set 조건까지 더하면 예제(v=15)에서 girth=8까지 달성 가능.
6. 부수 개념: elementary trapping set (α,β)-ETS와 normal graph를 이용해 girth를 간접 계산(예제 girth-8 확인용 툴).
7. 학습/최적화 절차 없음. 순수 조합적 재귀/직접 구성(TD, GDD weighting 등 디자인 이론 표준 도구) 사용.
8. 결과: v=15 예제에서 42×42 irregular LDPC(`dc={1,2,3,4}`, `dr={2,3,4}`) 구성, girth=8 확인. 그 외 BER/복호 성능/throughput 수치 전무.
9. 한계: 실제 통신/저장 채널 실험 없음(이론뿐), 코드 길이가 매우 작은 조합적 예제 위주, 복호 알고리즘·HW 설계 논의 전혀 없음, error-floor/waterfall 정량 평가 부재.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Super-simple directed design 기반 PCM 구성법 | `ecc_top.cpp` `Load_PCM()` | 새로운 대안적 H-matrix 구성법이지만 QC 구조·rate 무관한 순수 조합 설계로 실제 부호 스펙과 정합 불투명 |
| girth≥6/8 보증(4-cycle free) | 대응 없음 | Prime ECC의 QC-LDPC는 이미 구조적으로 girth 관리되며 이 논문의 이론적 증명 방식과 직접 연결 없음 |
| Trapping set / normal graph 개념 | 대응 없음 | error-floor 분석 툴로 쓰일 수 있으나 본 논문에서 실제 trapping-set 기반 성능 개선을 다루지 않음(정의만 소개) |

적용 가치: 낮음 — 조합 설계론 관점의 이론적 LDPC 구성 논문으로 정정능력·HW·복잡도 실험이 전무해 Prime ECC 이식 관점에서 참고할 실질적 요소가 거의 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2007.13743v2",
  "title": "Super-simple (v, 5, 2) directed designs and their smallest defining sets with its application in LDPC codes",
  "year": 2020,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": null,
  "code_length": "42~3406",
  "soft_quant": "무관",
  "key_contribution": "super-simple (v,5,2) directed design의 존재성을 재귀·직접 구성으로 증명하고, 이를 이용해 girth≥6(예제는 8)인 trade-based irregular LDPC 부호의 parity-check 행렬을 구성",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "조합 설계론(design theory) 순수 수학 논문으로 BER/error-floor/복호 성능 실험이 전무하며, 부호 예제도 매우 작은 length(42~3406) 위주라 실용 NAND ECC rate/length와 무관",
  "todo_check": "girth-8 보증 특성이 error-floor 개선에 실질적으로 기여하는지 정량 검증 필요(본문엔 이론적 girth 증명만 존재)"
}
```
