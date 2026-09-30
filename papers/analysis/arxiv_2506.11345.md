### arxiv:2506.11345v1 - On the High-Rate FDPC Codes: Construction, Encoding, and a Generalization (2025, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.63~0.96 |
| 부호length | 128~16384 |
| 연판정 | 무관 |
| 핵심기여 | 최소거리 보장 base matrix 재배열 구성 + bidiagonal 저복잡도 순차 인코더 + d=6 일반화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | FDPC는 각 열 무게 2 고정의 별도 부호족(QC-LDPC 아님), high-rate·짧은 길이 특화로 Prime ECC의 고정 QC-LDPC 구조와 비정합 |
| 추가확인 | error-floor 영역 성능과 NAND급 rate(~0.9) BER 곡선이 그림에만 있어 본문 서술 부족 |

> 총평: FDPC는 무게-2 base matrix 기반 고rate 부호로 정정성능·수렴속도는 우수하나 binary QC-LDPC 구조가 아니고 HW 미설계라 Prime ECC 이식성 하.

### B. 알고리즘 요약

1. 대상: BI-AWGN/BPSK 채널의 고rate FDPC 부호, 예제 `(256,164)`, `(1024,844)`, `(16384,15660)` 등 짧은~중간 블록.
2. 문제: 5G LDPC/polar는 같은 iteration 수에서 고rate 단블록 정정성능·수렴이 부족.
3. 구성 base-1: `2t`행 `t^2`열 base matrix, 각 열에 정확히 1이 2개, 열그룹 크기 `2t-1, 2t-3, ..., 1`로 배치.
4. 그래프 해석: 행=정점, 열=간선인 decagon 그래프. 길이-4 사이클 수 `A4`=무게-4 codeword 수, 밀도 `1/t`.
5. 인코딩: `2t`번째 열만 수정해 `A|B`의 bidiagonal `A` 확보, `p_i = p_{i-1} + (b_i·m)`로 parity bit 순차 계산(Fig.1 인코더).
6. 확장 base-2: 최소사이클 길이 `d=6`(최소거리 6)이 되도록 열 제거, 크기 `(2t, t(t+1)/2)` base matrix 구성.
7. 랜덤 순열: submatrix `C`에 `num_per`회 열 순열을 아래로 append해 FDPC(N, N-2t(num_per+1)) 생성(Algorithm 1).
8. 복호: normalized min-sum(FDPC/LDPC), polar은 scaled min-sum(0.9375)/BP로 비교.
9. 결과: `(256,164)` 5-iter FDPC가 50-iter 5G LDPC·polar 대비 약 0.5 dB gain(FER 1e-3); `(1024,844)` 12-iter가 CA-SCL(L8) 및 50-iter LDPC와 대등, latency 대폭 낮음.
10. 한계: HW 미설계·시뮬만, non-NAND(BI-AWGN 통신) 타깃, 열무게 2 고정 별도 부호족.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| bidiagonal 순차 인코딩 (`p_i=p_{i-1}+b_i·m`) | encoder.cpp `LDPC_encoder_4KB()` | dual-diagonal 인코더와 개념 유사하나 부호족 상이 |
| FDPC base matrix 구성 | ecc_top.cpp `Load_PCM()` | QC-LDPC 고정 구조라 FDPC H-matrix 이식 부담 큼 |
| normalized min-sum 복호 | decoder.cpp `LDPC_Decoder()` | min-sum은 이미 보유(중복 기여) |

적용 가치: **낮음** — FDPC는 QC-LDPC가 아닌 별도 부호족이며 HW 미설계·통신 타깃이라 NAND binary QC-LDPC 코드베이스 이식 부담이 크다.

### D. JSON 블록

```json
{
  "id": "arxiv:2506.11345v1",
  "title": "On the High-Rate FDPC Codes: Construction, Encoding, and a Generalization",
  "year": 2025,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": "0.63~0.96",
  "code_length": "128~16384",
  "soft_quant": "무관",
  "key_contribution": "최소거리 보장 base matrix 재배열 구성 + bidiagonal 저복잡도 순차 인코더 + d=6 일반화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "FDPC는 각 열 무게 2 고정의 별도 부호족(QC-LDPC 아님), high-rate·짧은 길이 특화로 Prime ECC의 고정 QC-LDPC 구조와 비정합",
  "todo_check": "error-floor 영역 성능과 NAND급 rate(~0.9) BER 곡선이 그림에만 있어 본문 서술 부족"
}
```
