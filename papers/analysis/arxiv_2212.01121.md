### arxiv:2212.01121v2 - Asymmetric adaptive LDPC-based information reconciliation for industrial quantum key distribution (2023, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | irregular |
| 부호rate | 0.5~0.9 |
| 부호length | 32000 |
| 연판정 | 무관 |
| 핵심기여 | a priori QBER 추정 기반 코드rate 선택 + 비블라인드 추가라운드 disclosure 규칙으로 비대칭 IR 효율 향상 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | QKD 정보조정(syndrome IR) 전용 - NAND ECC의 부호설계/디코더/HW 어디에도 이식점 없음 |
| 추가확인 | 없음 (도메인 불일치로 추가 조사 불요) |

> 총평: QKD 비대칭 정보조정용 rate-adaptive 프로토콜 논문. LDPC를 syndrome 조정에 쓰지만 기여는 QBER 추정·rate 선택·라운드 disclosure 규칙이라 NAND binary LDPC ECC와 무관, 이식성 하.

### B. 알고리즘 요약

1. 시스템은 decoy-state BB84 QKD의 고전 후처리 중 정보조정(IR) 단계, LDPC syndrome 방식(`s = H_R x mod 2`), frame=32000, α=0.15, subblock=27200.
2. 문제: 송신기(Alice)/수신기(Bob) 계산자원 비대칭 환경에서 대칭 blind IR 수준 효율을 자원 적은 쪽에서 유지하는 것.
3. 모델: BSC 근사, QBER `E_μ`를 채널상태로 보고 rate 풀 `R∈{0.5,0.55,...,0.9}`에서 선택.
4. 핵심기법 1 - a priori QBER 추정: 검증된 직전 프레임들의 지수이동평균 `EMA` (`γ=0.33`) + decoy-pulse QBER로 급변(3σ) 감지, 검증 실패 시 penalty `E_μ=0.5` 피드백.
5. 핵심식: `R_desired = 1 - f_start·h2(Ê_μ)` (`f_start=1.15`)로 목표 효율에서 rate를 역산, punctured `p`·shortened `s` 비트 수 결정.
6. 핵심기법 2 - 추가라운드 규칙: 기본 복호 실패 시 punctured 노드(true-random, 최소 LLR 경향) 값을 먼저 공개, 소진 후 payload 비트 공개, `d_k` 공식(11)로 라운드별 공개량 산정.
7. 구현 디테일: PEG로 PCM 생성, untainted puncturing, Mersenne-Twister 기반 interleaving으로 error burst 분산.
8. 복호기: variable-scaled Min-Sum (scaling step 12.5), Sum-Product 근사.
9. 결과: 제안 AEC가 대칭 SEC와 거의 동일 효율(`E_μ≳2%`), blind AEC 대비 throughput 약 2배, 실측 FER < 10^-3 (blind는 최대 ~10%@20dB).
10. 한계: single-processor·병렬 없음, HW 미설계, QKD 도메인 특화(NAND 무관), soft-read/양자화 논의 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| variable-scaled Min-Sum 복호 | decoder.cpp `CNU_Update_New_Mag()` | min-sum은 이미 보유, scaling만 다름 - 신규성 낮음 |
| rate-adaptive puncturing/shortening | 대응 없음 | Prime ECC는 고정 QC-LDPC(H-matrix 고정), rate 적응 미지원 |
| a priori QBER 추정 / 코드rate 선택 | 대응 없음 | 프로토콜 상위 로직, ECC 엔진 밖 |
| 추가라운드 bit disclosure (blind IR) | 대응 없음 | QKD 양방향 대화형 프로토콜 전용 |

적용 가치: **낮음** - QKD 정보조정 상위 프로토콜(QBER 추정·rate 선택·양방향 disclosure)이 기여의 전부이고, 복호기는 이미 보유한 min-sum 근사라 NAND binary QC-LDPC ECC에 떼어낼 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2212.01121v2",
  "title": "Asymmetric adaptive LDPC-based information reconciliation for industrial quantum key distribution",
  "year": 2023,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "irregular",
  "code_rate": null,
  "code_length": "32000",
  "soft_quant": "무관",
  "key_contribution": "a priori QBER 추정 기반 코드rate 선택 + 비블라인드 추가라운드 disclosure 규칙으로 비대칭 IR 효율 향상",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "QKD 정보조정(syndrome IR) 전용 - NAND ECC의 부호설계/디코더/HW 어디에도 이식점 없음",
  "todo_check": "없음 (도메인 불일치로 추가 조사 불요)"
}
```
