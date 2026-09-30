### arxiv:1702.07740v2 - Key Reconciliation with Low-Density Parity-Check Codes for Long-Distance Quantum Cryptography (2017, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.02 |
| 부호length | 1000000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | multi-edge LDPC를 QC 구조로 확장 + GPU coalesced-memory Sum-Product 디코더로 CV-QKD reconciliation 거리 100->160km 연장 |
| HW설계 | O |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 0.00181Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | 부분 |
| latency | 개선 |
| 정정능력향상 근거 | QC화로도 random 대비 동등 FER 유지(q=50가 최적), d=8 reconciliation로 waterfall 0.2dB gain |
| 추천도 | 하 |
| 한계,주의 | rate 0.02·length 10^6·32bit float Sum-Product·GPU 타깃으로 NAND 고rate/고정소수점/ASIC 환경과 정반대, min-sum은 저SNR서 부적합이라 배제 |
| 추가확인 | QC circulant 구성·early-termination lookup 기법이 고rate QC-LDPC에도 이득 있는지 (본 논문은 저rate 특화) |

> 총평: CV-QKD 저SNR용 저rate(0.02) multi-edge QC-LDPC를 GPU에서 float Sum-Product로 돌리는 논문 — 부호/디코더/HW 스펙이 NAND 고rate binary QC-LDPC ASIC과 정반대라 이식 가치는 낮다.

### B. 알고리즘 요약

1. CV-QKD reverse reconciliation을 저SNR(-15dB 이하) BIAWGNC로 모델링, 채널을 `Y=X+Z`로 두고 LDPC로 오류정정.
2. 풀려는 문제: 100km 초과 거리에서 near-Shannon reconciliation에 필요한 rate 0.02·length 10^6 부호의 복호 복잡도/latency가 secret key rate 병목.
3. 부호: Richardson-Urbanke `multi-edge type` LDPC(type1=degree3/check7~8 고rate 서브그래프 + type2 parity + type3 degree-1 VN)를 채택, `Omega/Psi` 다변수 degree 분포.
4. 핵심 기법 1단: multi-edge를 QC로 확장 — base graph를 `n/q`로 샘플링 후 각 nonzero를 `q x q` circulant `I_i`로 치환(`q in {21,50}`), lower-triangular parity로 forward-substitution 인코딩.
5. 의미: circulant 구조가 permutation을 `q`배 적은 항으로 기술 -> GPU 메모리 접근/라우팅 대폭 축소.
6. 핵심 기법 2단: multi-dimensional reconciliation(`d in {1,2,4,8}`, octonion까지)로 waterfall에서 d=8이 d=1 대비 0.2dB gain -> 거리 연장.
7. 디코더: `Sum-Product`(`Phi(x)=-ln tanh(x/2)`) belief propagation, 32bit float; min-sum은 저SNR서 성능 부족이라 명시적으로 배제.
8. HW: NVIDIA GTX 1080 GPU에 4-kernel(VN->CN, CN update, CN->VN, VN update) 구현, coalesced write/edge reorder로 uncoalesced 접근 최소화, SNR별 avg-iteration lookup으로 early-termination.
9. 결과: q=50 QC가 random 대비 raw throughput ~3x(정보 throughput 5.1~12.8x), 최대 raw `1.807Mb/s`/info `7.16Kb/s`(q=21,d=8), 거리 100->160km, 기존 GPU 대비 1.29x.
10. 한계: 시뮬/GPU 측정만(ASIC/FPGA 없음), rate 0.02·length 10^6·float 연산으로 NAND ECC와 스펙 상이, error-floor는 QKD에서 무의미(FER~0.1 운용).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| multi-edge QC circulant 부호 구성 | ecc_top.cpp `Load_PCM()` | 둘 다 QC(base+circulant)지만 rate 0.02 vs 고rate, degree 구조 상이 — 부호 재사용 불가 |
| Sum-Product belief propagation (tanh/Phi) | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 우리는 min-sum 근사 채택 — 본 논문은 min-sum을 저SNR서 배제, HW ASIC엔 full-tanh 부적합 |
| 32bit float 양자화 | 대응 없음 | Prime ECC는 hard/2SD/3SD 고정소수점 양자화, float 미지원 |
| early-termination (avg-iter lookup) | partial_CRC.cpp `partial_crc_HW_T4()`, `full_CRC.cpp` | 우리도 CRC 조기종료 보유 — 개념 중복, lookup 방식만 상이 |
| GPU coalesced memory/edge reorder | 대응 없음 | Prime ECC는 z=32 ASIC pipeline 모델, GPU SIMT 메모리 최적화와 무관 |

**적용 가치**: 낮음 — QC-LDPC/조기종료라는 공통어는 있으나 rate 0.02·length 10^6·float Sum-Product·GPU라는 축이 NAND 고rate 고정소수점 ASIC과 정반대이고, 핵심인 GPU 메모리 최적화는 우리 HW 모델에 대응이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1702.07740v2",
  "title": "Key Reconciliation with Low-Density Parity-Check Codes for Long-Distance Quantum Cryptography",
  "year": 2017,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": 0.02,
  "code_length": "1000000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "multi-edge LDPC를 QC 구조로 확장 + GPU coalesced-memory Sum-Product 디코더로 CV-QKD reconciliation 거리 100->160km 연장",
  "hw_designed": "O",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": 0.00181,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "하",
  "caveat": "rate 0.02·length 10^6·32bit float Sum-Product·GPU 타깃으로 NAND 고rate/고정소수점/ASIC 환경과 정반대, min-sum은 저SNR서 부적합이라 배제",
  "todo_check": "QC circulant 구성·early-termination lookup 기법이 고rate QC-LDPC에도 이득 있는지 (본 논문은 저rate 특화)"
}
```
