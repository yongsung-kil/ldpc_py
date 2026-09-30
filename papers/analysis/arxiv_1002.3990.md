### arxiv:1002.3990v1 - Static Address Generation Easing: a Design Methodology for Parallel Interleaver Architectures (2010, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 미상 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 병렬 인터리버 아키텍처용 충돌회피(conflict-free) 메모리 매핑을 찾으면서 목표 steering 네트워크(barrel-shifter 등)를 최적화하는 재귀 매핑 방법론 SAGE |
| HW설계 | O |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 인터리버(permutation) 기반 turbo/LDPC 디코더 대상, 교육용 예제(12원소, 3PE)만 제시하고 실칩/합성 수치 없음 |
| 추가확인 | Prime ECC의 QC-LDPC는 circulant shift(고정) 구조라 임의 인터리버 매핑 문제가 그대로 발생하는지 확인 필요 |

> 총평: turbo-like 병렬 디코더의 메모리 충돌회피 매핑 방법론으로, 부호/복호 알고리즘 기여는 없고 교육용 예제뿐이라 Prime ECC의 고정 QC-LDPC HW에 이식 가치가 낮다.

### B. 알고리즘 요약

1. 대상: 고throughput turbo-like(turbo-code / LDPC) 병렬 디코더의 인터리버 아키텍처 — 여러 PE가 인터리빙 규칙에 따라 메모리 뱅크에 동시 접근.
2. 문제: 병렬 접근 시 서로 다른 PE가 같은 메모리 블록에 동시 read/write하는 "collision" 발생 → 표준 준수하면서 충돌 없이, 게다가 네트워크(steering component)까지 최적화하고 싶다.
3. 기존 3부류: (a) 전용 인터리버 규칙 설계(표준 비준수 위험), (b) 버퍼 추가(면적/latency↑, Benes 네트워크 비효율), (c) 충돌회피 메모리 매핑([13]은 SA로 항상 해 찾지만 종료 예측 불가 + 네트워크 최적화 안 함).
4. 문제 정형화: `L`개 원소를 두 partition(`Nat`, `Int=Π`)으로 나누고, 각 subset 크기 `X = L/N`(=병렬도=뱅크 수). 매핑 `M:{1..L}→{1..X}`.
5. 충돌회피 조건: 같은 subset(같은 시각 접근)에 속한 원소는 서로 다른 뱅크로 → `M(i) ≠ M(i')` (식 (1),(2)).
6. SAGE 표현: 자연순서 `MNat`, 인터리브순서 `MInt` 행렬 + 매핑행렬 `MAPNat/MAPInt`. 열=동시 처리 cycle, 행=PE.
7. 제약: (구조) 공통 데이터는 두 매핑에서 동일 뱅크, 각 열에서 뱅크는 1회만. (아키텍처 목표) barrel-shifter면 각 열이 다른 열의 circular permutation이 되도록.
8. 알고리즘(MemMap): 첫 열에 뱅크 초기 할당 → 가장 제약 많은 열 선택 → 각 빈칸에 가능한 뱅크 리스트(목표 아키텍처 우선 정렬) 구성 → 첫 원소 매핑 후 상대 행렬 반영·재귀, 리스트 비면 backtrack.
9. 결과: 12원소·3PE·barrel-shifter 예제에서 충돌회피 매핑 도출(Bank A={0,1,6,3} 등), 각 열이 순환치환 → barrel-shifter로 네트워크 구현 가능. 13 대비 네트워크 제어 가능함을 보임.
10. 한계: 교육용(pedagogical) 예제 1건, gate count/throughput/합성 수치 없음, 부호·복호 성능 기여 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 병렬 메모리 뱅크 충돌회피 매핑 | 대응 없음 (우리는 z=32 row-parallel, circulant shift 고정) | 임의 인터리버가 아닌 QC circulant 구조라 문제 형태가 다름 |
| steering network(barrel-shifter) 최적화 | 대응 없음 | Prime ECC HW 라우팅은 GT/HCU로 고정, 인터리버 네트워크 합성 대상 아님 |
| 인터리빙 permutation 처리 | 대응 없음 | QC-LDPC는 shift 기반, turbo-style 인터리버 아님 |

마지막 적용 가치: **낮음** — turbo-like 임의 인터리버의 메모리 충돌회피/네트워크 합성 방법론으로, circulant-shift 고정 구조의 Prime ECC QC-LDPC HW에는 문제 정의 자체가 대응되지 않는다.

### D. JSON 블록

```json
{
  "id": "arxiv:1002.3990v1",
  "title": "Static Address Generation Easing: a Design Methodology for Parallel Interleaver Architectures",
  "year": 2010,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "미상",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "병렬 인터리버 아키텍처용 충돌회피 메모리 매핑을 찾으면서 목표 steering 네트워크(barrel-shifter 등)를 최적화하는 재귀 매핑 방법론 SAGE",
  "hw_designed": "O",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "인터리버(permutation) 기반 turbo/LDPC 디코더 대상, 교육용 예제(12원소, 3PE)만 제시하고 실칩/합성 수치 없음",
  "todo_check": "Prime ECC의 QC-LDPC는 circulant shift(고정) 구조라 임의 인터리버 매핑 문제가 그대로 발생하는지 확인 필요"
}
```
