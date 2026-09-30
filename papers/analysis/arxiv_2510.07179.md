### arxiv:2510.07179v2 - Diffusion Codes: Self-Correction from Small(er)-Set Expansion with Tunable Non-locality (2026, arXiv/quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.18 |
| 부호length | 244~99536 |
| 연판정 | 무관 |
| 핵심기여 | random SWAP network 깊이로 locality<->expansion을 조절하는 "diffusion code" 구성법, sub-extensive "smaller-set" expander 증명 |
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
| 한계,주의 | 순수 구성법·조합론 이론(passive quantum memory·self-correction 지향), 부호 파라미터가 최적 대비 sub-optimal이고 NAND ECC 성능·HW와 무관 |
| 추가확인 | 없음 |

> 총평: SWAP network 기반 tunable-locality LDPC 구성법 + 양자 hypergraph product 이론으로, NAND용 고rate QC-LDPC 부호설계와 목표·구조가 달라 이식가치 낮음.

### B. 알고리즘 요약

1. 대상은 cycle graph 위의 (준)1D classical LDPC 및 그 hypergraph product로 얻는 (준)2D quantum CSS LDPC, 파라미터 `[n, O(n), O(n^β)]`, 예: `wbit=9, wcheck=11`(rate `1-9/11≈0.18`).
2. 문제: 좋은 expander LDPC는 geometric locality가 없어 근거리 HW에 배치 곤란, 반대로 국소 부호는 좋은 파라미터 불가 - locality<->expansion trade-off.
3. 모델: 완전 랜덤 permutation(configuration model=Gallager 부호)을 국소 SWAP(interchange) 과정으로 대체, 확산 시간 `T`로 국소성 조절.
4. 핵심 기법: N개 노드에 nearest-neighbor SWAP 회로 깊이 `NT` 적용 후 socket 단위로 collapse해 (wbit,wcheck)-biregular Tanner graph 생성 (Fig.1).
5. 핵심 식/성질: `T~N^α`이면 δ~`n^β`(β>α/2)까지 lossless "smaller-set" vertex expander, 각 check의 geometric 크기는 `~T^(1/2)`로 유계.
6. 확장: 두 classical diffusion code의 hypergraph product로 torus 위 quantum LDPC 획득, 동일 smaller-set (co)boundary expansion·self-correction 상속.
7. 증명 기법: Tanner graph 확장을 simple exclusion process(SEP)의 interparticle 거리 분포 문제로 환원, mesoscopic time(δ≪T≪t_mix)에서 stochastic monotonicity로 mixing 경계 확보.
8. 이론적 귀결: expansion이 거리 하한(Lemma 2.19), confinement(Lemma 2.21), Glauber 동역학 하 thermal stability(Thm 3.42), 선형시간 flip/single-shot 디코딩 가능성을 보장.
9. 결과(시뮬): `wbit=9,wcheck=11,T=N`에서 flip decoder threshold `0.017~0.019`, BP decoder threshold `0.11~0.13`; memory time이 시스템 크기의 stretched-exponential `exp(Ω(√N))`로 발산(self-correction).
10. 한계: 순수 이론/구성법(HW 미설계), 부호 파라미터가 pure code perspective에서 sub-optimal, 목표가 passive quantum memory·spin glass 물리로 NAND ECC와 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SWAP network 기반 Tanner graph/H-matrix 구성법 | 대응 없음 | Prime ECC는 고정 QC-LDPC(base+circulant, `PCM_b`)로 랜덤 SWAP 구성과 부호구조 상이 |
| hypergraph product quantum CSS 부호 | 대응 없음 (non-binary/양자 부호) | 양자 self-correcting memory 대상, binary NAND LDPC와 무관 |
| flip / BP decoder (시뮬 벤치마크) | 대응 없음 (교과서 수준, min-sum 아님) | expander 부호용 local flip decoder는 Prime ECC의 min-sum 디코더와 별개 |
| 부호구조 로드 | `ecc_top.cpp` `Load_PCM()` | 형식상 H-matrix 로드 대응은 있으나 diffusion 구성 자체가 이식 대상 아님 |

적용 가치: **낮음** — passive quantum memory·self-correction을 위한 tunable-locality LDPC 구성 이론으로, NAND용 고rate binary QC-LDPC의 부호설계·디코더·HW 어디에도 실질 이식 요소 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2510.07179v2",
  "title": "Diffusion Codes: Self-Correction from Small(er)-Set Expansion with Tunable Non-locality",
  "year": 2026,
  "venue": "arXiv/quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": 0.18,
  "code_length": "244~99536",
  "soft_quant": "무관",
  "key_contribution": "random SWAP network 깊이로 locality<->expansion을 조절하는 diffusion code 구성법, sub-extensive smaller-set expander 증명",
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
  "caveat": "순수 구성법·조합론 이론(passive quantum memory·self-correction 지향), 부호 파라미터가 최적 대비 sub-optimal이고 NAND ECC 성능·HW와 무관",
  "todo_check": "없음"
}
```
