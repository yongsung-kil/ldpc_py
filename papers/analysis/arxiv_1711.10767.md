### arxiv:1711.10767v2 - Parameter-free ℓp-Box Decoding of LDPC Codes (2018, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5 |
| 부호length | 2640 |
| 연판정 | 무관 |
| 핵심기여 | LP 복호의 이진제약을 box∩ℓp-sphere로 대체한 parameter-free ℓ2-box ADMM 복호기 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | LP/ADMM 계열 복호로 HW 미설계·CPU time만 측정, Min-Sum 대비 반복당 연산 비용 큼 |
| 추가확인 | 고rate NAND QC-LDPC에서의 ℓ2-box ADMM 수렴속도·error-floor 이득 실측 필요 |

> 총평: penalty parameter 없는 LP/ADMM 복호로 error-floor는 낮추나 NAND용 Min-Sum HW 엔진과는 계열이 달라 이식성 낮음.

### B. 알고리즘 요약

1. 대상은 binary linear LDPC `C` (길이 `N`, M×N parity-check `H`), AWGN 채널에서 [2640,1320] Margulis 및 [2304,768] WiMAX 부호로 실험.
2. 기존 penalized-LP(ADMM) 복호는 penalty parameter `α` 선택이 성능·속도·최적해에 결정적이라 SNR/채널마다 재튜닝이 필요한 것이 문제.
3. ML 복호 `min γ^T x` (LLR 벡터 `γ`)를 Feldman의 LP relaxation으로 완화하고, 국소 codeword 제약을 codeword polytope `PP_d`로 표현.
4. 핵심 기법: 이진제약 `x∈{0,1}^N`을 box `[0,1]^N` 와 ℓp-sphere `‖x-½1‖_p^p = N/2^p` 의 교집합으로 **정확히** 등가 치환 (parameter-free reformulation).
5. 이 등가식 덕분에 penalty 없이도 이진 복호의 전역 최적해가 곧 완화문제의 전역 최적해가 되어, α 튜닝 없이 정확도 확보.
6. 구현 단순화를 위해 `p=2`로 고정(구 위 투영이 단순)하여 ℓ2-box 문제로 특수화.
7. 보조변수 `y`(box), `z_j`(codeword polytope)를 도입해 ADMM 프레임에 얹고, augmented Lagrangian의 `x/y/z/λ1/λ2`-update를 각각 closed-form으로 유도(분산 처리 가능).
8. 정지조건은 `max_j‖P_j x-z_j‖_∞<ε`, `‖x-y‖_∞<ε` (learning 절차 없음, μ1,μ2만 대략 튜닝).
9. 결과: Margulis SNR 1.8~2.4dB에서 BP error-floor를 크게 하회, WiMAX SNR 4~4.4dB에서 MS error-floor 대비 개선. CPU time은 BP 0.027s vs ℓ2-box 0.018s(@2.0dB).
10. 한계: HW 미설계, gate/throughput 없이 CPU time만 제시, μ1,μ2 여전히 존재(insensitive라 주장), 저rate 통신용 부호로만 검증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| ℓ2-box ADMM 복호 이터레이션 | decoder.cpp `LDPC_Decoder()` | 복호 루프 자리는 같으나 Min-Sum→LP/ADMM 알고리즘 계열 전면 교체라 실질 대응 약함 |
| LLR 벡터 `γ` 입력 | channel.cpp `Set_LLR_Th()` | LLR 생성부는 재사용 가능하나 ADMM은 실수 LLR 그대로 사용 |
| codeword polytope 투영 `Π_PP_d` | 대응 없음 | Prime ECC(min-sum)에는 polytope 투영 개념 없음 |

적용 가치: **낮음** — LP/ADMM 복호는 HW min-sum 엔진과 계열이 다르고 반복당 연산·메모리 비용이 커 고rate NAND QC-LDPC 이식 부담이 크다.

### D. JSON 블록

```json
{
  "id": "arxiv:1711.10767v2",
  "title": "Parameter-free ℓp-Box Decoding of LDPC Codes",
  "year": 2018,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "2640",
  "soft_quant": "무관",
  "key_contribution": "LP 복호의 이진제약을 box∩ℓp-sphere로 대체한 parameter-free ℓ2-box ADMM 복호기",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "LP/ADMM 계열 복호로 HW 미설계·CPU time만 측정, Min-Sum 대비 반복당 연산 비용 큼",
  "todo_check": "고rate NAND QC-LDPC에서의 ℓ2-box ADMM 수렴속도·error-floor 이득 실측 필요"
}
```
