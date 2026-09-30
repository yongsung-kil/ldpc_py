### arxiv:2306.12063v1 - High Throughput Open-Source Implementation of Wi-Fi 6 and WiMAX LDPC Encoder and Decoder (2022, ITA)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.83 |
| 부호length | 576~2304 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Wi-Fi6(802.11ax)/WiMAX(802.16) QC-LDPC용 오픈소스 C99 direct 인코더 + layered single-scan min-sum 디코더(float/16bit fixed) 구현 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 0.044Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | 부분 |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | 표준 min-sum/layered/single-scan 재구현으로 신규 알고리즘 없음, HW 미설계, x86 소프트웨어 throughput만 |
| 추가확인 | single-scan min1/min2 sign-bitmap 메모리 절감 트릭이 Prime ECC의 min-sum 메모리 구조와 정합되는지 (이미 보유일 가능성 높음) |

> 총평: 표준 QC-LDPC 인코더/디코더의 교과서 알고리즘(direct encoding + layered single-scan min-sum)을 이식성 좋은 C99로 재구현한 오픈소스 툴킷으로, 신규 기법이 없어 Prime ECC 추천도는 하.

### B. 알고리즘 요약

1. 대상: IEEE 802.11ax(Wi-Fi6)·802.16-2017(WiMAX) 표준 QC-LDPC 부호, `N=576~2304`, rate `1/2·2/3·3/4·4/5·5/6`, 확장인자 `Z`(Wi-Fi {27,54,81}, WiMAX 24~96).
2. 문제: 빠른 C/C++ 구현과 MATLAB 통합을 동시에 제공하는 오픈소스가 부재(기존은 HW 또는 폐쇄형 MEX).
3. 인코딩: G행렬 없이 model matrix `Hbm`만으로 direct encoding — 부블록 `Z`bit의 `P_{i,j}` 곱셈을 순환시프트+GF(2) XOR로 대체(식 12~15), 합항 `S_i` 재사용.
4. 인코더 구현: universal array형과 최소메모리 bitmap(packed-bits)형 2종, `Z`가 word폭 배수일 때 단일스캔 순환시프트 알고리즘 A1(WiMAX 절반만 적용, Wi-Fi Z는 비정렬로 부적합).
5. 디코더 핵심: layered single-scan min-sum, CN 갱신 `L_mn = min_{n'≠n}|Z_mn'| · Πsgn` (식 18/23), VN 갱신 `Z_mn = Z_n − L_mn` (식 22).
6. 의미: single-scan은 CN 출력이 최소/차소 두 magnitude만 가짐을 이용, sign을 bitmap으로 분리 저장해 메모리를 대폭 절감(Wi-Fi R=5/6 max degree 20에서 18개 magnitude 절약, `L_mn`만 저장해 ~50% 절감).
7. layered: 체크노드를 `Z` block-row tier로 묶어 super-iteration 구성 → 수렴 가속으로 iteration 수 감소.
8. 고정소수점: `int16_t`에 `QB=10`bit + sign으로 표현, 상위 5bit 여유로 overflow 완화(저rate·큰 N에서 손실 큼).
9. 결과: float 디코더는 상용 MATLAB R2021b 대비 BER 시각적으로 동일, fixed-point는 약 0.1dB 손실; 단일스레드는 상용의 ~60%, 멀티스레드(AMD 32T fixed MTX)는 43.95Mbps로 상용 멀티스레드 대비 약 한 자릿수 우위.
10. 한계: HW 미설계, 표준 알고리즘 재구현(신규 기법 없음), throughput은 x86 소프트웨어 벤치마크 한정.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| layered single-scan min-sum CN 갱신 | decoder.cpp CNU_Update_New_Mag(), C2V_Cal_New_Sgn() | 동일 min1/min2 + sign 방식 — Prime ECC 이미 보유(중복) |
| VN 갱신 / posterior LLR | decoder.cpp VN_Cal_HD() 등, LDPC_Decoder() 루프 | 표준 min-sum VN 처리, 이미 보유 |
| direct encoding (Hbm 순환시프트) | encoder.cpp LDPC_encoder_4KB(), Generate_PCM_encoding() | 방식 유사(dual-diagonal vs double-diagonal), 참고 가능 |
| 16bit fixed-point 양자화(QB=10) | ecc_data.h PARAM_LLR, decoder.cpp Get_VNU_Table_Idx() | Prime ECC는 magnitude 양자화 테이블 사용 — 개념 유사 |
| 조기종료(H x̂=0 syndrome check) | full_CRC.cpp / partial_CRC.cpp | Prime ECC는 CRC 기반 조기종료 사용, 방식 상이 |
| soft-info 표준(802.11/802.16 QC-LDPC 부호) | 대응 없음 (무선 표준 부호, NAND용 아님) | 부호 자체는 NAND에 부적합 |
```

적용 가치: **낮음** — 표준 layered single-scan min-sum과 direct encoding을 이식성 좋게 재구현한 오픈소스 참조코드로, Prime ECC가 이미 보유한 기법과 중복. 무선 표준 부호라 부호설계 이식가치도 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:2306.12063v1",
  "title": "High Throughput Open-Source Implementation of Wi-Fi 6 and WiMAX LDPC Encoder and Decoder",
  "year": 2022,
  "venue": "ITA",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "576~2304",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Wi-Fi6(802.11ax)/WiMAX(802.16) QC-LDPC용 오픈소스 C99 direct 인코더 + layered single-scan min-sum 디코더(float/16bit fixed) 구현",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": 0.044,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "부분",
  "latency": "동등",
  "recommend": "하",
  "caveat": "표준 min-sum/layered/single-scan 재구현으로 신규 알고리즘 없음, HW 미설계, x86 소프트웨어 throughput만",
  "todo_check": "single-scan min1/min2 sign-bitmap 메모리 절감 트릭이 Prime ECC의 min-sum 메모리 구조와 정합되는지 (이미 보유일 가능성 높음)"
}
```
