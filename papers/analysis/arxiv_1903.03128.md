### arxiv:1903.03128v3 - Decoder-in-the-Loop: Genetic Optimization-based LDPC Code Design (2019, ISIT/arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 128 |
| 연판정 | 무관 |
| 핵심기여 | GenAlg(유전 알고리즘)로 디코더/채널을 루프에 넣고 short-length H-matrix 전체를 직접 최적화 |
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
| 한계,주의 | short-length(n=128) 무선/URLLC 타깃, HW 미설계·시뮬만, 고rate NAND QC-LDPC와 정합 안 됨 |
| 추가확인 | GenAlg를 고rate·긴 QC-LDPC + min-sum(양자화) 디코더-in-loop으로 확장 시 error-floor 영향 |

> 총평: 유전 알고리즘 기반 short LDPC 부호설계로 아이디어는 흥미로우나 n=128 저rate·무선 타깃이라 NAND 고rate QC-LDPC 이식성은 하.

### B. 알고리즘 요약

1. 시스템: bi-AWGN 및 Rayleigh fading 채널, 대상 부호는 `(n=128, k=64)`, `Rc=0.5` short-length LDPC.
2. 문제: density evolution/EXIT chart 등 점근길이 기반 설계는 ultra-short 영역에서 성능 열화, PEG도 점근 degree profile에 의존.
3. 핵심 기법: 부호설계를 BLER 최소화 최적화 문제로 보고 Genetic Algorithm(`GenAlg`)로 H-matrix 전체(edge interleaver)를 직접 진화.
4. "Decoder-in-the-loop": 실제 BP 디코더·채널·`Nit,max`를 fitness 평가에 넣어 설계 SNR(예: 5 dB)에서 BLER로 후보 부호를 평가.
5. 진화 연산: mutation(edge 추가/삭제), crossover(두 부모 H1,H2의 2D 대칭 교차), 세대마다 상위 `T=20` 부호 선택.
6. 확장: IRA/TB-IRA/PTB-IRA 등 accumulator 기반 구조(`H=[HL HR]`, HR=dual-diagonal)를 강제해 인코딩 용이 부호도 설계 가능.
7. 결과: 5G/CCSDS/ARJA 등 표준 short LDPC와 대등하거나 능가, `Nit,max=20`으로 설계 시 AWGN 0.325 dB, Rayleigh 0.8 dB(BLER 10^-5~10^-4) 이득.
8. iteration/복잡도: 동일 `Nit,max`에서 평균 iteration `Nit,avg`와 복잡도 `η=Nit,avg·E/k`가 표준 부호보다 낮음(디코딩 latency 감소).
9. 인사이트: 최적 부호에 degree-1 VN이 등장하나 CN당 1개만 연결되도록 GenAlg가 스스로 "학습", short girth의 degree-2 VN도 회피.
10. 한계: HW 미설계·시뮬 전용, short-length·무선(URLLC) 타깃, 긴 부호로 scale 시 degree-1 VN에 의한 error-floor 발생(sanity check).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| H-matrix / 부호구조 최적화(GenAlg) | ecc_top.cpp `Load_PCM()` | 부호설계 레이어 대응이나 Prime ECC는 특정 QC-LDPC 고정, 재설계 부담 큼 |
| BP(SP tanh) 디코더 in-loop | decoder.cpp `LDPC_Decoder()` | 우리는 min-sum 근사, full-tanh SP는 대응 부분적 |
| accumulator/dual-diagonal 인코딩 구조 | encoder.cpp `LDPC_encoder_4KB()` | dual-diagonal 개념은 유사하나 우리 인코딩 고정 |
| degree-1/degree-2 VN 구조 규칙 | 대응 없음 | 부호구조 인사이트일 뿐 코드 모듈 직접 대응 없음 |

적용 가치: **낮음** — GenAlg 개념은 참고할 만하나 short-length·저rate·무선 타깃 + HW 미설계로, 고rate·특정 QC-LDPC 고정된 Prime ECC에 그대로 떼어 쓰기 어렵다.

### D. JSON 블록

```json
{
  "id": "arxiv:1903.03128v3",
  "title": "Decoder-in-the-Loop: Genetic Optimization-based LDPC Code Design",
  "year": 2019,
  "venue": "arXiv cs.IT (ISIT)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "128",
  "soft_quant": "무관",
  "key_contribution": "GenAlg로 디코더/채널을 루프에 넣고 short-length H-matrix 전체를 직접 최적화",
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
  "caveat": "short-length(n=128) 무선/URLLC 타깃, HW 미설계·시뮬만, 고rate NAND QC-LDPC와 정합 안 됨",
  "todo_check": "GenAlg를 고rate·긴 QC-LDPC + min-sum(양자화) 디코더-in-loop으로 확장 시 error-floor 영향"
}
```
