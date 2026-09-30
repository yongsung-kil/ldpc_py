### arxiv:2507.03461v1 - Learning Variable Node Selection for Improved Multi-Round Belief Propagation Decoding (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 96 |
| 연판정 | soft-4bit+ |
| 핵심기여 | SBND 착안 stacked-GRU로 MRBP 교란 대상 VN 예측, expert rule 대비 적은 라운드로 near-MLD |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | GRU 20.6M 파라미터로 HW 비현실적, short LDPC(96,48) 한정, NAND 무관 |
| 추가확인 | high-rate NAND QC-LDPC로 확장 시 라벨 생성 비용·GRU 축소 가능성 |

> 총평: 학습 기반 MRBP VN 선택으로 near-MLD에 근접하나 파라미터 과다·short code 한정이라 NAND binary QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 대상은 short (96,48) irregular QC-LDPC (rate 0.5), BI-AWGN/BPSK 채널, 채널 LLR `Lch = 2y/σ²`.
2. 문제: short blocklength에서 BP가 MLD 대비 열세이며, 소수 문제성 VN 때문에 수렴 실패.
3. MRBP는 문제성 VN을 골라 채널 LLR을 flip+포화(`Lch,t = -∞·sign`)한 뒤 재복호(`l1≤l0` iter)하여 후보 codeword 리스트 `L`에서 `argmin ||y-(-1)^c||` 선택.
4. 핵심 착안: 교란할 VN 집합이 채널 오류 패턴의 부분집합이므로, syndrome-based neural decoder(SBND)로 오류를 추정하는 문제와 연결.
5. 기존 [15]의 얕은 MLP를 stacked GRU로 교체 (5-layer, hidden `6(2n-k)`, 5 time step).
6. 입력을 채널 LLR 대신 충분통계 `(|Lch|, sch)` 쌍으로 변경 → all-zero codeword 시뮬만으로 학습 데이터 생성 가능.
7. 학습을 이진분류로 정식화하여 BCE loss (6) 사용, 라벨 `bi=1`은 VN i 교란 시 재복호 성공.
8. 학습: PyTorch, 60M BP 실패 예제(3dB, `l0=l1=20`), Adam lr `10⁻⁴`, 250 epoch, Reduce-on-Plateau.
9. 결과: GRU-D2가 nSMEA expert rule을 T=1부터 능가, [9]를 절반 perturbation으로 매칭, 39M SBND 대비 절반 파라미터로 우수, BP 100iter도 초과.
10. 한계: 20.6M 파라미터로 HW 비현실적, (96,48) 단일 코드만 검증, DNN 추론 복잡도 매우 큼.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MRBP BP 이터레이션 재복호 | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 재복호 루프 자체는 대응하나 min-sum 기반이라 BP/LLR 스케줄 상이 |
| 채널 LLR flip+포화 교란 | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | soft-read LLR 조작 지점과 개념적 대응 |
| 조기종료(리스트 후보 선택) | full_CRC.cpp, partial_CRC.cpp | 성공 판정에는 대응하나 ML-list 선택은 미보유 |
| GRU 신경망 VN 선택기 | 대응 없음 | NN 디코더는 Prime ECC 미지원 |

적용 가치: **낮음** — 학습형 MRBP는 20.6M NN이 필요해 NAND HW 디코더에 이식 불가하고, min-sum 기반 Prime ECC와 알고리즘 정합성도 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:2507.03461v1",
  "title": "Learning Variable Node Selection for Improved Multi-Round Belief Propagation Decoding",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "96",
  "soft_quant": "soft-4bit+",
  "key_contribution": "SBND 착안 stacked-GRU로 MRBP 교란 대상 VN 예측, expert rule 대비 적은 라운드로 near-MLD",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "GRU 20.6M 파라미터로 HW 비현실적, short LDPC(96,48) 한정, NAND 무관",
  "todo_check": "high-rate NAND QC-LDPC로 확장 시 라벨 생성 비용·GRU 축소 가능성"
}
```
