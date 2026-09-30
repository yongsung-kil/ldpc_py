### arxiv:2510.21600v1 - Real-time decoding of the gross code memory with FPGAs (2025, arXiv/quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 144 |
| 연판정 | 무관 |
| 핵심기여 | Relay-BP(멀티-leg BP + disordered memory) qLDPC 디코더를 완전병렬 FPGA로 구현, int4~6 정밀도로 float 성능 유지하며 BP iter 24ns 달성 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | bivariate bicycle CSS 양자 LDPC 대상(syndrome 기반, 코드워드 아닌 error 추정), 우리 binary NAND QC-LDPC와 부호·채널 모델 상이. 완전병렬(노드당 전용 유닛) 방식은 z=32 pipeline HW와 정합 안 됨 |
| 추가확인 | int4 sign-magnitude 양자화·min-sum scaling α=1-2^-t 기법이 NAND min-sum 디코더에 단독 이식 가능한지, 완전병렬이 아닌 우리 GT/HCU 구조에서의 효용 |

> 총평: 우수한 실시간 FPGA qLDPC 디코더지만 양자 CSS 부호·syndrome 디코딩 전용이라 NAND binary QC-LDPC 이식성은 낮음(정밀도 양자화 아이디어 정도만 참고).

### B. 알고리즘 요약

1. 대상: `[[144,12,12]]` gross code 및 `[[56,2,10]]` Loon code (bivariate bicycle CSS 양자 LDPC)의 memory 실험용 실시간 디코더, biAWGN 아닌 circuit-level Pauli noise 모델.
2. 문제: 초전도 큐빗은 μs 단위 QEC 사이클이라 syndrome 도착보다 빠른 초저지연·고throughput 디코더 필요(backlog 회피). GPU/AI 가속기는 데이터전송·커널 지연으로 부적합.
3. 디코딩 프레임: check matrix `H`로 `σ=He`, 디코더는 syndrome `σ`만으로 error `ê` 추정(`Hê=σ` 및 논리 등가 `Aê=Ae`). X/Z 분리(split) 또는 XYZ 상관 디코딩.
4. 핵심 알고리즘 Relay-BP: DMem-BP(disordered memory strength `γ_j`를 BP에 주입) 서브루틴을 여러 leg로 순차 ensembling, 이전 leg의 최종 marginal을 다음 leg 초기값으로 전달하고 최저 weight 해 반환.
5. bias 갱신식 `Λ_j(t)=(1-γ_j)Λ_j(0)+γ_j M_j(t-1)`: memory strength로 과거 marginal을 반영, `γ_j=0`이면 표준 BP. Relay는 음수 memory strength까지 허용.
6. 메시지: CN은 min-sum `µ=κ·(-1)^σ·min|ν|`(min1/min2 + sign), min-sum scaling factor `α=1-2^-t` 적용. VN은 `ν=Λ+Σµ`, marginal `M=Λ+Σµ`, HD로 `ê`.
7. HW arch: Valls et al. 방식대로 그래프의 모든 VN/CN에 전용 compute unit 1:1 할당, 메시지를 FPGA 배선에 고정(중앙 메모리 contention 제거). VNU/CNU 각 1 clock, flooding schedule로 iter당 2 clock.
8. 저정밀 산술: sign-magnitude 정수 `intN.S.M`(scale S, memory scale M=2^m로 shift 구현), memory 곱셈을 비트확장+shift+null로 근사. split XZ는 int4, 상관 XYZ는 int6으로 float 성능 일치.
9. 결과: gross code split X/Z 디코더가 AMD XCVU19P FPGA에서 12ns clock→BP iter 24ns, p<10^-3에서 평균 ~20 iter 수렴 → 12-cycle window 480ns(cycle당 40ns), 1μs syndrome rate보다 빨라 backlog 없음. LUT 51.6% 사용.
10. 한계: 합성 syndrome 검증만(실측 QPU 미연결), 자원 소모 큼(최대급 FPGA 필요), 논리연산 디코딩 미확장, 양자 CSS 부호·noise 모델 특화.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| CN min-sum(min1/min2 + sign) 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 동일 min-sum이나 우리도 이미 보유(중복 기여), 양자 syndrome 디코딩 맥락 |
| VN 처리 / sign-magnitude 정수 양자화 | decoder.cpp `VN_Cal_HD()` 등, `decoder.h` `Get_VNU_*` | int4~6 저정밀 양자화 아이디어는 형식 유사하나 우리는 2SD/3SD LLR 테이블 기반이라 직접 이식 아님 |
| min-sum scaling α=1-2^-t | decoder.cpp `LDPC_Decoder()` 루프 | scaled min-sum은 우리 min-sum 근사와 대응, 다만 우리는 magnitude 양자화 테이블 사용 |
| Relay/DMem memory strength(γ) bias 갱신 | 대응 없음 | 우리 디코더에 memory-strength 개념 없음(양자 error-floor 대책 특화) |
| 완전병렬 노드-전용 유닛 + 배선 라우팅 | 대응 없음 | 우리는 z=32 row 병렬 pipeline+HCU/GT 구조라 노드 1:1 완전병렬과 정합 안 됨 |
| 조기종료(`Hê=σ` parity check) | partial_CRC.cpp `partial_crc_HW_T4()` | 우리는 CRC 기반 조기종료, 개념만 유사 |

적용 가치: **낮음** — bivariate bicycle CSS 양자 LDPC의 syndrome 디코더로 부호구조·채널·디코딩 대상이 NAND binary QC-LDPC와 상이하고, 완전병렬 배선 HW는 우리 pipeline 구조와 정합 불가. sign-magnitude 저정밀(int4) 양자화 정도만 참고 가치.

### D. JSON 블록

```json
{
  "id": "arxiv:2510.21600v1",
  "title": "Real-time decoding of the gross code memory with FPGAs",
  "year": 2025,
  "venue": "arXiv/quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "144",
  "soft_quant": "무관",
  "key_contribution": "Relay-BP(멀티-leg BP + disordered memory) qLDPC 디코더를 완전병렬 FPGA로 구현, int4~6 정밀도로 float 성능 유지하며 BP iter 24ns 달성",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "bivariate bicycle CSS 양자 LDPC 대상(syndrome 기반), binary NAND QC-LDPC와 부호·채널 모델 상이. 완전병렬 노드-전용 유닛 방식은 z=32 pipeline HW와 정합 안 됨",
  "todo_check": "int4 sign-magnitude 양자화·min-sum scaling α=1-2^-t의 NAND min-sum 디코더 단독 이식 가능성, GT/HCU 구조에서의 효용"
}
```
