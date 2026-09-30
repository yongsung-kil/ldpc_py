### arxiv:2305.00137v6 - Spatially-Coupled QLDPC Codes (2025, Quantum)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.2759~0.3425 |
| 부호length | 5800~7300 |
| 연판정 | 무관 |
| 핵심기여 | 2D-SC 특성함수(다변수 다항식)로 stabilizer 조건·단주기 열거를 대수화하고 GRADE-AO로 SC-HGP QLDPC 부호의 short cycle을 최소화 |
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
| 한계,주의 | 양자 stabilizer/CSS 부호(Pauli, depolarization 채널, BP-OSD) 대상이라 binary NAND LDPC와 대상 자체가 다름 |
| 추가확인 | 인용 [38] 고전 SC-LDPC의 GRADE-AO cycle 최적화 원논문이 NAND용 고rate QC-LDPC 부호설계에 더 직접적 |

> 총평: 양자 SC-QLDPC 부호설계·단주기 최적화 논문으로, 대수적 cycle 열거 아이디어는 흥미로우나 대상이 quantum 부호라 Prime ECC(binary QC-LDPC) 이식성은 하.

### B. 알고리즘 요약

1. 대상: 토릭 부호를 고전 2D-SC 부호의 양자 대응물로 보고, 이를 일반화한 spatially-coupled QLDPC(SC-QLDPC) 부호 구성 (CSS/stabilizer 부호).
2. 문제: 기존 QLDPC 연구는 최소거리 스케일링·저rate(<1/10)에 집중, 유한길이 성능(단주기 제거)과 고rate 부호는 소홀.
3. 모델: 2D-SC 부호의 PCM을 두 부정원 `F(U,V)=Σ H_ij U^i V^j` 특성함수(계수는 Pauli 행렬)로 표현.
4. 핵심 1단: stabilizer(commute) 필요충분조건을 대수식 `⟨F(U,V), F(U⁻¹,V⁻¹)⟩_s = 0`으로 도출(Thm 2).
5. 의미: 이 단일 대수조건이 성분행렬 A,B,C,D의 다수 symplectic 직교조건을 대체 → 새 부호족(HGP/XYZ) 체계적 구성.
6. 핵심 2단: SC-HGP 부호를 quasi-abelian lifted product 부호와 동일시하고, 파티션 행렬 `Pa,Pb`의 alternating-sum 조건(Lemma 1)으로 Tanner graph cycle-4/6/8을 열거.
7. 트릭: cycle을 base 행렬만으로 결정되는 rigid cycle과 `Pa,Pb` 의존 flexible cycle로 분리 → rigid cycle limit이 성능 하한.
8. 최적화: GRADE(확률분포 gradient descent)로 초기 edge 분포 최적화 후 AO(greedy) 단계로 flexible cycle 실제 제거.
9. 결과: depolarization 채널 BP-OSD(+BP-SSF) 시뮬에서 rate 0.3425 부호 threshold ~7.0%, rate 0.2759 부호 ~8.7%; cycle 최소화로 LER 개선, 동일길이 HGP 부호 대비 우수.
10. 한계: HW 미설계, 양자 stabilizer 부호 전용(Pauli likelihood BP-OSD), 고전 binary NAND LDPC와 대상 상이.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-HGP QLDPC 부호구성/특성함수 | 대응 없음 (양자 stabilizer 부호, non-binary Pauli) | Prime ECC는 binary QC-LDPC, 대상 상이 |
| alternating-sum 기반 cycle 열거·GRADE-AO 최적화 | ecc_top.cpp Load_PCM() (H-matrix 로드) | 고전 QC-LDPC 부호설계 아이디어는 개념적으로만 연결, 그대로 이식 불가 |
| BP-OSD / BP-SSF 양자 디코더 | 대응 없음 (Pauli likelihood, degenerate error) | Prime ECC는 binary min-sum, 무관 |
| windowed / low-latency 디코딩 언급 | 대응 없음 | 개념 언급뿐, 구현 없음 |
```

적용 가치: **낮음** — 양자 SC-QLDPC 부호설계·양자 디코더 논문으로, NAND binary QC-LDPC(Prime ECC 3.1)에 떼어 쓸 요소가 거의 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2305.00137v6",
  "title": "Spatially-Coupled QLDPC Codes",
  "year": 2025,
  "venue": "Quantum",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "5800~7300",
  "soft_quant": "무관",
  "key_contribution": "2D-SC 특성함수(다변수 다항식)로 stabilizer 조건·단주기 열거를 대수화하고 GRADE-AO로 SC-HGP QLDPC 부호의 short cycle을 최소화",
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
  "caveat": "양자 stabilizer/CSS 부호(Pauli, depolarization 채널, BP-OSD) 대상이라 binary NAND LDPC와 대상 자체가 다름",
  "todo_check": "인용 [38] 고전 SC-LDPC의 GRADE-AO cycle 최적화 원논문이 NAND용 고rate QC-LDPC 부호설계에 더 직접적"
}
```
