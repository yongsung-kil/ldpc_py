### arxiv:1107.3253v2 - Spatially-Coupled Codes and Threshold Saturation on Intersymbol-Interference Channels (2011, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | ISI 채널에서 spatial coupling의 threshold saturation을 EXIT/GEXIT + area theorem으로 규명, SC 부호가 joint BP로 SIR에 보편적 접근 |
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
| 한계,주의 | ISI(dicode/자기기록) 채널·SC-LDPC convolutional 대상 순수 이론이라 NAND memoryless binary QC-LDPC와 채널·부호구조가 상이 |
| 추가확인 | (없음 - NAND 이식 관점에서 재검토 가치 낮음) |

> 총평: ISI 채널 SC-LDPC의 SIR 접근을 EXIT/GEXIT 이론으로 증명한 정보이론 논문으로, NAND binary QC-LDPC 디코더/HW 이식과 무관.

### B. 알고리즘 요약

1. 대상 시스템: binary-input ISI 채널(dicode `a(D)=1-D`, DEC/pDEC 및 dicode AWGN) 위에서 채널 그래프+부호 그래프를 합친 joint(turbo equalization) BP 디코더.
2. 풀려는 문제: irregular LDPC 부호를 ISI 채널마다 별도 설계해야 universality가 없음 → 채널 파라미터 없이 SIR에 보편적으로 접근하는 방법.
3. 핵심 아이디어: spatially-coupled(=LDPC convolutional) `(l,r,L)` / `(l,r,L,w)` 앙상블의 threshold saturation - BP threshold가 저변 정규 앙상블의 MAP threshold로 상승.
4. 핵심 기법 1: erasure(GEC)에 대해 joint BP의 (E)BP-EXIT 곡선을 폐형식으로 유도, area theorem으로 MAP threshold 상한 `¯MAP` 계산.
5. 핵심 식 의미: `∫ hEBP(x) dε(x) = r` (area=design rate) → EBP 곡선의 최좌점이 BP threshold, 면적조건이 MAP threshold를 준다.
6. 핵심 기법 2: 일반 ISI+AWGN에는 BP-GEXIT 곡선을 GEXIT kernel로 구성하고 동일 area theorem으로 `¯hMAP` 상한 도출 (BCJR/DE + Monte Carlo로 수치계산).
7. 구현 디테일: circular `(l,r,L)` 앙상블에서 각 row 앞의 pilot bit로 trellis state 고정 → row별 BCJR 병렬 실행.
8. 이론 결과: `(l,r)`-정규 앙상블에서 `l,r→∞`, rate 고정 시 `¯MAP → SIR` 증명 (Theorem 2).
9. 수치 결과: DEC (3,6) `BP≈0.569 → MAP≈0.639≈SIR 0.640`; dicode AWGN `σBP(3,6)≈1.70dB → σBP(3,6,22)≈0.959dB≈σ¯MAP`, (5,10,44)는 `σSIR≈0.823dB`에 근접.
10. 한계: memoryless NAND가 아닌 memory/ISI 채널 전용, HW/양자화 없음, threshold saturation의 해석적 증명은 미해결(수치 증거만).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-LDPC / (l,r,L,w) 부호구조 | 대응 없음 | Prime ECC는 고정 binary QC-LDPC(base+circulant)로 convolutional/coupled 구조 미지원 |
| joint BP + BCJR trellis(ISI 채널) | 대응 없음 | NAND는 memoryless, ISI equalization trellis가 없음 |
| EXIT/GEXIT area theorem MAP threshold 분석 | 대응 없음 | 이론적 threshold 분석 도구로 코드베이스에 대응 모듈 없음 |
| DE(density evolution) 기반 threshold 계산 | 대응 없음 | 부호설계·분석 단계 도구로 Prime ECC 시뮬 오케스트레이션(ecc_top.cpp)과 무관 |

적용 가치: **낮음** — ISI 채널 SC-LDPC의 SIR 접근을 다루는 순수 이론이라 NAND memoryless binary QC-LDPC 디코더/HW에 떼어낼 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1107.3253v2",
  "title": "Spatially-Coupled Codes and Threshold Saturation on Intersymbol-Interference Channels",
  "year": 2011,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": 0.5,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "ISI 채널에서 spatial coupling의 threshold saturation을 EXIT/GEXIT + area theorem으로 규명, SC 부호가 joint BP로 SIR에 보편적 접근",
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
  "caveat": "ISI(dicode/자기기록) 채널·SC-LDPC convolutional 대상 순수 이론이라 NAND memoryless binary QC-LDPC와 채널·부호구조가 상이",
  "todo_check": "없음 - NAND 이식 관점에서 재검토 가치 낮음"
}
```
