### arxiv:1206.3362v1 - An Improved WBF Algorithm for Higher-Speed Decoding of LDPC Codes (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.69~0.76 |
| 부호length | 255~1023 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 파이프라인 비교기 네트워크로 다중비트 flip 후보 선택을 부분병렬화해 MLP-WBF 대비 결정 지연을 줄인 FWBF 알고리즘 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 대상 부호가 EG-LDPC(finite geometry)이며 min-sum이 아닌 weighted bit-flipping 계열이라 Prime ECC 3.1의 min-sum 아키텍처와 알고리즘 계열 자체가 다름 |
| 추가확인 | 본문에 정확한 gatecount/throughput 수치가 없어 실제 HW 이득 크기 확인 불가 |

> 총평: BF 계열 저복잡도 디코더의 결정 지연을 파이프라인 비교기로 줄인 구조적 아이디어이나, min-sum 기반 Prime ECC 3.1과 알고리즘 계열이 달라 직접 이식 가치는 낮음.

### B. 알고리즘 요약

1. EG(255,175), EG(1023,781) LDPC 코드에 BPSK/AWGN 채널을 가정, 기존 BP 기반 디코더는 고속(예: 40Gb/s급 광통신) 요구에 하드웨어 복잡도가 과도함.
2. 기존 MLP-WBF는 flip할 λ개 비트를 순차적으로(bit-by-bit) 선택해야 해 반복당 결정 지연이 큼.
3. 핵심 기법: 메트릭 벡터를 `N/p`개의 p-length 블록으로 나누고, 각 블록에서 최대 metric 비트 1개만 flip 후보로 뽑는 부분병렬 선택(FWBF).
4. 비트 n의 metric `En = Σ_{m∈M(n)} (2sm-1)wn,m - α·yn` (IMWBF와 동일 metric 식 재사용, wn,m = min_{i∈N(m)\n} yi).
5. 비교기 네트워크(Fig.1, `log2(2q)` 단 파이프라인)를 이용해 블록별 최대값을 클록마다 파이프라인으로 흘려보내 지연을 `log2(2q) + N/(2q)`로 단축(식 3), MLP-WBF는 `λ×(log2(2q)+N/(2q)+log2(N/2q))`(식 2).
6. p(블록 길이) 선택이 평균 반복횟수와 트레이드오프 - p가 클수록(블록 적을수록) 반복수는 늘지만 하드웨어는 단순.
7. 부수 트릭: "null" metric 값을 도입해 N을 2q(=16)의 배수로 맞춰 병렬 계산 단위를 정렬.
8. 별도 학습/최적화 절차 없음 (고정 규칙 기반 알고리즘).
9. 결과: EG(255,175)에서 decoding delay가 MLP-WBF의 λ=10일 때 24λ=240 대비 FWBF는 20으로 대폭 감소(같은 평균 iteration 수 유지), BER 성능은 MLP-WBF와 유사.
10. 한계: HW(RTL/합성) 미설계, 시뮬레이션 및 지연 클록 수 이론 분석뿐이며 오래된 EG-LDPC 코드에 한정, BF 계열 성능은 BP 대비 waterfall에서 열세(code1에서 BER 1e-4 기준 0.5dB 열화).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| FWBF 비트 선택(파이프라인 비교기, flip 결정) | 대응 없음 | Prime ECC는 min-sum 기반이며 bit-flipping 계열 flip 결정 로직 자체가 없음 |
| 메트릭 값 계산(En, wn,m) | 대응 없음 | WBF 고유 metric으로 min-sum LLR 갱신과 무관 |
| 부분병렬 블록 구조/파이프라인 지연 단축 아이디어 | `decoder.cpp` `LDPC_Decoder()` | 파이프라인화 개념 자체는 일반적 HW 설계 원리로 참고 가능하나 알고리즘 계열이 다름 |

> 적용 가치: 낮음 - BF 계열(min-sum 아님) 알고리즘이며 코드도 EG-LDPC 구성법 기반이라 Prime ECC의 min-sum QC-LDPC 구조와 직접 대응되는 모듈이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1206.3362v1",
  "title": "An Improved WBF Algorithm for Higher-Speed Decoding of LDPC Codes",
  "year": 2012,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.69~0.76",
  "code_length": "255~1023",
  "soft_quant": "soft-4bit+",
  "key_contribution": "파이프라인 비교기 네트워크로 다중비트 flip 후보 선택을 부분병렬화해 MLP-WBF 대비 결정 지연을 줄인 FWBF 알고리즘 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "대상 부호가 EG-LDPC(finite geometry)이며 min-sum이 아닌 weighted bit-flipping 계열이라 Prime ECC 3.1의 min-sum 아키텍처와 알고리즘 계열 자체가 다름",
  "todo_check": "본문에 정확한 gatecount/throughput 수치가 없어 실제 HW 이득 크기 확인 불가"
}
```
