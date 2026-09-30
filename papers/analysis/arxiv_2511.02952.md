### arxiv:2511.02952v1 - DecodeX: Exploring and Benchmarking of LDPC Decoding across CPU, GPU, and ASIC Platforms (2025, arXiv cs.NI)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | QC-LDPC |
| 부호rate | 0.245~0.88 |
| 부호length | K=352~8440 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 5G LDPC 복호를 CPU/GPU/ASIC 플랫폼별로 통일 벤치마킹하는 프레임워크(DecodeX) 제시 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 6Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 알고리즘·부호설계 기여 없음; 기존 상용 5G LDPC 구현(FlexRAN/Aerial/ACC100)의 latency·throughput 측정에 국한 |
| 추가확인 | 없음 (NAND binary QC-LDPC 이식 요소 부재) |

> 총평: 5G vRAN용 LDPC 복호기의 플랫폼 간 latency 벤치마킹 논문으로, NAND용 부호설계/디코더 알고리즘 기여가 없어 Prime ECC 이식 가치 없음.

### B. 알고리즘 요약

1. 시스템: 5G NR vRAN baseband의 LDPC 복호를 CPU(FlexRAN)/GPU(Aerial, Sionna-RK)/ASIC(ACC100)에서 통일 인터페이스 `Decode{HW}-{Impl}`로 벤치마킹.
2. 문제: 이기종 플랫폼별 LDPC 복호 latency·에너지·데이터이동 특성이 체계적으로 비교되지 않음.
3. 코드: 5G NR 표준 QC-LDPC 2종 base graph(BG1/BG2), circulant shift, lifting size `Zc`로 확장, MCS별 code rate.
4. 핵심기법: 각 플랫폼의 실행 파이프라인(threading/SIMD, DPDK BBDev offload, CUDA kernel launch/stream)을 분해하여 layered belief-propagation 복호 latency를 MCS/SNR/PRB 함수로 프로파일링.
5. CPU: AVX512로 512-bit 레지스터당 32 LLR 병렬, TB 단위 코어 병렬(near-linear scaling).
6. ASIC: ACC100 eASIC를 DPDK `rte_bbdev` API로 구동, bulk enqueue/dequeue로 순차 대비 최대 30x throughput.
7. GPU: Aerial inline(GPUDirect RDMA로 GPU-resident 데이터 경로), Sionna-RK unified memory(Jetson).
8. 확장: PyAerial에 parallel LDPC 인터페이스(`cuphyErrorCorrectionLDPCTransportBlockDecode`) 추가, 다중 TB를 CUDA stream 동시 복호.
9. 결과: parallel GPU 복호가 kernel time 최대 20x 감소; ACC100 bulk가 순차 대비 최대 30x throughput(~6Gbps); ACC100/H200은 PRB 증가에도 latency 거의 일정.
10. 한계: 복호 알고리즘·부호설계 개선 없음; 상용 구현의 성능 측정·시스템 분석에 국한, error-correction 성능(BER) 미평가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 5G NR QC-LDPC belief-propagation 복호 | 대응 없음 | 표준 BP/full-BP, NAND용 min-sum과 상이하고 알고리즘 변형 아님 |
| 플랫폼 벤치마킹/프로파일링 | 대응 없음 | Prime ECC는 bit-exact C++ 시뮬레이터로 플랫폼 벤치마킹 목적이 아님 |
| DPDK BBDev/CUDA stream 오케스트레이션 | 대응 없음 | vRAN 런타임 스케줄링, NAND 컨트롤러와 무관 |

적용 가치: **낮음** — 부호설계·디코더 알고리즘·HW 아키텍처 기여가 없는 순수 플랫폼 벤치마킹 논문이라 NAND binary QC-LDPC ECC에 떼어 쓸 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2511.02952v1",
  "title": "DecodeX: Exploring and Benchmarking of LDPC Decoding across CPU, GPU, and ASIC Platforms",
  "year": 2025,
  "venue": "arXiv cs.NI",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "K=352~8440",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "5G LDPC 복호를 CPU/GPU/ASIC 플랫폼별로 통일 벤치마킹하는 프레임워크(DecodeX) 제시",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": 6,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "알고리즘·부호설계 기여 없음; 기존 상용 5G LDPC 구현(FlexRAN/Aerial/ACC100)의 latency·throughput 측정에 국한",
  "todo_check": "없음 (NAND binary QC-LDPC 이식 요소 부재)"
}
```
