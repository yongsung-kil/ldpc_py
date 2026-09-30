### arxiv:2605.08644v1 - On Codes with Support-Constrained Parity Checks (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.667 |
| 부호length | 36 |
| 연판정 | 무관 |
| 핵심기여 | 패리티체크 support 제약 하 최대 minimum distance를 expansion(τ,ρ)로 특성화, K6,6 마스크로 GRS 서브코드 불가능 반례 제시 |
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
| 한계,주의 | 순수 이론(비구성적 존재성), 큰 유한체 Fq 필요, binary QC-LDPC와 무관 |
| 추가확인 | 없음 (NAND binary LDPC 이식 가치 없음) |

> 총평: sparse 패리티체크 부호의 minimum-distance 한계에 대한 순수 대수적 이론 논문으로, 큰 유한체 GRS/Vandermonde 기반이라 NAND binary QC-LDPC에 이식 여지 없음.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 패리티체크 행렬 `H`에 임의의 support(0/1 마스크 `M`) 제약을 준 선형부호로, 각 체크식이 정해진 심볼 집합만 포함하도록 강제한다.
2. 문제: 이 support 제약 하에서 달성 가능한 최대 minimum distance는 무엇이며, 작은 체에서 구조적 부호로 실현 가능한가.
3. 모델: 유한체 `Fq`, 열 support `Sj={i:Mij=1}`, 이분그래프 `G_M`의 매칭으로 구조적 rank 정의.
4. 핵심량: structural row rank `ρ(M)=ν(G_M)`(최대 매칭), structural Kruskal rank `τ(M)`(모든 `|R|≤s`에 `|S(R)|≥|R|` 유지 최대 s).
5. 핵심정리(Theorem 1): 임의 filling에서 `dmin(kerH) ≤ τ(M)+1`이며, `q > Δ(M)=(ρ+τ)·C(n,τ)`인 소수거듭제곱 체에서 등호 달성.
6. 증명은 Schwartz-Zippel(각 τ-부분집합 minor가 비영)로 존재성만 보장 - 비구성적이고 지수적 체 크기 요구.
7. MDS 영역: expansion 조건(5)이 m까지 성립하면 dual GM-MDS로 GRS 부호가 `M`을 만족(`q≥n+m-1`).
8. Vandermonde certificate: sparse 부호를 GRS 서브코드로 실현 가능한지 `AH=V`(Vandermonde) 인수분해로 판정.
9. 반례: `K6,6` 정점-간선 근접행렬 마스크(`m=12,n=36,τ=5,ρ=12`)는 `[36,24,6]` 부호를 허용하나 어떤 체에서도 GRS 서브코드로 실현 불가(부록 A: PGL2 involution 논증).
10. 한계: 순수 이론으로 디코더·복잡도·HW 전무, non-binary 큰 체 GRS/RS 대상이라 실용 LDPC 구성법 아님.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| support-제약 패리티체크 부호설계 | 대응 없음 | 큰 체 GRS/RS 대상, binary QC-LDPC 부호구조와 무관 |
| minimum distance 이론 한계 | 대응 없음 | 디코더/성능 시뮬 요소 없음 |
| GM-MDS/Vandermonde 인수분해 | 대응 없음 | Prime ECC는 고정 binary H-matrix 사용 |

적용 가치: **낮음** - 순수 대수 이론이며 non-binary 큰 체 GRS 기반이라 NAND binary QC-LDPC 코드베이스에 이식할 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.08644v1",
  "title": "On Codes with Support-Constrained Parity Checks",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": 0.667,
  "code_length": "36",
  "soft_quant": "무관",
  "key_contribution": "패리티체크 support 제약 하 최대 minimum distance를 expansion(τ,ρ)로 특성화하고 K6,6 마스크로 GRS 서브코드 불가능 반례 제시",
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
  "caveat": "순수 이론(비구성적 존재성), 큰 유한체 Fq 필요, binary QC-LDPC와 무관",
  "todo_check": "없음 (NAND binary LDPC 이식 가치 없음)"
}
```
