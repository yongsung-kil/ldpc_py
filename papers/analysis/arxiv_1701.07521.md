### arxiv:1701.07521v2 - Floor Scale Modulo Lifting for QC-LDPC codes (2017, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.89 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | scale 상수 하나만 저장해 mother matrix에서 다양한 circulant size의 QC-LDPC를 floor+scale로 생성, 4-cycle 수를 확률적으로 최소화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | length granularity(가변 circulant size)용 lifting 기법 - 고정 z=32 부호를 쓰는 Prime ECC엔 가변길이 요구가 없어 부적합 |
| 추가확인 | Prime ECC가 length-scalable QC-LDPC를 요구하는지, scale값 offline 탐색이 우리 부호에서 girth 이득을 주는지 |

> 총평: mother matrix에서 여러 길이의 QC-LDPC를 저장부담 없이 생성하며 short-cycle을 확률적으로 줄이는 lifting 이론/시뮬 논문 - 가변길이 부호구성이 목적이라 고정부호 Prime ECC엔 이식가치 낮음.

### B. 알고리즘 요약

1. 대상: circulant size `L`인 QC-LDPC의 exponent matrix `E(H)`에서 더 작은 circulant `Lk`의 부호를 생성하는 lifting, AWGN·BPSK/QPSK, BP/min-sum 디코딩.
2. 문제: 하나의 mother matrix로 여러 길이 부호를 만들 때 기존 floor/modulo lifting은 short cycle(특히 4-cycle)을 많이 남겨 성능 저하.
3. 모델: block-cycle은 exponent chain `{a1..a2l}`이 `sum (-1)^i a_i ≡ 0 mod L`이면 cycle 형성(Proposition 1).
4. 기존기법 비교: floor lifting `E_ij(Hk)=floor((Lk/L0)*E_ij)`, modulo lifting `E_ij(Hk)=E_ij mod Lk`. 4-cycle 생성 확률 각각 `p_fl=5/(4(2q-1))`, `p_mod=1/(2q-1)`.
5. 핵심 식: 제안 floor scale modulo lifting `E_ij(Hk)=floor((Lk/L0)*((r*E_ij) mod L0))`, `r`=scale value (2q와 서로소).
6. 핵심 아이디어: scale `r`을 여러 개(집합 `R`, |R|=φ(2q)/2) 써서 서로 다른 lifting 후보를 만들고 그중 4-cycle 최소인 것을 선택; Proposition 4로 두 scale이 동시에 cycle 만들 확률 0 보장.
7. 저장 트릭: 각 circulant size마다 부호를 저장하지 않고 mother matrix + scale 상수 `r` 하나만 저장(메모리 절감).
8. 최적화: scale `r`은 girth·최소길이 cycle 수 기준 offline 탐색(예: IEEE 802.16 rate1/2 12x24 mother matrix에 적용, Table II).
9. 결과: 이론적으로 `P_fsml(Nr)=1-O(q^{-Nr})`로 4-cycle 부재 확률 급증; AR4JA rate4/5(BP 100it)·rate8/9 산업표준 대비 SNR 시뮬로 fine granularity·catastrophic case 회피 확인.
10. 한계: 순수 lifting/부호구성 이론, HW·디코더 설계 없음, 4-cycle에 확률분석 집중, 결과는 시뮬만이고 gate/throughput 무관.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| floor scale modulo lifting으로 exponent matrix 생성 | ecc_top.cpp Load_PCM() | H-matrix/부호구조 생성 단계에 닿으나 Prime ECC는 z=32 고정 단일부호라 가변lifting 필요 없음 |
| scale 상수만 저장하는 부호표현 | 대응 없음 | Prime ECC는 부호 하나를 고정 로드, length-scalable 저장구조 없음 |
| BP/normalized offset min-sum 디코딩 가정 | decoder.cpp LDPC_Decoder() (성능 관측 대상) | 디코더 알고리즘 변경 아님, min-sum은 이미 보유 |
```

적용 가치: **낮음** - 여러 circulant size 부호를 저장부담 없이 생성하는 가변길이 lifting 기법으로, 단일 고정부호(z=32)를 쓰는 Prime ECC엔 요구가 없고 디코더/HW 이점이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1701.07521v2",
  "title": "Floor Scale Modulo Lifting for QC-LDPC codes",
  "year": 2017,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "0.5~0.89",
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "scale 상수 하나만 저장해 mother matrix에서 다양한 circulant size의 QC-LDPC를 floor+scale로 생성, 4-cycle 수를 확률적으로 최소화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "length granularity용 lifting 기법 - 고정 z=32 부호를 쓰는 Prime ECC엔 가변길이 요구가 없어 부적합",
  "todo_check": "Prime ECC가 length-scalable QC-LDPC를 요구하는지, scale값 offline 탐색이 우리 부호에서 girth 이득을 주는지"
}
```
