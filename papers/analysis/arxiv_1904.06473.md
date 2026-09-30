### arxiv:1904.06473v2 - Iterative Decoding of Trellis-Constrained Codes inspired by Amplitude Amplification (Preliminary Version) (2019, arXiv preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 미상 |
| 핵심기여 | 양자 amplitude amplification 착안, 최우도 codeword 상대우도를 반복 증폭하는 TCC 복호기 제안 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | 부분 |
| latency | 미상 |
| 추천도 | 하 |
| 한계,주의 | Preliminary Version - Experiments/Conclusions 섹션 TBD(빈칸), 결과·수렴증명·복잡도 전무 |
| 추가확인 | Turbo/일반 TCC trellis 구조 전제, LDPC 특수화 시 실제 성능·수렴여부 미검증 |

> 총평: 양자 진폭증폭 착안 TCC 복호 아이디어 초안(실험 TBD), 결과 부재로 NAND binary QC-LDPC 이식성 하.

### B. 알고리즘 요약

1. 대상은 Trellis-Constrained Code(TCC, Turbo+LDPC 상위집합), 두 저-trellis-복잡도 부호 `C1`,`C2`의 교집합부호 `C∩=C1∩C2`를 인터리버로 결합.
2. 풀려는 문제: BP는 일부 TCC류에서만 준최적, 일반 TCC에는 안정적 준최적 복호가 안됨.
3. 채널모델: 무기억 binary 채널 `P(r|s)=γ^{rs}` (BSC/BEC/AWGN 각 `γ` 부록 정의), LLR `L(r)`.
4. 핵심기법: ML 목표 `č=argmax γ^{rs^T}`를 `w1+w2=r`로 분해, 반복마다 `w1(i),w2(i)`를 갱신해 최우도 codeword 우도 `p(č)`의 상대우도를 증폭(Grover 진폭증폭 착안).
5. 핵심식: 짝수 iteration은 `w1←w1+Δ, w2←w2-Δ`(식1), 홀수 iteration은 `w1←ρw1, w2←ρw2`(식2), 조건 `p(č^{i+1})/Ξ^{i+1} ≥ p(č^i)/Ξ^i`(식3)로 상대우도 단조증가 보장.
6. 확장: `Δ`는 위치 j별 `δj_min=(logγ Ξ_-1 - logγ Ξ_+1)/4`(식5)로 누적우도 `Ξ`를 최소화, 실무는 전 심볼 δ를 스케일 `κ`로 한번에.
7. 구현 디테일: `ρ`는 닫힌형 없어 gradient로 최적화, `Ξ^{i+1}` 직접계산해 조건(3) 항상 보장.
8. 학습/최적화: 없음(순수 결정론적 우도 갱신, DE/NN 없음).
9. 결과: 없음 - IV. Experiments, V. Conclusions 모두 `TBD`(내용 없음), 수치·BER·수렴그래프 전무.
10. 한계: Preliminary Version, HW 미설계·실험 부재·수렴 정리 미완, trellis 표현 전제로 고전 QC-LDPC 직접 대응 불명.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| TCC 반복 우도증폭 복호 | decoder.cpp `LDPC_Decoder()` | 반복 message-passing 루프 위치는 대응하나 알고리즘(진폭증폭)은 이질적 |
| trellis 기반 `C1`/`C2` 교집합부호 | 대응 없음 | Prime ECC는 QC-LDPC PCM 단일, Turbo/trellis 구조 없음 |
| LLR `L(r)` / 채널 γ | channel.cpp `Set_LLR_Th()` | LLR 개념만 공유, 갱신방식 상이 |
| `Δ`/`ρ` 우도 갱신 스텝 | 대응 없음 | min-sum C2V/V2C 갱신과 무관한 진폭증폭식 갱신 |

적용 가치: **낮음** — trellis(Turbo) 구조 전제의 미완성 초안이며 실험·복잡도·HW가 전무해 NAND binary QC-LDPC 디코더 이식 근거 부족.

### D. JSON 블록

```json
{
  "id": "arxiv:1904.06473v2",
  "title": "Iterative Decoding of Trellis-Constrained Codes inspired by Amplitude Amplification (Preliminary Version)",
  "year": 2019,
  "venue": "arXiv preprint",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "미상",
  "code_length": "미상",
  "soft_quant": "미상",
  "key_contribution": "양자 amplitude amplification 착안, 최우도 codeword 상대우도를 반복 증폭하는 TCC 복호기 제안",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "부분",
  "latency": "미상",
  "recommend": "하",
  "caveat": "Preliminary Version - Experiments/Conclusions 섹션 TBD(빈칸), 결과·수렴증명·복잡도 전무",
  "todo_check": "Turbo/일반 TCC trellis 구조 전제, LDPC 특수화 시 실제 성능·수렴여부 미검증"
}
```
