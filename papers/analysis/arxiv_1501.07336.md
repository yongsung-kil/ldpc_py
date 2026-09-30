### arxiv:1501.07336v1 - Generalized Simplified Variable-Scaled Min Sum LDPC decoder for irregular LDPC Codes (2015, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5~0.75 |
| 부호length | 16200~64800 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Min-sum 체크노드 스케일링 인자를 iteration에 따라 `α = 1-(1-α0)*2^-(⌈i/S⌉-1)` 형태로 지수 증가시키되 초기값 α0까지 DE+Nelder-Mead로 공동 최적화(GSVS-min-sum)해 기존 SVS-min-sum·2D correction min-sum 대비 WER·평균 iteration을 동시 개선. |
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
| 추천도 | 중 |
| 한계,주의 | 회로 개념도(barrel shifter 기반)만 제시되고 실제 HW 합성/검증은 없음(시뮬 MATLAB); DVB-T2 eIRA 부호·256QAM/BPSK 채널 기준으로 NAND soft-read 채널과는 다름; 스케일링 factor (α0,S)는 부호율별 offline DE 최적화가 필요. |
| 추가확인 | Prime ECC의 min-sum 정규화/스케일링 방식(§3, magnitude 양자화 테이블 기반)과 비교해 GSVS 방식이 실질적 추가 이득이 있는지, 그리고 barrel-shift 기반 스케일링이 기존 HW 파이프라인(6-stage)에 저비용으로 삽입 가능한지 확인 필요. |

> 총평: min-sum 스케일링 인자를 반복 구간별 지수 증가 시퀀스로 일반화하고 초기값까지 최적화한 저복잡도 기법으로, decoder.cpp의 CN 업데이트 로직에 상대적으로 낮은 난이도로 이식 검토 가치가 있다.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 irregular LDPC(DVB-T2 eIRA 부호, `(16200,7200)` rate 0.5, `(16200,11880)`·`(64800,48600)` rate 0.75)의 min-sum 기반 반복 복호, 채널은 AWGN 위 BPSK 또는 256-QAM.
2. 문제: 기존 scaled min-sum(상수 α)은 irregular 부호에 부적합, 2D correction min-sum은 CN/VN degree별 벡터 α,β를 요구해 복잡, variable-scaling(반복별 다른 α)은 저장 오버헤드가 큼; 저자들의 기존 SVS-min-sum도 시작값을 0.5로 고정해 성능 제한.
3. 채널 모델은 AWGN이며, QAM의 경우 all-zero codeword 가정이 성립하지 않아 LLR을 `Uch → Uch×(1-2Vk)` 형태로 보정한 PDF를 사용(식 8).
4. 핵심 기법(GSVS-min-sum): 체크노드 업데이트 `Ui→j = α · sign(·)·min|vj→i|`의 스케일 인자 α를 반복 구간(`S`마다 갱신)별로 `α = 1-(1-α0)·2^{-(⌈i/S⌉-1)}`로 지수 증가시켜 큰 반복에서 1에 수렴(식 7).
5. 핵심 식 의미: 초기 스케일 α0을 자유 파라미터로 일반화함으로써 기존 SVS(α0=0.5 고정)와 constant scaled min-sum(S=총반복수인 특수해)을 모두 GSVS의 부분집합으로 포함시켜 성능 하한을 없앰.
6. 확장/최적화: `(α0, S)`를 Density Evolution(DE)으로 계산된 `(Eb/N0)min`을 비용함수로 Nelder-Mead simplex 탐색을 이용해 offline 공동 최적화(단일 최소점임을 등고선(Fig.4)으로 확인).
7. 부수 트릭(HW 친화): `(1-α0)`을 `2^-i` 또는 `2^-j+2^-k` 형태로 제한해 barrel shifter 우측 시프트+뺄셈만으로 스케일 곱셈 구현(곱셈기 불필요), 반복 카운터로 시프트량 `⌈i/S⌉-1` 생성.
8. 학습 절차: 부호율마다 오프라인 DE+Nelder-Mead로 `(α0,S)` 1회 산출 후 그 값을 디코더 회로에 상수로 반영(런타임 최적화 아님).
9. 결과: `(16200,7200)` 256QAM에서 GSVS가 SVS 대비 WER=10^-3 지점에서 0.5dB 이득, 2D correction min-sum 대비 0.3dB 이득, LLR-SPA 대비 0.1dB 이내 gap(복잡도는 LLR-SPA보다 크게 낮음); 평균 iteration 수도 최소(latency·throughput 개선).
10. 한계: 최대 40 iteration MATLAB 시뮬 결과로 실제 HW 합성/게이트카운트 없음, DVB-T2 무선방송 표준 부호·QAM 변조 대상이라 NAND read 채널과 직접 검증되지 않음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Min-sum CN 스케일링(GSVS) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | CN magnitude 갱신 시 반복 구간별 지수 증가 스케일 인자 적용 지점과 직접 대응, 이식 난이도 낮음 |
| 반복(iteration)별 스케일 파라미터 관리 | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 기존 iteration별 LLR threshold 테이블 구조에 (α0,S) 기반 스케일 시퀀스를 유사하게 추가 가능 |
| barrel-shift 기반 스케일 곱셈 HW | 디코더 HW 모델(6-stage pipeline) | 곱셈기 대신 shift+subtract로 구현하는 저비용 방식이 기존 min-sum 연산 스테이지에 삽입 가능할지 검토 필요 |
| DE+Nelder-Mead 오프라인 파라미터 최적화 | 대응 없음 | Prime ECC는 자체 부호 최적화 도구가 없어 오프라인 산출된 (α0,S) 상수만 반영 가능 |

> 적용 가치: 중간 — 이미 보유한 min-sum/스케일링 기법과 유사한 영역이지만, 초기값까지 포함한 지수 스케일 시퀀스와 저비용 barrel-shift 구현은 waterfall 성능·평균 iteration 개선 여지가 있어 decoder.cpp 스케일링 로직에 검토 가치가 있음.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1501.07336v1",
  "title": "Generalized Simplified Variable-Scaled Min Sum LDPC decoder for irregular LDPC Codes",
  "year": 2015,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": "0.5~0.75",
  "code_length": "16200~64800",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Min-sum 체크노드 스케일링 인자를 iteration에 따라 α = 1-(1-α0)*2^-(⌈i/S⌉-1) 형태로 지수 증가시키되 초기값 α0까지 DE+Nelder-Mead로 공동 최적화(GSVS-min-sum)해 기존 SVS-min-sum·2D correction min-sum 대비 WER·평균 iteration을 동시 개선.",
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
  "recommend": "중",
  "caveat": "회로 개념도(barrel shifter 기반)만 제시되고 실제 HW 합성/검증은 없음(시뮬 MATLAB); DVB-T2 eIRA 부호·256QAM/BPSK 채널 기준으로 NAND soft-read 채널과는 다름; 스케일링 factor (α0,S)는 부호율별 offline DE 최적화가 필요.",
  "todo_check": "Prime ECC의 min-sum 정규화/스케일링 방식(§3, magnitude 양자화 테이블 기반)과 비교해 GSVS 방식이 실질적 추가 이득이 있는지, 그리고 barrel-shift 기반 스케일링이 기존 HW 파이프라인(6-stage)에 저비용으로 삽입 가능한지 확인 필요."
}
```
