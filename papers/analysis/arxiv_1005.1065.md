### arxiv:1005.1065v1 - New Families of LDPC Block Codes Formed by Terminating Irregular Protograph-Based LDPC Convolutional Codes (2010, arXiv/ISIT-class preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.25~0.857 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | AR4JA 프로토그래프 기반 LDPC convolutional을 종단(termination factor L)하여 rate 가변·capacity 근접 threshold·선형 최소거리 성장 부호족 구성 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC 대상 density evolution/weight enumerator 점근분석뿐(HW·유한길이 시뮬 없음), spatially-coupled 계열이라 짧은 QC-LDPC NAND ECC와 구조·복호창 상이 |
| 추가확인 | AWGN에서 유사거동 확인은 [15] 별도 논문에 있음 — 종단 아이디어를 고rate 짧은 부호에 적용 시 threshold saturation 이득 여부 |

> 총평: spatially-coupled(종단 LDPC convolutional) 부호족의 점근 threshold/거리 성장 설계 이론 논문. NAND binary QC-LDPC ECC 이식성 낮음.

### B. 알고리즘 요약

1. 대상: 프로토그래프 기반 LDPC convolutional code를 유한 시점 L에서 종단(termination)해 얻는 LDPC block code 앙상블족, 예시로 AR4JA 프로토그래프 사용.
2. 문제: irregular 부호는 BP threshold는 좋지만 최소거리 성장, regular는 그 반대 — 둘을 동시에(capacity 근접 threshold + 선형 최소거리) 만족하는 유연한 rate 부호족이 필요.
3. 모델: BEC(소실확률 `ε`), BP 복호. 프로토그래프 구조 보존 덕에 density evolution을 프로토그래프 내에서 수행.
4. 핵심 기법: base matrix `B`를 component submatrix `B0,...,B_ms`로 edge-spreading하여 무한 convolutional protograph `B[-∞,∞]` 구성 (`ms`=syndrome former memory).
5. 종단: 시점 0~L-1로 잘라 유한 base matrix `B[0,L-1]` 형성. 설계 rate `RL = 1 - ((L+ms)/L)(1-R)` — L↑이면 rate가 unterminated `R`로 접근.
6. AR4JA 확장: degree-4 변수노드 `2e`개 추가로 rate `R=(1+e)/(2+e)` 조절, `1/4 ≤ R ≤ 6/7` 범위 부호족 확보. degree-1,2 체크노드 회피하도록 c0 edge 미분할.
7. 분석: 점근 weight enumerator로 모든 앙상블이 asymptotically good(최소거리 `~n·δmin` 선형성장) 임을 증명.
8. threshold saturation: L↑이면 BP threshold가 Shannon limit로 수렴(예 e=0, R∞=1/2에서 `ε*=0.4996` vs `εsh=0.5`), 더 이상 감쇠 안 함.
9. 결과: L=9→gap 10%, L=20→5%, L=50→2%, L=100→1%. threshold와 거리성장 사이 trade-off를 e,L로 튜닝 가능.
10. 한계: BEC 점근분석(DE+enumerator)만, HW·유한길이 성능·복잡도 정량평가 없음. AWGN 결과는 후속 논문[15] 참조.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 프로토그래프/AR4JA 부호구조 설계 | ecc_top.cpp `Load_PCM()` | Prime ECC는 특정 QC-LDPC 고정 — protograph convolutional 종단부호와 부호구조 상이, 재검증 부담 큼 |
| BP density evolution threshold | 대응 없음 | Prime ECC는 min-sum 반복복호기만, DE 부호설계 툴 없음 |
| spatially-coupled 복호창 | 대응 없음 | Prime ECC 디코더는 block 단위, sliding-window 복호 미지원 |

적용 가치: **낮음** — spatially-coupled/종단 LDPC convolutional의 점근 부호설계 이론으로, 고rate 짧은 binary QC-LDPC NAND ECC와 부호구조·복호 아키텍처가 달라 직접 이식 대상이 아니다.

### D. JSON 블록

```json
{
  "id": "arxiv:1005.1065v1",
  "title": "New Families of LDPC Block Codes Formed by Terminating Irregular Protograph-Based LDPC Convolutional Codes",
  "year": 2010,
  "venue": "arXiv (cs.IT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": "0.25~0.857",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "AR4JA 프로토그래프 LDPC convolutional을 종단(L)하여 rate 가변·capacity 근접 threshold·선형 최소거리 성장 부호족 구성",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC 대상 DE/weight enumerator 점근분석뿐(HW·유한길이 시뮬 없음), spatially-coupled 계열이라 짧은 QC-LDPC NAND ECC와 구조·복호창 상이",
  "todo_check": "AWGN 유사거동은 [15] 별도 논문 — 종단 아이디어를 고rate 짧은 부호에 적용 시 threshold saturation 이득 여부"
}
```
