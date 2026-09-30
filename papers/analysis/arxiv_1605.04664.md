### arxiv:1605.04664v1 - A Joint Optimization Technique for Multi-Edge Type LDPC Codes (2016, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.1~0.5 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | MET-LDPC 구조·차수분포 joint 최적화(AR+Dif.E)로 DE 임계값을 Shannon 근접까지 향상 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC/BI-AWGN 점근 임계값 최적화 이론뿐, 유한길이 부호·HW·NAND 무관; MET+puncturing은 고rate NAND ECC와 이질적 |
| 추가확인 | AR+Dif.E joint 최적화가 고rate binary QC-LDPC 부호설계 오프라인 툴로 재활용 가능한지 |

> 총평: MET-LDPC 구조와 차수분포를 동시에 최적화해 임계값을 높이는 부호설계 이론 논문으로, 저rate·MET·puncturing 지향이라 고rate NAND binary QC-LDPC 이식가치는 낮다.

### B. 알고리즘 요약

1. 대상은 multi-edge type(MET) LDPC 부호 앙상블 설계로 rate-1/2, rate-1/10 예제를 BEC/BI-AWGN에서 다룸.
2. 풀려는 문제: MET는 좋은 Tanner 구조가 사전에 불명확 - 구조 `(Λ,Γ)`와 차수분포 `(L,R)`를 동시 최적화해야 함.
3. 부호는 노드관점 다항식 `L(r,x)=ΣL_{b,d}r^b x^d`, `R(x)=ΣR_d x^d`, rate `R=L(1,1)−R(1)`로 기술.
4. 핵심 관찰: socket-count 등식 `L_{xi}(1,1)=R_{xi}(1)`과 rate 제약으로 `(Γ,R)`가 `(Λ,L)`에 종속 - 탐색을 `(Λ,L)`로 축소.
5. 이 종속식으로 concentrated check node degree를 결정론 함수 `Γ=f(Λ,L)`, `R=f(Λ,L)`로 계산(2~3 check class).
6. 최적화기: 차수분포 `L`은 Adaptive Range(AR) 지역탐색, 구조 `Λ`는 Differential Evolution - combined optimization (AR+Dif.E).
7. AR은 현재 최적점 주변 `SR` 내 랜덤탐색 후 개선 없으면 `SR=RM×max|Q_Best−Q_NextBest|`로 축소.
8. 비용함수(임계값 `P∗`)는 `L` 최적화 시 국소최대가 밀집, `Λ` 최적화 시 멀리 떨어져 → 두 단계에 다른 기법 사용 정당화.
9. 결과: rate-1/2 code 4가 max VN degree 6으로 BI-AWGN 임계값 0.927(Shannon 0.0516 이내); rate-1/10 puncturing으로 max degree 23→7 절감.
10. 한계: 점근 임계값(무한 길이) 이론뿐, 유한길이 부호·복호 iteration·HW·NAND soft-read 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MET 구조·차수분포 joint 최적화 | 대응 없음 | Prime ECC는 고정 binary QC-LDPC, MET/puncturing 설계 오프라인 툴 대응 모듈 없음 |
| DE 임계값 비용함수 | 대응 없음 | bit-exact 복호 시뮬레이터에 DE 점근 임계값 계산 없음 |
| H-matrix/부호구조 로드 | ecc_top.cpp `Load_PCM()` | 산출 차수분포를 QC-LDPC로 변환·재검증해야 이식, MET는 QC 구조와 이질적이라 부담 큼 |

적용 가치: **낮음** — 저rate MET-LDPC 점근 임계값 최적화 이론이라 고rate 고정 binary QC-LDPC 코드베이스에 직접 이식할 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1605.04664v1",
  "title": "A Joint Optimization Technique for Multi-Edge Type LDPC Codes",
  "year": 2016,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": "0.1~0.5",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "MET-LDPC 구조·차수분포 joint 최적화(AR+Dif.E)로 DE 임계값을 Shannon 근접까지 향상",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC/BI-AWGN 점근 임계값 최적화 이론뿐, 유한길이 부호·HW·NAND 무관; MET+puncturing은 고rate NAND ECC와 이질적",
  "todo_check": "AR+Dif.E joint 최적화가 고rate binary QC-LDPC 부호설계 오프라인 툴로 재활용 가능한지"
}
```
