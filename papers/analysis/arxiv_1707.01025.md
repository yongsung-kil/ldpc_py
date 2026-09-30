### arxiv:1707.01025v1 - Distance Properties of Short LDPC Codes and their Impact on the BP, ML and Near-ML Decoding Performance (2017, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 48 |
| 연판정 | 무관 |
| 핵심기여 | 중복행(RPC) 추가로 stopping/trapping set 제거하여 BP FER를 ML에 근접시키는 near-ML 복호와 거리특성 분석 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | N=48 초단·저rate(0.5) 코드, RPC가 ML수렴엔 지수복잡도, 중복행 추가로 CN 부담 급증(HW 라우팅 악화) |
| 추가확인 | 고rate·긴 QC-LDPC에서 dstop→dmin 필요 중복행수와 실HW 라우팅/latency 비용 |

> 총평: 초단 LDPC 거리특성·RPC near-ML 이론 분석으로, NAND 고rate QC-LDPC HW 복호기엔 이식성 하.

### B. 알고리즘 요약

1. 대상: **길이 n=48, rate R=1/2** 짧은 코드(random RU, QC-LDPC, nonbinary 이진상, 최적선형)를 BEC/AWGN에서 BP/ML/near-ML 복호.
2. 문제: LDPC의 BP와 ML FER 격차가 커, 어떤 코드 파라미터가 FER에 영향을 주는지와 near-ML 복호법을 규명.
3. 모델: BEC FER는 최소 stopping set 크기 `dstop`이, ML은 최소거리 `dmin`이 지배; Tanner graph girth `g` 관련.
4. 핵심기법: 패리티검사행렬에 **중복행(dual codeword)을 저중량 순으로 추가**(RPC decoding)해 stopping/trapping set을 파괴, BP를 ML로 수렴.
5. 정의: `ℓ-th stopping redundancy ρ_ℓ` = 크기 ℓ 이하 ML-decodable stopping set을 모두 제거하는 최소 행수 → RPC 필요량 척도.
6. 확장: nonbinary(GF(2^m)) LDPC의 이진상 코드도 다룸(AWGN엔 q-ary 패리티 추가 필요, 향후 과제).
7. 이론: 평균 weight/stopping-set 스펙트럼 계수를 `n`에 선형 복잡도로 재귀 계산 → union-type 상한(식3)·tangential-sphere 상한 개선.
8. 스펙트럼 생성함수 `g(s)`, `φ(s)`로 이진상 평균 weight enumerator(식7) 유도.
9. 결과: 큰 girth QC-LDPC가 RPC로 ML에 가장 빠르게 수렴; RPC-16~256 추가 시 FER 급개선(N=48 코드), AWGN도 BEC와 유사 거동.
10. 한계: 시뮬·이론 전용(HW 미설계), N=48 초단 코드 예시뿐, RPC는 임계 이후 복잡도만 증가하고 완전 ML수렴은 지수복잡도.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| RPC(중복행 추가) 복호 | `decoder.cpp` `LDPC_Decoder()` | BP 루프는 대응되나 중복행 확장은 PCM/CN 구조 변경 필요, 고rate에선 행수 폭증 |
| 부호 PCM / QC 구조 로드 | `ecc_top.cpp` `Load_PCM()` | 중복행 추가로 H-matrix 재구성해야 함, 고정 QC-LDPC와 충돌 |
| stopping/trapping set 개선(error-floor) | 대응 없음 | Prime ECC엔 stopping-redundancy 기반 후처리 대응 모듈 없음 |
| 거리·스펙트럼 이론 분석 | 대응 없음 | 설계·검증 이론 도구, 시뮬레이터에 직접 대응 없음 |

적용 가치: **낮음** — 초단·저rate 코드의 거리이론·RPC near-ML 분석으로, NAND 고rate QC-LDPC HW 복호기에는 중복행 폭증·지수복잡도 때문에 이식 실익이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1707.01025v1",
  "title": "Distance Properties of Short LDPC Codes and their Impact on the BP, ML and Near-ML Decoding Performance",
  "year": 2017,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "48",
  "soft_quant": "무관",
  "key_contribution": "중복행(RPC) 추가로 stopping/trapping set 제거하여 BP FER를 ML에 근접시키는 near-ML 복호와 거리특성 분석",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "악화",
  "recommend": "하",
  "caveat": "N=48 초단·저rate(0.5) 코드, RPC가 ML수렴엔 지수복잡도, 중복행 추가로 CN 부담 급증(HW 라우팅 악화)",
  "todo_check": "고rate·긴 QC-LDPC에서 dstop->dmin 필요 중복행수와 실HW 라우팅/latency 비용"
}
```
