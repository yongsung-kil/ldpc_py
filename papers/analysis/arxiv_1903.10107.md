### arxiv:1903.10107v1 - High Throughput and Low Cost LDPC Reconciliation for Quantum Key Distribution (2019, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 100000 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 8-bit 고정소수 양자화 RCBP CN 처리 + saturation-oriented VN 처리로 CPU/SIMD 고throughput LDPC 복호 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 0.122 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | CPU/SIMD SW 최적화 타깃(HW 미설계), QKD reconciliation 특화·frame 100kb 대형, 정정능력 자체 향상 아님 |
| 추가확인 | 8-bit RCBP LUT(Algorithm 1)와 saturation VN 규칙이 z=32 min-sum 파이프라인/짧은 NAND frame에 정합되는지 |

> 총평: binary QC-LDPC layered 디코더의 8-bit 양자화·RCBP CN·saturation VN 최적화로 QKD SW용이나 양자화/포화 처리 아이디어는 NAND HW 디코더에 간접 참고 가치 있어 이식성 중.

### B. 알고리즘 요약

1. 시스템: DV-QKD 후처리 reconciliation, binary QC-LDPC(base `Mb×Nb`, expansion Z), frame `100kb`, rate-adaptive bi-directional, QBER 1~8%.
2. 문제: 고속 QKD에서 reconciliation이 병목, GPU는 고비용·집적 곤란, 저비용 CPU로 high throughput+efficiency 동시 달성 필요.
3. 핵심 모델: layered scheduling SPA(flooding 대비 수렴 2배), CN sign=곱, magnitude=box-plus/`φ(x)=-ln tanh(x/2)`, RCBP 근사 채택(CPU 친화).
4. 핵심 기법1(양자화): soft message를 `8-bit 고정소수`로 표현 → SSE/AVX SIMD lane 4배(FP 8 → int 32/clock), cache 적중률↑로 throughput 최소 4배.
5. 핵심 식 의미: 8-bit화가 SIMD utilization·cache hit를 올려 처리지연을 줄이지만 rough quantization이 reconciliation efficiency를 떨어뜨림.
6. 핵심 기법2(RCBP CN): 더 정밀한 양자화 step + 확대 LUT `τ(p,q)`, LUT 대신 단순 연산 Algorithm 1(MIN/MAX/비교)으로 계산(LUT 접근보다 빠름).
7. 핵심 기법3(VN): saturation-oriented VN 처리(Algorithm 2) — magnitude가 `Emax=127`에 도달한 VN은 갱신 안 함, 8-bit 포화로 인한 부호/크기 오류 방지.
8. 병렬화: SIMD=intra-frame, multi-core=inter-frame, 조기종료·AVX-2로 추가 2배, layered는 layer간 데이터 의존으로 GPU 부적합(CPU 유리).
9. 결과: i7-6700HQ 57.60 Mbps @ efficiency 1.108, GPU 대비 ×3.8, CPU[5] 대비 ×11.3 speedup; i9-9900K에선 122.17 Mbps, FPGA16와 대등 이상.
10. 한계: SW(CPU) 최적화 타깃이라 HW(RTL) 미설계, QKD reconciliation 특화(frame 100kb 대형), 정정능력 자체 향상이 아닌 throughput·efficiency 최적화.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| RCBP box-plus CN 처리(LUT/Algorithm 1) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 우리는 min-sum(min1/min2), RCBP는 box-plus 계열 대안 CN 근사 |
| 8-bit 고정소수 양자화 message | decoder.cpp `VN_Cal_HD()` 등, ecc_data.h `PARAM_LLR` | 양자화 magnitude 테이블 개념과 상통 |
| saturation-oriented VN 갱신 규칙 | decoder.cpp `LDPC_Decoder()` VN 이터레이션 | 포화 VN 미갱신은 우리 VN 루프에 얹을 수 있는 트릭 |
| layered scheduling / 조기종료 | decoder.cpp `LDPC_Decoder()`, partial_CRC.cpp `partial_crc_HW_T4()` | 우리는 Dual-Update 스케줄+Partial CRC 조기종료 이미 보유 |
| SIMD/multi-core 병렬화 | 대응 없음 | Prime ECC는 HW(z=32) 병렬 모델, x86 SIMD SW 최적화와 별개 |

적용 가치: **중간** — QKD 특화·SW(CPU) 타깃이라 그대로는 아니나, 8-bit 양자화 message의 saturation 처리와 RCBP CN 근사는 Prime ECC의 양자화 min-sum 디코더(양자화 정밀도/포화 오류 대응)에 간접 참고할 만하다.

### D. JSON 블록

```json
{
  "id": "arxiv:1903.10107v1",
  "title": "High Throughput and Low Cost LDPC Reconciliation for Quantum Key Distribution",
  "year": 2019,
  "venue": "arXiv quant-ph",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "미상",
  "code_length": "100000",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "8-bit 고정소수 양자화 RCBP CN 처리 + saturation-oriented VN 처리로 CPU/SIMD 고throughput LDPC 복호",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": 0.122,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "중",
  "caveat": "CPU/SIMD SW 최적화 타깃(HW 미설계), QKD reconciliation 특화·frame 100kb 대형, 정정능력 자체 향상 아님",
  "todo_check": "8-bit RCBP LUT(Algorithm 1)와 saturation VN 규칙이 z=32 min-sum 파이프라인/짧은 NAND frame에 정합되는지"
}
```
