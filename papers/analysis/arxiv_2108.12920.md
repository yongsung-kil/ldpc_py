### arxiv:2108.12920v1 - KO codes: Inventing Nonlinear Encoding and Decoding for Reliable Wireless Communication via Deep-learning (2021, ICML/PMLR 139)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호length | 64~512 |
| 부호rate | 미상 |
| 연판정 | 무관 |
| 핵심기여 | RM/Polar의 Plotkin(Kronecker) 트리를 골격으로 encoder/decoder를 NN으로 비선형 일반화해 end-to-end 학습, SC 복호 하에서 RM/Polar 능가 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | NN 기반 비선형 non-LDPC 부호(RM/Polar 계열)로 학습된 부호·복호가 통짜라 binary QC-LDPC로 이식 불가, AWGN 시뮬만 |
| 추가확인 | Plotkin 트리 골격을 NN으로 일반화한다는 발상이 LDPC message-passing 스케줄에 유추 적용 가능한지(직접 이식은 아님) |

> 총평: RM/Polar를 NN으로 비선형 일반화한 딥러닝 부호설계 논문. LDPC와 무관하고 부호·복호가 학습된 non-binary 실수 매핑이라 NAND binary QC-LDPC ECC 이식 가치 없음.

### B. 알고리즘 요약

1. 시스템: AWGN 채널 물리계층, short-to-medium block length(`n=64`~`512`) regime. RM/Polar를 대체할 새 부호쌍 학습이 목표.
2. 문제: RM/Polar는 minimum pairwise distance 최적화라 short block에서 average-case 신뢰도(BER/BLER)엔 보수적 → 개선 여지.
3. 모델: encoder `gθ:{0,1}^k→R^n`, decoder `fφ`를 NN으로 파라미터화, cross-entropy surrogate로 BER 최소화 학습.
4. 핵심 기법: RM/Polar의 Kronecker(Plotkin) 재귀구조를 computation tree(Plotkin tree)로 보고, 내부노드의 선형 Plotkin 매핑 `(u,u⊕v)`를 좌표별 비선형 NN `gi(u,v)∈R²`로 교체.
5. 핵심 식: 복호는 Dumer 재귀복호(=Polar SC)를 일반화 — `f2i-1`이 `LSE` 대체, `f2i`가 parity-adjusted LLR 덧셈 `⊕v̂` 대체. leaf는 미분가능 Soft-MAP.
6. 확장: Polar(64,7)에도 동일 적용, KO 복호가 MAP에 근접(0.5~0.7dB gain). channel-agnostic — `y`에서 직접 채널통계 학습.
7. 구현 디테일: 각 NN 블록 3층×32노드; TinyKO는 1층×4노드(20 param, 110배 압축)로 GPU 병렬 시 Dumer SC와 동일 latency.
8. 최적화: SGD end-to-end, encoder/decoder 동시 학습, AWGN 샘플 무제한 생성.
9. 결과: KO(9,2)/KO(8,2)가 RM 대비 BER·BLER 동시 개선, 학습된 codeword pairwise-distance가 Gaussian codebook에 근사. non-AWGN(Rayleigh/bursty)에도 robust.
10. 한계: HW 미설계, AWGN 시뮬만, 부호·복호가 통짜 학습된 non-binary 실수 비선형 부호라 binary LDPC/NAND ECC와 근본적으로 별개 계열.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| NN 기반 KO encoder/decoder | 대응 없음 | 프로파일 §6 명시 "NN/딥러닝 디코더"는 대응 없음 |
| RM/Polar Plotkin(Kronecker) 부호구성 | 대응 없음 | non-LDPC 알고리즘 계열, QC-LDPC 구조와 무관 |
| Dumer/SC 재귀복호 일반화 | 대응 없음 | Prime는 min-sum message-passing, SC/재귀복호 아님 |
| Soft-MAP / LSE 미분가능 복호 | 대응 없음 | 학습용 미분가능 복호, bit-exact min-sum 코어와 무관 |

적용 가치: **낮음** — 딥러닝으로 학습한 비선형 RM/Polar 계열 부호·복호로, 프로파일이 "대응 없음"으로 못박은 NN 디코더·non-binary·turbo/polar 범주에 해당한다. binary QC-LDPC의 부호설계→디코더→HW 어느 레이어에도 떼어 쓸 수 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2108.12920v1",
  "title": "KO codes: Inventing Nonlinear Encoding and Decoding for Reliable Wireless Communication via Deep-learning",
  "year": 2021,
  "venue": "ICML/PMLR 139",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "64~512",
  "soft_quant": "무관",
  "key_contribution": "RM/Polar의 Plotkin(Kronecker) 트리를 골격으로 encoder/decoder를 NN으로 비선형 일반화해 end-to-end 학습, SC 복호 하에서 RM/Polar 능가",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "동등",
  "recommend": "하",
  "caveat": "NN 기반 비선형 non-LDPC 부호(RM/Polar 계열)로 학습된 부호·복호가 통짜라 binary QC-LDPC로 이식 불가, AWGN 시뮬만",
  "todo_check": "Plotkin 트리 골격을 NN으로 일반화한다는 발상이 LDPC message-passing 스케줄에 유추 적용 가능한지(직접 이식은 아님)"
}
```
