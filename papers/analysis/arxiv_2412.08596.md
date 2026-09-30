### arxiv:2412.08596v1 - Quantum-enhanced belief propagation for LDPC decoding (2024, arXiv/quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.67 |
| 부호length | 12 |
| 연판정 | hard-1bit |
| 핵심기여 | QAOA(양자근사최적화) 신드롬 디코딩을 min-sum BP의 warm-start 전처리로 결합해 BLER·수렴 iteration 감소 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | 양자컴퓨터(QAOA/NISQ) 필수, 블록길이 12~13 극소, 라운드마다 파라미터 재최적화로 실제 throughput 저하 |
| 추가확인 | 없음 (양자 HW 전제로 NAND 컨트롤러 이식 비현실적) |

> 총평: BP의 초기 LLR를 QAOA 신드롬 디코딩 결과로 warm-start하는 양자-고전 혼합 디코더. 양자 HW 전제·극소 블록 한계로 NAND binary QC-LDPC 이식 불가.

### B. 알고리즘 요약

1. 시스템: `[12,8]` regular(2,3)/irregular LDPC 및 `[n,1]` 반복부호, BSC/AWGN+BPSK 채널 (경판정 후 BSC 등가).
2. 문제: BP는 짧은 부호의 Tanner graph cycle 때문에 ML에 못 미치고 수렴 iteration이 지연을 유발.
3. 핵심 기법 QEBP: QAOA를 BP의 전처리로 사용 - 신드롬 `s=yHᵀ`에 대해 QAOA로 비트별 오류확률 `ε_i^QAOA`(식14)를 추정.
4. QAOA는 cost Hamiltonian `C=-η Σ(1-2s_j)ΠZ - α ΣZ_j`(식9, 패리티만족+오류가중치최소화)를 p층 회로로 최소화.
5. 채널 결합: QAOA를 2차 BSC로 보고 원 BSC와 concatenate → `ε_i=(1-ε_BSC)ε_QAOA+ε_BSC(1-ε_QAOA)`(식16)로 초기 LLR `L(v_i)` 계산.
6. 이후 표준 min-sum BP: CN `L(c_ji)=Π sign·min|β|`(식21), VN `L(q_ij)=L(v_i)+ΣL(c_j'i)`(식22) 반복.
7. one-sample 변형: 최다 측정 샘플로 `ε_QAOA∈{0,1}` 이진 할당 (추정확률 대신).
8. 반복부호 분석: transfer matrix 고유값(식28)으로 level-1 QAOA의 공유 파라미터 `γ≈0.194, β≈0.506` 최적화, 신드롬/길이 무관 재사용성 조사.
9. 결과: 블록길이 12에서 QEBP가 BP 대비 BLER 13~40% 개선, 수렴 iteration 평균 35% 감소(regular one-sample은 53.7%). post-selection은 최대 72% BLER 저감.
10. 한계: HW 미설계, 시뮬만. NISQ 노이즈로 대형부호(3GPP 최대 8448) 불가, 라운드마다 QAOA 파라미터 재최적화 필요 → 처리량 저하.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum BP CN/VN 업데이트(식21,22) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 이미 보유한 min-sum과 동일, 신규성 없음 |
| QAOA 전처리로 초기 LLR warm-start | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | 초기 LLR 주입 지점은 존재하나 QAOA는 양자 HW 필요 → 대응 불가 |
| QAOA 신드롬 디코더(양자회로) | 대응 없음 | 양자 알고리즘, NAND 고전 컨트롤러에 미대응 |
| 조기종료(신드롬 `s=vHᵀ=0`) | full_CRC.cpp | 개념 유사하나 표준적, 신규성 없음 |

적용 가치: 낮음 - 디코더 본체는 이미 보유한 min-sum이고, 핵심 신규성인 QAOA 전처리는 양자 HW(NISQ) 전제에 블록길이 12 수준이라 NAND binary QC-LDPC 컨트롤러 이식이 원천 불가.

### D. JSON 블록

```json
{
  "id": "arxiv:2412.08596v1",
  "title": "Quantum-enhanced belief propagation for LDPC decoding",
  "year": 2024,
  "venue": "arXiv/quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.67,
  "code_length": "12",
  "soft_quant": "hard-1bit",
  "key_contribution": "QAOA 신드롬 디코딩을 min-sum BP의 warm-start 전처리로 결합해 BLER·수렴 iteration 감소",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "악화",
  "recommend": "하",
  "caveat": "양자컴퓨터(QAOA/NISQ) 필수, 블록길이 12~13 극소, 라운드마다 파라미터 재최적화로 throughput 저하",
  "todo_check": "없음 (양자 HW 전제로 NAND 컨트롤러 이식 비현실적)"
}
```
