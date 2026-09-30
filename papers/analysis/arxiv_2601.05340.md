### arxiv:2601.05340v1 - The Number of Cycles of Bi-regular Tanner Graphs in Terms of the Eigenvalues of the Adjacency Matrix (2026, arXiv/IEEE Trans. IT submitted)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 155 |
| 연판정 | 무관 |
| 핵심기여 | 인접행렬 고유값만으로 bi-regular QC-LDPC의 2k-cycle 수를 계산하는 재귀·닫힌형 공식 유도 |
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
| 한계,주의 | 순수 조합/스펙트럼 이론, 부호 구성·복호·HW 없음. bi-regular 그래프에만 적용 |
| 추가확인 | 이 cycle 카운팅을 실제 QC-LDPC H-matrix 설계(short-cycle 최소화)에 자동화 접목 가능한지 |

> 총평: NAND ECC 이식 가치는 낮으나, QC-LDPC H-matrix 설계 시 short-cycle 진단 도구로만 부수 활용 여지.

### B. 알고리즘 요약

1. 대상은 `nc x nv` circulant 블록으로 구성된 binary QC-LDPC 부호(polynomial PCM `H(x) mod x^N-1`); 예시로 Tanner의 (3,5)-regular [155,91,20] 부호(`N=31`) 사용.
2. 문제: LDPC의 waterfall/error-floor 성능을 좌우하는 Tanner 그래프의 짧은 cycle 수 `N_2k`를 빠르게 세는 것.
3. 기존 Dehghan-Banihashemi 정리는 directed edge matrix `Ae`의 고유값 `{η_i}`를 방정식 `ξ^2+(-λ^2+q1+q2)ξ+q1q2=0`으로 구해야 함.
4. 핵심 기법: `Ae` 고유값 계산을 우회, 인접행렬 `A`(혹은 `HH^T`)의 고유값 `λ`만으로 `N_2k`를 직접 표현.
5. bi-regular 그래프에서 짝수 cycle만 존재(`N_2k = Σ η^2k /4k`)한다는 관찰과 Newton 항등식으로 재귀식 유도.
6. 주 결과(Theorem 3): `α = λ^2-(q1+q2)`에 대해 `S_{α,k}=α·S_{α,k-1}-q1q2·S_{α,k-2}` 재귀로 `N_2k` (`k<=g`)를 정수계수만으로 계산.
7. 확장(Cor.3): `HH^T`의 고유값 `λ`의 거듭제곱과 `N_2j (j<k)`로 `N_2k`를 `k<=7`까지 명시 공식화.
8. Cor.5: girth 조건 `g>=2k iff Σλ^j=|E|·A_2j`로 원하는 girth 달성의 필요충분조건 제시.
9. QC 구조상 `HH^T` 고유값은 `H(ρ)H(ρ)^T` (block-circulant, roots of unity `ρ`) 평가로 효율 계산; 예시서 `N_8=465, N_10=3720` 등 기존 결과와 일치 확인.
10. 한계: 순수 이론(HW·복호·시뮬 없음), bi-regular 그래프 한정, irregular/실제 NAND 부호로 직접 이식 불가.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC H-matrix cycle 진단(설계 보조) | ecc_top.cpp Load_PCM() | H-matrix 로드 대상이나 논문은 설계 지표 제공만, 코드 변경 불필요 |
| 복호 알고리즘/스케줄 | 대응 없음 | 논문은 복호 미다룸 |
| 인코더 | 대응 없음 | 논문은 인코더 미다룸 |
| soft-read/양자화 | 대응 없음 | 연판정 무관 |
```

적용 가치: **낮음** — 순수 cycle 카운팅 이론으로 복호/HW에 직접 이식할 요소가 없고, 우리 QC-LDPC는 이미 고정된 H-matrix라 재설계 지표로서의 활용도 제한적.

### D. JSON 블록

```json
{
  "id": "arxiv:2601.05340v1",
  "title": "The Number of Cycles of Bi-regular Tanner Graphs in Terms of the Eigenvalues of the Adjacency Matrix",
  "year": 2026,
  "venue": "arXiv (IEEE Trans. Information Theory, submitted)",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "155",
  "soft_quant": "무관",
  "key_contribution": "인접행렬 고유값만으로 bi-regular QC-LDPC의 2k-cycle 수를 계산하는 재귀·닫힌형 공식 유도",
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
  "caveat": "순수 조합/스펙트럼 이론, 부호 구성·복호·HW 없음. bi-regular 그래프에만 적용",
  "todo_check": "이 cycle 카운팅을 실제 QC-LDPC H-matrix 설계(short-cycle 최소화)에 자동화 접목 가능한지"
}
```
