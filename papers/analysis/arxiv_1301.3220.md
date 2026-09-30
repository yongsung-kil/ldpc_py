### arxiv:1301.3220v1 - A Low-Complexity Encoding of Quasi-Cyclic Codes Based on Galois Fourier Transform (2013, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | encoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.53~0.87 |
| 부호length | 4095~8176 |
| 연판정 | 무관 |
| 핵심기여 | Galois Fourier transform 기반 변환영역 인코딩으로 QC 코드 인코딩 복잡도를 O(e²(n-k)k)에서 O(e(n-k)k) (또는 binary는 O(e(n-k)k log2 e))로 감소 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 결과 코드워드가 non-systematic이라 복호 후 별도 Fourier transform으로 메시지 복원 필요, HW 미검증(이론뿐) |
| 추가확인 | Prime ECC는 dual-diagonal 고정 인코더 구조라 본 변환영역 인코딩 이식 시 재검증 부담이 큰지 확인 필요 |

> 총평: QC 코드 일반 인코딩 복잡도 감소를 위한 대수적(Galois Fourier transform) 이론 기법으로, NAND용 Prime ECC의 고정된 dual-diagonal 인코더 구조와는 이질적이며 이식 우선순위 낮음.

### B. 알고리즘 요약

1. 대상은 일반 (en,ek) QC 코드(및 QC-LDPC 서브클래스), circulant 크기 `e`, 코드 rate 예시로 (4095,2160) 64진/이진, (8176,7154) 이진 등 다양한 rate/length 사용.
2. 전통적 QC 인코딩은 `G·m` 곱셈 기반으로 계산복잡도가 `O(e²(n-k)k)`로 크고, 부분 병렬화해도 symbol 연산 수가 여전히 크다는 문제.
3. 채널/노이즈 모델은 다루지 않음(순수 인코딩 알고리즘, 복호기와 독립).
4. 핵심 기법은 Galois Fourier transform(GFFT)으로 생성행렬 `G`를 변환영역 `GF,π`(대각행렬 블록)로 바꾼 뒤 그 영역에서 메시지 `m`을 인코딩(ETD, Encoding in Transform Domain).
5. 핵심 식 `cF,π = m · GF,π` 후 역 Fourier transform으로 최종 코드워드 `c` 복원; 변환영역에서는 `k×n` 행렬 `e`번 연산으로 축소되어 계산량이 `O(e(n-k)k)`로 감소.
6. 이진 QC 코드 확장: 변환된 코드워드가 이진이 되도록 서브필드 basis(`β_i,l`) 기반 메시지 사전처리 매핑을 도입해 conjugacy constraint(`d_(2t)e = d_t²`) 만족시킴.
7. 이 conjugacy constraint를 활용하면 이진 경우 복잡도가 `O(e(n-k)k log2 e)`로 추가 감소(대표 conjugacy class만 저장/계산).
8. 별도 학습/최적화 절차 없음(닫힌형 대수적 유도, Gaussian elimination으로 systematic 변환 정도만 사용).
9. 결과: (4095,2160) 64진 코드는 전통 대비 1.59%, (4095,2160) 이진은 9.52%, (8176,7154) 이진은 1.77% 계산량. 메모리 소비는 전통 인코딩과 동일(O(e(n-k)k) 심볼).
10. 한계: 순수 이론/복잡도 분석뿐(시뮬레이션·HW 없음), 결과 코드워드가 non-systematic이라 디코딩 후 메시지 복원에 추가 Fourier transform 필요, rank-deficient parity-check 행렬 케이스도 다루나 실제 HW 친화성은 미검증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Fourier transform 기반 인코딩 (ETD) | `encoder.cpp` `LDPC_encoder_4KB()`, `Generate_PCM_encoding()` | Prime ECC는 dual-diagonal 고정 구조로 완전히 다른 인코딩 방식이라 대체 시 재설계 필요 |
| 부호 PCM/rank-deficient 처리 | `ecc_top.cpp` `Load_PCM()` | H-matrix rank 분석 관련성은 있으나 코드 구조 자체를 바꾸는 수준의 변경 요구 |
| 이진 conjugacy constraint 매핑 | 대응 없음 | Prime ECC엔 대응하는 변환영역 표현 없음 |

적용 가치: **낮음** — 순수 이론적 대수 인코딩 기법으로 Prime ECC의 고정 dual-diagonal 인코더와 구조적으로 이질적이며, non-systematic 코드워드 특성상 실제 채택 시 부호화/복호화 파이프라인 전반의 재설계가 필요함.

### D. JSON 블록

```json
{
  "id": "arxiv:1301.3220v1",
  "title": "A Low-Complexity Encoding of Quasi-Cyclic Codes Based on Galois Fourier Transform",
  "year": 2013,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "encoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.53~0.87",
  "code_length": "4095~8176",
  "soft_quant": "무관",
  "key_contribution": "Galois Fourier transform 기반 변환영역 인코딩으로 QC 코드 인코딩 복잡도를 O(e^2(n-k)k)에서 O(e(n-k)k) 또는 이진 O(e(n-k)k log2 e)로 감소",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "결과 코드워드가 non-systematic이라 복호 후 별도 Fourier transform으로 메시지 복원 필요, HW 미검증(이론뿐)",
  "todo_check": "Prime ECC는 dual-diagonal 고정 인코더 구조라 본 변환영역 인코딩 이식 시 재검증 부담이 큰지 확인 필요"
}
```
