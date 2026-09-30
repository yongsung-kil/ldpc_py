### arxiv:2509.13040v2 - Linear Complexity Computation of Code Distance and Minimum Size of Trapping Sets for LDPC Codes with Bounded Treewidth (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | other |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | bounded treewidth LDPC에서 최소거리·최소 (a,b)-trapping set 크기·개수를 부호길이에 선형복잡도로 계산하는 tree decomposition 기반 DP |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | bounded treewidth 가정에 의존; 실무 QC-LDPC는 treewidth가 커 선형복잡도 이점 소실 위험, 복호기·부호설계 개선책은 없음 |
| 추가확인 | Prime ECC의 실제 QC-LDPC PCM(z=32, N_b=129) treewidth/pathwidth가 얼마인지 - bounded 여부가 적용성 좌우 |

> 총평: error-floor의 주범 trapping set/최소거리를 선형복잡도로 계산하는 순수 이론 분석 도구로, 복호기·HW·부호구성 이식 요소는 없다.

### B. 알고리즘 요약

1. 문제: Tanner graph `G`와 `b≥0`이 주어질 때 최소 `a`의 `(a,b)`-trapping set을 찾기 (`a`=variable node 수, `b`=odd-degree check node 수); `b=0`이면 최소거리 계산과 등가.
2. 배경: MINIMUM TRAPPING SET은 일반 binary linear code에서 NP-hard(근사조차 NP-hard). error-floor의 주 원인이라 실용 코드(길이 1000~10000)에서 탐색이 중요.
3. 핵심 가정: LDPC 부호의 Tanner graph가 **bounded treewidth `k`**를 가지면(그리고 tree decomposition을 알면) 선형복잡도로 풀 수 있음.
4. 핵심 기법: rooted nice tree decomposition의 bag `B_t`를 bottom-up 순회하는 DP. leaf/introduce/forget/join 노드별로 함수 `f_t(L,I)`(최소 크기), `g_t(L,I)`(개수)를 갱신.
5. 핵심 식: `Γ°_G(S)=Γ°_G(S1)⊕Γ°_G(S2)` (Property 1) - odd-degree check 집합이 부분집합 대칭차로 분해됨을 이용해 부분해를 합성.
6. 확장(`b>0`): 상태에 `(L,R,d)` 추가(`d`=bag 밖 odd-degree check 수)해 일반 `(a,b)` trapping set으로 확장 (Theorem 4).
7. 구현 디테일: introduce check 노드에서 `E(c,L)` 홀짝으로 유효성 판정; join 노드에서 두 자식 상태를 `⊕`로 병합.
8. 최적화 절차: Theorem 1/4 알고리즘을 반복 호출하는 FMTS/GFMTS(Alg.1/2)로 실제 최소 trapping set 원소집합까지 복원.
9. 결과: 복잡도 `O(n·4^k)`(b=0), `O(n(b+1)²·4^k)`(b>0); pathwidth면 `O(n·2^k)`. SC-LDPC(4×5 subcode, coupling length 10, width 3) 검증: 최소 (10,0) trapping set 1개, exhaustive 대비 50.13h→0.57h(≈88배).
10. 한계: HW 미설계, 복호기·부호구성 개선 없음; bounded treewidth가 전제라 treewidth 큰 실무 QC-LDPC에는 지수항 `4^k` 폭발.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 최소거리 / trapping set 크기 계산 | 대응 없음 | 오프라인 부호분석 도구, 복호기·인코더 실행경로 밖 |
| trapping set 기반 error-floor 추정 | decoder.cpp `LDPC_Decoder()` (간접) | error-floor는 복호 성능이나, 본 논문은 복호기를 바꾸지 않고 부호구조만 분석 |
| SC-LDPC / tree decomposition | ecc_top.cpp `Load_PCM()` (간접) | 부호구조 입력을 공유할 수 있으나 Prime ECC는 QC-LDPC 고정, SC-LDPC 대상 아님 |

적용 가치: **낮음** — error-floor 분석에 개념적으로 닿지만, Prime ECC의 고rate QC-LDPC는 treewidth가 커 선형복잡도 이점이 사라질 가능성이 크고, 복호기/HW/부호설계에 떼어 쓸 알고리즘 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2509.13040v2",
  "title": "Linear Complexity Computation of Code Distance and Minimum Size of Trapping Sets for LDPC Codes with Bounded Treewidth",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "other",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "bounded treewidth LDPC에서 최소거리·최소 (a,b)-trapping set 크기·개수를 부호길이에 선형복잡도로 계산하는 tree decomposition 기반 DP",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "bounded treewidth 가정에 의존; 실무 QC-LDPC는 treewidth가 커 선형복잡도 이점 소실 위험, 복호기·부호설계 개선책은 없음",
  "todo_check": "Prime ECC의 실제 QC-LDPC PCM(z=32, N_b=129) treewidth/pathwidth가 얼마인지 - bounded 여부가 적용성 좌우"
}
```
