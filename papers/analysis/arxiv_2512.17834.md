### arxiv:2512.17834v1 - A 14 ns-Latency 9 Gb/s 0.44 mm2 62 pJ/b Short-Blocklength LDPC Decoder ASIC in 22FDX (2025, arXiv cs.AR)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.75 |
| 부호length | 128~256 |
| 연판정 | soft-4bit+ |
| 핵심기여 | MP 친화 short-blocklength binary QC-LDPC 설계 + 완전병렬 ANMS 디코더 ASIC로 최저 latency 달성 |
| HW설계 | O |
| 검증수준 | 실측 |
| 복잡도 | 0.44mm2@22FDX |
| 병렬화 | 완전병렬 |
| Throughput | 9~22Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | 5G URLLC/AWGN 무선 타깃·short-blocklength(128~256bit)라 NAND 고rate·긴부호와 격차, 완전병렬은 NAND ECC 면적에 부담 |
| 추가확인 | ANMS(ML학습 edge-weight α_ij)가 min-sum 대비 실이득 & Prime ECC 적응형 LLR과 중복 여부, fixed-point 7bit(4.2.1) 양자화 이식성 |

> 총평: ML최적화 edge-adaptive NMS + 완전병렬 flooding ASIC로 극저 latency를 실측 입증한 실전 논문이나, short-blocklength 무선 URLLC용 부호설계라 NAND 고rate QC-LDPC엔 부분 이식(ANMS scaling, ET, pipeline interleaving) 수준.

### B. 알고리즘 요약

1. 시스템: 5G URLLC용 binary QC-LDPC, 3rate(`R=1/2,2/3,3/4`), `(k,n')=(64,128)/(128,192)/(192,256)`, AWGN+BPSK 채널.
2. 문제: URLLC는 short-blocklength가 필요한데 기존 MP-LDPC는 short 부호에서 성능·저latency HW가 부족, polar SCL은 순차적이라 latency·면적 효율이 나쁨.
3. 부호설계: protograph 기반 rate-compatible AR4A(`Hproto` 3×9)를 2단 lifting — 1단 PEG(`Z=4`, girth↑), 2단 ACE(`Z=8`, `dACE=3, ηACE=13`)로 short cycle 연결성 확보.
4. rate 조정: PC matrix `H`의 앞 64/128열을 제거하고 정보비트 puncturing으로 3rate 지원.
5. 복호: flooding 스케줄 완전병렬 MP + edge-adaptive normalized min-sum(ANMS) `ℓ_cj ≈ α_ij × Π sign(ℓ_k) × min|ℓ_k|`.
6. `α_ij`(edge별 scaling)는 오프라인 ML 학습(deep-learning decoder [8]) + SNR deweighting·BLER loss fine-tuning으로 결정, 전 iteration 공유 → HW는 상수 곱만 필요.
7. HW 트릭: pipeline interleaving으로 2 codeword 동시 처리(throughput↑, latency 유지), early termination(ET)으로 pipeline freeze(전력↓), fixed-point 7bit(정수4+소수2+부호1).
8. 아키텍처: `N=288` VN 블록 + `M=96` CN 블록, CN은 min1/min2 추출 + sign XOR, sign-magnitude↔2's complement 변환 PU.
9. 결과: 22FDX ASIC 실측, `0.44mm2`, throughput 9/16/22Gbps, latency 13.78/16.06/17.52ns(최저), `62pJ/b`; 5G LDPC-SPA 대비 0.3~0.5dB BLER 이득, refined NA bound와 1.5dB 격차.
10. 한계: 무선 URLLC/AWGN 전제, short-blocklength(≤256bit)라 NAND 고rate·긴부호와 직접 비교 불가, iteration 감소 기여는 없음(`Imax=10` 고정).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| edge-adaptive normalized min-sum(ANMS) CN 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime ECC min-sum(min1/min2+sign XOR)과 동일 골격, edge별 학습 scaling만 추가 |
| ML학습 edge-weight α_ij scaling 테이블 | decoder.cpp `Get_VNU_Table_Idx()`, ecc_data.h `PARAM_LLR` | 적응형 LLR 테이블 구조와 유사 — normalized factor를 edge별로 확장 가능 |
| early termination(ET) | full_CRC.cpp, partial_CRC.cpp `partial_crc_HW_T4()` | 조기종료 기법 존재하나 논문은 PC(신드롬) 기반, Prime ECC는 CRC 기반으로 상이 |
| 완전병렬 flooding + pipeline interleaving | 디코더 HW 모델(z=32, pipeline 6-stage) | Prime ECC는 row 단위 병렬(z=32), 논문은 부호 전체 완전병렬 → 구조 정합 필요 |
| protograph/PEG/ACE 부호설계 | ecc_top.cpp `Load_PCM()` | 부호구조 자체가 다름(short-blocklength AR4A) — H-matrix 재검증 부담 큼 |

적용 가치: **중간** — ANMS의 edge-adaptive scaling 아이디어와 ET·pipeline interleaving은 Prime ECC min-sum 디코더에 부분 이식 여지가 있으나, short-blocklength 무선 부호설계·완전병렬 아키텍처는 NAND 고rate QC-LDPC 구조와 격차가 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2512.17834v1",
  "title": "A 14 ns-Latency 9 Gb/s 0.44 mm2 62 pJ/b Short-Blocklength LDPC Decoder ASIC in 22FDX",
  "year": 2025,
  "venue": "arXiv cs.AR",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.5~0.75",
  "code_length": "128~256",
  "soft_quant": "soft-4bit+",
  "key_contribution": "MP 친화 short-blocklength binary QC-LDPC 설계 + 완전병렬 ANMS 디코더 ASIC로 최저 latency 달성",
  "hw_designed": "O",
  "verification": "실측",
  "complexity": "0.44mm2@22FDX",
  "parallelism": "완전병렬",
  "throughput_gbps": "9~22",
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "중",
  "caveat": "5G URLLC/AWGN 무선 타깃·short-blocklength(128~256bit)라 NAND 고rate·긴부호와 격차, 완전병렬은 NAND ECC 면적에 부담",
  "todo_check": "ANMS(ML학습 edge-weight α_ij)가 min-sum 대비 실이득 & Prime ECC 적응형 LLR과 중복 여부, fixed-point 7bit 양자화 이식성"
}
```
