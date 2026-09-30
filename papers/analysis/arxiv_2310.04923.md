### arxiv:2310.04923v2 - An Optimal Unequal Error Protection LDPC Coded Recording System (2023, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | irregular |
| 부호rate | 0.65~0.82 |
| 부호length | 4161~11520 |
| 연판정 | soft-4bit+ |
| 핵심기여 | RLL flipping 오류를 강한 정정 세그먼트에 몰아넣는 interleaver+신호labeling과 UEP irregular LDPC 노드분포 최적화(DE/EXIT/differential evolution)로 error-floor 제거 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 4-level PAM 광/자기광 기록(DVD)+PR채널+RLL flipping 특화 - NAND binary AWGN/RBER 채널과 문제설정이 달라 이식 불가 |
| 추가확인 | 권장부호 VND=[2,5]/CND=[10]의 degree-2 VN 비중과 short-cycle/trapping-set이 NAND 고rate에서 재현되는지 |

> 총평: 광기록 RLL flipping용 UEP 부호설계로 error-floor 제거가 핵심이나 채널·변조·응용이 NAND와 상이해 이식성 하.

### B. 알고리즘 요약

1. 시스템: 4-level RLL(0,3) 제약 광/자기광(DVD-ROM) 기록, PR채널 `h=(1,2,2,1)`+AWGN+jitter noise(`M0=βN0, β=0.15`), PEG-irregular LDPC(rate 0.65/0.75/0.8, length 4608·11520).
2. 문제: RLL 제약 위반 비트를 write측에서 deliberate flipping하면 read측 LDPC가 그 flipping 오류를 정정해야 하는데, 고rate에서 flipping 오류가 많아지면 성능 급락·error-floor 발생.
3. 모델: `y = v⊕q`로 RLL 위반 비트 flip, PLM precoder+4-level PAM(natural mapping) 후 PR채널; read측은 BCJR MAP equalizer(43-state)+LDPC의 turbo equalization(inner `Ui`/outer `Uo`).
4. 핵심 기법1(UEP 부호): irregular LDPC의 VND를 강한부분(VND 4~7)/약한부분(VND 2,3)으로 나눠 unequal error protection, 강한 세그먼트에 flipping 오류를 배치.
5. 핵심 식: `d1δ1^2 ≥ ... ≥ dM δM^2` (Euclidean separation 부등식) - UEP 성립조건, nearest-neighbor(NN) 수를 줄여 error coefficient(`2^d·Ad`→`2^-d·Ad`) 대폭 감소.
6. 핵심 기법2(할당): regular interleaver type I(short-distance flip)/type II(long-distance flip, NN 적은 labeling에 강한부호 배치)로 flipping 오류를 코드 세그먼트에 국한; type II가 최적.
7. 구현 디테일: soft-info 조정(erasing / |LLR| 평균 magnitude / |LLR| 평균 clipping), RLL+parity check 병행 검출로 flipped-bit 검출 확률↑, non-reset decoder 사용.
8. 최적화: sum-product DE의 `tanh`(Γ) 계산난이로 min-sum 기반 DE로 대체, flipping이 random codeword 의존이라 all-zero 가정 불가→Monte Carlo DE; EXIT chart로 수렴 확인; differential evolution(α=0.5, L=50)으로 노드분포 전역최적화.
9. 결과: type II·`Uo=5,Ui=3`에서 flipped 시스템이 non-flipped 대비 0.1dB 이내, error-floor 제거; 권장부호 VND=[2,5] λ=[0.5,0.5], CND=[10] γ=[0.9707,0.0293](rate 0.65).
10. 한계: BER/DE/EXIT 시뮬만(HW 미설계), 4-level 광기록·PR·RLL flipping이라는 특수 응용, throughput/complexity 수치 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| irregular UEP 노드분포 설계 | ecc_top.cpp `Load_PCM()` | Prime ECC는 고정 QC-LDPC H-matrix라 UEP degree distribution 도입은 부호 재설계·재검증 부담 큼 |
| min-sum 기반 DE 성능평가 | 대응 없음 | 부호평가용 해석도구일 뿐 디코더 코드에 직접 대응 없음 |
| flipped-bit soft-info 조정(LLR 클리핑/평균) | decoder.cpp `Get_VNU_Table_Idx()`, ecc_data.h `PARAM_LLR` | LLR 조정 개념은 유사하나 RLL flipping 검출 전제라 NAND엔 부적합 |
| MAP equalizer/turbo equalization | 대응 없음 | Prime ECC는 채널 equalizer 없음(RBER/AWGN 직접 주입) |
| PR채널/jitter noise | channel.cpp `Set_R_Offset()` | 채널모델 구조만 유사, PR/ISI/jitter는 NAND 채널과 상이 |

적용 가치: **낮음** - UEP 부호설계·error-floor 제거 관점은 흥미로우나 4-level 광기록 RLL flipping이라는 응용 특화로 NAND binary QC-LDPC에 떼어 쓸 요소가 사실상 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2310.04923v2",
  "title": "An Optimal Unequal Error Protection LDPC Coded Recording System",
  "year": 2023,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "irregular",
  "code_rate": "0.65~0.82",
  "code_length": "4161~11520",
  "soft_quant": "soft-4bit+",
  "key_contribution": "RLL flipping 오류를 강한 정정 세그먼트에 몰아넣는 interleaver+신호labeling과 UEP irregular LDPC 노드분포 최적화(DE/EXIT/differential evolution)로 error-floor 제거",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "4-level PAM 광/자기광 기록(DVD)+PR채널+RLL flipping 특화 - NAND binary AWGN/RBER 채널과 문제설정이 달라 이식 불가",
  "todo_check": "권장부호 VND=[2,5]/CND=[10]의 degree-2 VN 비중과 short-cycle/trapping-set이 NAND 고rate에서 재현되는지"
}
```
