### arxiv:2011.14753v3 - Метод, аппаратно-ориентированный алгоритм и специализированное устройство для построения низкоплотностных кодов архивной голографической памяти (2020, arXiv/PhD Thesis)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 32000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 홀로그래픽 메모리용 QC-LDPC 프로토그래프 구성(금지계수 탐욕법+시뮬레이티드 어닐링)과 격자 기반 코드거리 추정 FPGA 가속 장치 제안 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 러시아어 박사논문 전문(홀로그래픽 채널 특화), rate=0.5·length=32000 저rate 부호로 NAND ECC(고rate)와 스펙 상이, FPGA 장치는 코드 설계 단계(격자 최단벡터탐색)용이며 디코더/인코더 HW 아님 |
| 추가확인 | 제안 부호 A(d=54)/D(d=24)/B(d=22)의 정확한 프로토그래프 base matrix 구조 및 NAND 관계 채널(RBER)로의 이식 가능성 재확인 필요 |

> 총평: 홀로그래픽 메모리(AWGN 채널, R=0.5, N=32000) 대상 QC-LDPC 코드 구성법 논문으로, NAND binary LDPC(고rate)와는 채널·rate·목적이 달라 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: 홀로그래픽 아카이브 메모리 페이지 레벨 채널(AWGN 근사), QC-LDPC 부호 `R=0.5`, `N=32000`, 32비트 패리티체크 포함.
2. 문제: 기존 Density Evolution/PEG/Hill-Climbing 기반 구성법은 Tanner graph의 조합대수적 성질(ACE spectrum)과 코드거리(distance property)를 동시에 고려하지 못해 trapping set·저중량 코드워드가 남아 error-floor를 유발.
3. 채널 모델: 홀로그래픽 판독 채널을 다수의 병렬 AWGN 채널(페이지 단위)로 근사, LLR은 `μ1,μ0,σ1,σ0` 기반 가우시안 형태로 정의.
4. 핵심 기법 1단(프로토그래프 구성): 초기 base matrix를 Density Evolution 가중치 분포로 초기화 후, 랜덤 비트마스크 `M_{j,l}=rand(0,1)`로 값을 반전시키며 PEXIT-chart로 반복임계값(iterative decoding threshold) `Threshold=Eb/No(σ)`를 계산, `P_UB ≤ P_BER`이고 `Threshold ≤ SNR`이면 채택.
5. 핵심 식: `P_UB ≈ (ω_dmin·K/N)·Q(√(dmin·K/N·2Eb/N0))` — 최소 코드거리 `d_min`과 그 중복도 `ω_dmin`으로 error-floor 영역 오류확률을 근사, 코드거리가 부족하면 조기에 폴백.
6. 핵심 기법 2단(확장): 프로토그래프를 탐욕적 "금지계수(forbidden coefficients)" 알고리즘으로 1차 확장한 뒤, 시뮬레이티드 어닐링으로 순환 구조(EMD spectrum, trapping set 관련 cycle 12/14/16)를 추가 최적화하여 후보 코드 집합 `{C'}`를 생성.
7. 부수 트릭: 코드거리 정밀 추정을 위해 코드를 격자(lattice)에 매장하고 QR분해 병렬화 + branch-and-bound(슬라이딩 윈도우, 512차원 부분격자) 기반 최단벡터탐색을 FPGA로 가속(DSP 사용량 1/4, 소프트웨어 대비 33.93배 고속화).
8. 최적화 절차: PEXIT-chart(반복임계값) + Covariance Evolution(waterfall penalty 함수, `α,β,σ*` 계수) + Cole's Importance Sampling(trapping set BER 추정)을 결합해 후보 코드 랭킹/필터링.
9. 결과: 최종 선택된 코드 A(`d_min=54`)가 TrellisWare F-LDPC 대비 SNR=1.1dB에서 BER 8.9배, 1.6dB에서 최대 45455배 개선. FPGA 격자탐색 장치는 소프트웨어 대비 33.93배 가속.
10. 한계: 홀로그래픽 메모리 채널(저rate 0.5, N=32000, AWGN) 특화 설계이며 NAND flash RBER 채널·고rate 부호로의 일반화는 본문에서 다루지 않음. 제안 FPGA 장치는 코드 설계(오프라인) 단계 전용으로 실시간 디코더/인코더 HW가 아님.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| QC-LDPC 프로토그래프 구성(Density Evolution+어닐링) | `ecc_top.cpp` `Load_PCM()` | 특정 H-matrix 재설계로 이식 난이도 높음, 채널·rate 상이 |
| 코드거리(distance) 격자 추정 FPGA 장치 | 대응 없음 | Prime ECC는 오프라인 코드 설계 도구/격자탐색 HW 미보유 |
| trapping-set/ACE spectrum 최적화 | 대응 없음 | 부호 구성 단계 전용, 디코더 실행시간 모듈과 무관 |
| PEXIT-chart 반복임계값 계산 | 대응 없음 | 이론적 asymptotic 분석 도구, 코드 시뮬레이터에 대응 없음 |

적용 가치: 낮음 — 홀로그래픽 채널·저rate(0.5) QC-LDPC 구성법과 오프라인 격자기반 코드거리 추정 FPGA 장치로, Prime ECC의 고rate NAND binary QC-LDPC 디코더/HW 구조와 직접 대응되는 모듈이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2011.14753v3",
  "title": "Метод, аппаратно-ориентированный алгоритм и специализированное устройство для построения низкоплотностных кодов архивной голографической памяти",
  "year": 2020,
  "venue": "arXiv (PhD Thesis)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "32000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "홀로그래픽 메모리용 QC-LDPC 프로토그래프 구성(금지계수 탐욕법+시뮬레이티드 어닐링)과 격자 기반 코드거리 추정 FPGA 가속 장치 제안",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "러시아어 박사논문 전문(홀로그래픽 채널 특화), rate=0.5·length=32000 저rate 부호로 NAND ECC(고rate)와 스펙 상이, FPGA 장치는 코드 설계 단계(격자 최단벡터탐색)용이며 디코더/인코더 HW 아님",
  "todo_check": "제안 부호 A(d=54)/D(d=24)/B(d=22)의 정확한 프로토그래프 base matrix 구조 및 NAND 관계 채널(RBER)로의 이식 가능성 재확인 필요"
}
```
