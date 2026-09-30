### arxiv:2410.11111v2 - A Combinatorial Approach to Avoiding Weak Keys in the BIKE Cryptosystem (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 1114~24646 |
| 연판정 | hard-1bit |
| 핵심기여 | QC-MDPC(BIKE) 개인키의 Tanner graph 4-cycle을 정의 다항식에서 직접 셈하는 폐형 공식 + weak key 필터링 알고리즘 |
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
| 한계,주의 | QC-MDPC 암호(BIKE)·bit-flipping BGF 전용, rate 0.5 저rate·MDPC(LDPC보다 dense), NAND ECC 무관 |
| 추가확인 | 4-cycle 폐형 셈 공식이 우리 고rate QC-LDPC girth 진단·H-matrix 스크리닝에 재사용될 여지 |

### B. 알고리즘 요약

1. 대상: BIKE 후양자 암호의 개인키 = `H=[H_0 H_1]` (2블록 circulant, `r` prime, rate 0.5 QC-MDPC), 반복 bit-flipping(BGF) 디코더.
2. 문제: MDPC 반복디코더의 DFR(디코딩 실패율) 계산이 어렵고, 실패가 key-recovery 공격으로 이어짐 -> 실패 유발 weak key를 걸러내야 함.
3. 핵심 가정: 반복디코더 실패는 Tanner graph의 짧은 cycle(특히 4-cycle)이 주범이며, weak key와 4-cycle 수가 강상관.
4. 핵심 기법 1단: circulant의 column intersection `CI(i,j)=µ(d(i,j),h)`로 환원(Prop.3.3), 단일 circulant 내 4-cycle 수를 거리 multiplicity로 `r·Σ C(µ(δ,h),2)`(Lemma 3.4)로 폐형화.
5. 핵심 식 의미: 두 블록 간 4-cycle은 `c_i=|Supp(h_0)∩Supp(h_1^i)|`로 `r·Σ C(c_i,2)`(Lemma 3.7), 전체는 Thm 3.9로 합산 -> 다항식만으로 4-cycle 총수 계산.
6. 핵심 기법 2단: 일반 QC-MDPC(`n0>2`)로 확장, 4-cycle을 Type A~D로 분류(Type D는 폐형 open).
7. 구현 디테일: 거리스펙트럼 `S_0,S_1,Q`와 가중벡터 `w_i=C(i,2)`로 column-intersection 프로파일 기반 필터(Algorithm 1), 기존 Type II/III 필터보다 미미한 추가연산.
8. 학습/최적화: 없음(조합론·통계), 4-cycle-free 조건 `r>2d^2` 분석(BIKE 파라미터로는 회피 불가) 및 random 키의 4-cycle-free 확률표(Table 2).
9. 결과: [3]의 공개데이터로 r=557/587 실패키 vs 랜덤키 4-cycle 수 비교 -> 실패키가 특히 **단일 circulant 내부** 4-cycle 유의하게 많음(p<0.05), block 내 cycle 우선 최소화 권고.
10. 한계: 순수 이론·통계 분석, HW/throughput/양자화 무관, 암호(rate 0.5 MDPC·bit-flipping) 특화라 NAND soft-decision min-sum LDPC와 직접 접점 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 다항식 기반 4-cycle 폐형 셈 / girth 진단 | ecc_top.cpp `Load_PCM()` | H-matrix 스크리닝 지표로 참고 가능하나 우리 H는 고정, 설계도구 성격 |
| bit-flipping(BGF) 디코더 | 대응 없음 | 우리는 soft min-sum, hard bit-flipping 미사용 |
| weak key 필터(암호 키공간) | 대응 없음 | NAND ECC엔 암호 키 개념 자체가 없음 |

적용 가치: **낮음** — 암호(BIKE/QC-MDPC)·bit-flipping 전용 조합론이라 NAND soft min-sum QC-LDPC 파이프라인과 직접 접점이 없고, 4-cycle 폐형 셈은 표준 girth 진단 수준 재사용에 그친다.

### D. JSON 블록

```json
{
  "id": "arxiv:2410.11111v2",
  "title": "A Combinatorial Approach to Avoiding Weak Keys in the BIKE Cryptosystem",
  "year": 2025,
  "venue": "arXiv (cs.IT) preprint",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "1114~24646",
  "soft_quant": "hard-1bit",
  "key_contribution": "QC-MDPC(BIKE) 개인키의 Tanner graph 4-cycle을 정의 다항식에서 직접 셈하는 폐형 공식 + weak key 필터링 알고리즘",
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
  "caveat": "QC-MDPC 암호(BIKE)·bit-flipping BGF 전용, rate 0.5 저rate·MDPC(LDPC보다 dense), NAND ECC 무관",
  "todo_check": "4-cycle 폐형 셈 공식이 우리 고rate QC-LDPC girth 진단·H-matrix 스크리닝에 재사용될 여지"
}
```
