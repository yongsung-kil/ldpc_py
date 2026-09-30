### arxiv:2409.01440v2 - An almost-linear time decoding algorithm for quantum LDPC codes under circuit-level noise (2025, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | BP+OTF post-processing(Kruskal 스패닝포레스트)로 행렬역변환 없이 almost-linear time QLDPC 복호 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 양자 CSS QLDPC(bivariate bicycle/surface) 전용, detector error model 기반이라 NAND binary LDPC와 문제구조 상이 |
| 추가확인 | OTF의 Kruskal 스패닝트리 아이디어가 고전 binary LDPC trapping-set 완화에 전용 가능한지(순수 이론적 관심만) |

> 총평: 양자 QLDPC 실시간 복호기로 NAND 고전 binary LDPC와 도메인이 달라 직접 이식가치 없음(이식성 하).

### B. 알고리즘 요약

1. 대상은 양자 CSS/QLDPC 부호(bivariate bicycle `[[72,12,6]]~[[288,12,18]]`, rotated surface `d=5~17`)를 circuit-level noise 하에서 복호하는 문제.
2. 기존 BP+OSD/MWPM은 정확하나 후처리 행렬역변환이 `O(n^3)`이라 실시간(1µs) 복호에 부담.
3. 채널은 depolarising circuit-level noise, 복호는 syndrome/detector가 아닌 detector error model(DEM) `Hdem·e=sD` 기반.
4. 핵심기법 OTF: BP 실패 시 soft-info로 열을 신뢰도순 정렬 후 수정된 Kruskal 알고리즘으로 loop-free ordered Tanner forest `Hotf` 생성, 그 위에서 BP 재실행(트리이므로 수렴 보장).
5. 핵심식 `|V~P ∩ VP|>1`이면 loop 발생 → 평균 열무게 `j̄`가 낮을수록 유효 `Hotf` 확보 확률 상승.
6. 확장 DEM sparsification: transfer matrix `Atr`로 `Hsdem·Atr=Hdem`, 열무게 `≤γ`로 축소(열수 약 30%).
7. soft-info 전달은 Piling-up lemma 기반 XOR 확률식 `p(esdem)=1/2(1-∏(1-2p(edem)))`로 sparsified 그래프에 매핑.
8. 최종 3단 파이프라인 BP+BP+OTF: full DEM BP → sparsified BP → OTF, 첫 성공 시 종료.
9. 결과: BP+OSD-0/MWPM과 동등한 logical error 억제, bivariate bicycle에서 10배 이상 속도, `d=17` surface를 107 BP iteration으로 복호, almost-linear `O(n log n)`.
10. 한계: HW 미설계(FPGA/ASIC은 향후), 현 구현은 serial(실측 quadratic), 양자 전용이라 고전 NAND LDPC와 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP(min-sum) 복호 루프 | decoder.cpp `LDPC_Decoder()` | 표면적 유사(min-sum)하나 양자 DEM 복호라 직접 대응 아님 |
| OTF Kruskal 스패닝포레스트 post-processing | 대응 없음 | Prime ECC엔 트리화 post-processor 개념 없음 |
| DEM sparsification / transfer matrix | 대응 없음 | 양자 circuit-level noise 전용 개념 |
| soft-info XOR 매핑(Piling-up) | 대응 없음 | 양자 detector 확률 전달용 |

적용 가치: 낮음 — 양자 QLDPC/CSS 부호와 circuit-level detector error model 전용 기법으로, NAND용 고전 binary QC-LDPC의 부호설계/디코더/HW 어디에도 떼어 쓸 대응이 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2409.01440v2",
  "title": "An almost-linear time decoding algorithm for quantum LDPC codes under circuit-level noise",
  "year": 2025,
  "venue": "arXiv (quant-ph)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "BP+OTF post-processing(Kruskal 스패닝포레스트)로 행렬역변환 없이 almost-linear time QLDPC 복호",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "하",
  "caveat": "양자 CSS QLDPC(bivariate bicycle/surface) 전용, detector error model 기반이라 NAND binary LDPC와 문제구조 상이",
  "todo_check": "OTF의 Kruskal 스패닝트리 아이디어가 고전 binary LDPC trapping-set 완화에 전용 가능한지(순수 이론적 관심만)"
}
```
