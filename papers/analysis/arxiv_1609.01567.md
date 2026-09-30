### arxiv:1609.01567v2 - OpenCL/CUDA algorithms for parallel decoding of any irregular LDPC code using GPU (2017, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 256~262144 |
| 연판정 | soft-2~3bit |
| 핵심기여 | edge-level 병렬화(1 thread=1 edge)로 최대 node degree 제약 없이 임의 irregular LDPC를 GPU에서 SP 복호+syndrome 병렬 계산 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | GPU(OpenCL/CUDA) SW 가속·BER 시뮬 도구일 뿐, ASIC/RTL HW 디코더가 아니며 정정성능 개선 없음 |
| 추가확인 | edge-level 스레드 매핑 아이디어가 z=32 row 병렬 HW 구조와 개념적 참고가 되는지 정도 |

> 총평: 임의 irregular LDPC를 GPU에서 edge-level 병렬 SP 복호하는 튜토리얼성 소프트웨어 구현. 알고리즘은 무손실 full SP 그대로이고 GPU 가속·BER 시뮬 용도라 NAND HW ECC(min-sum, z=32) 이식 가치는 낮음.

### B. 알고리즘 요약

1. 시스템: 임의 irregular LDPC (예제 (14,7); 벤치는 NASA CCSDS (256,128) 및 protograph 확장 rate 1/2, N=256~262144), AWGN+BPSK, Encoder-Channel-Decoder.
2. 문제: LDPC 복호는 계산량이 크고 중·장블록에서 non-approximated 복호가 느림. 기존 GPU 디코더는 특정 code family 또는 최대 node degree에 제한.
3. 핵심 가정: soft-decision Sum-Product(SP) 그대로 사용(단순화·근사 없음). AWGN에서 `pj=1/(1+exp(-2yj/σ²))` 확률 초기화.
4. 핵심 기법: edge-level 병렬화 — 스레드 1개가 edge 1개의 outgoing message를 계산. row/column 단위가 아닌 edge 단위라 임의 degree·구조 지원.
5. 핵심 식: message는 destination 제외 이웃의 곱(VN) / `ri0=1/2+1/2·∏(1-2qi1)`(CN, 식 Alg.1) — 표준 SP 확률 도메인 갱신.
6. 확장: syndrome `z=cH^T`도 병렬 계산(Algorithm 7). 조기종료는 syndrome all-zero 검사(전체 복호의 ~34%가 이 직렬 검사).
7. 구현 디테일: edge를 e/v/c/t/s/u 6개 address iterator 배열로 표현(Edge 구조체). working group(≤1024 threads) 한계 초과 시 edge를 page 단위로 분할.
8. 최적화: local(shared) memory 사용 시 ~40% 가속하나 local mem 240kB 제한으로 장블록 불가. lower precision/LUT/특정 family 특화 등 여지 언급.
9. 결과: NVIDIA Tesla K40에서 CPU(C++ O3) 대비 최대 22배(비최적화 대비 최대 58배), N=262144에서 25배. OpenCL vs CUDA 거의 동등(CUDA 소폭 우세).
10. 한계: 정정성능 개선 없음(알고리즘 무변경), HW/ASIC 설계 아님, GPU SW·BER 시뮬 가속 목적. throughput(Gbps)·gate count 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| edge-level 병렬 SP 복호 루프 | decoder.cpp `LDPC_Decoder()` | Prime ECC는 HW min-sum·z=32 row병렬, GPU thread 매핑과 구조 상이 |
| full-tanh/probability Sum-Product | 대응 없음 | Prime ECC는 min-sum 근사 사용, full SP 미사용 |
| syndrome 병렬 계산 / 조기종료 | partial_CRC.cpp `partial_crc_HW_T4()` | Prime ECC는 CRC 조기종료 사용, syndrome all-zero 방식과 별개 |
| GPU/OpenCL 프레임워크 | 대응 없음 | Prime ECC는 C++ bit-exact HW 시뮬레이터, GPU 무관 |

마지막에 한 문장으로 **적용 가치**: 낮음 — 근사 없는 full SP를 GPU에서 가속하는 SW/BER-시뮬 도구로, Prime ECC의 min-sum·고정 QC-LDPC·HW(z=32) 파이프라인과 알고리즘·아키텍처가 모두 달라 이식 가치가 낮다.

### D. JSON 블록

```json
{
  "id": "arxiv:1609.01567v2",
  "title": "OpenCL/CUDA algorithms for parallel decoding of any irregular LDPC code using GPU",
  "year": 2017,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "256~262144",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "edge-level 병렬화(1 thread=1 edge)로 최대 node degree 제약 없이 임의 irregular LDPC를 GPU에서 SP 복호+syndrome 병렬 계산",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "하",
  "caveat": "GPU(OpenCL/CUDA) SW 가속·BER 시뮬 도구일 뿐 ASIC/RTL HW 디코더가 아니며 정정성능 개선 없음",
  "todo_check": "edge-level 스레드 매핑 아이디어가 z=32 row병렬 HW 구조에 개념적 참고가 되는지 정도"
}
```
