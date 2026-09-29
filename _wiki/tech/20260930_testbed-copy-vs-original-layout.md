---
summary: 시험장 사본(ldpc_py)과 원본 배치(2_LDPC_base)의 차이. 런처 탐색과 디코더 주입 사슬, -m 경로의 BaseDecoder 고정, .gitignore와 형제 프로젝트 부재, 온보딩 코드 무수정
tags: [testbed, launcher, layout]
sources: [workspace/_template/run.py:9-33, workspace/README.md:1-13, src/run.py:11-15, src/run.py:277, src/run.py:393-396, src/run.py:443-445, src/run.py:780-795, docs/profile/structure.md:20, docs/profile/structure.md:97, docs/explore/프로젝트전체.md:37-41, docs/explore/프로젝트전체.md:154-159]
last_verified: 2026-09-30
---

## 무엇을 하는가

- ㉮ 이 저장소는 원본 `2_LDPC_base/`의 시험장 사본이고 폴더 이름이 `ldpc_py`다. 코드는 같지만 배치가 달라 실험 폴더 런처가 동작하지 않는다
- ㉯ 이 사본에서 동작하는 실행 경로는 저장소 루트의 `python -m src.run <config>` 하나이고 디코더는 BaseDecoder 고정이다

## 어떻게 도는가

- ㉮ 원본 배치의 런처 (`workspace/_template/run.py`, 실험 폴더 5개 동일 33줄)
  - ㉠ 자기 폴더에서 부모로 올라가며 `{조상}/2_LDPC_base/src` 폴더가 있는지 본다 (`:11-12`)
  - ㉡ 파일시스템 루트까지 못 찾으면 `SystemExit` (`:13-17`)
  - ㉢ 찾으면 `{조상}/2_LDPC_base`를 `sys.path[0]`에 넣고 `from src.run import main` (`:18-22`)
  - ㉣ `DECODER_CLASS` 한 곳이 디코더를 고른다. None이면 BaseDecoder, 변형은 같은 폴더 `decoder.py`의 자식 클래스를 import해 지정 (`:24-28`)
  - ㉤ 인자 config마다 `main([config_path], decoder_class=DECODER_CLASS)`. 인자가 없으면 형제 `config.json` (`:30-33`)
- ㉯ 본체 쪽 주입 사슬: `main(argv, decoder_class=None)` (`src/run.py:780`) → `setup(config, decoder_class)` (`:786`, `:393-396`) → `decoder_class(code, llr_matrix=llr_matrix)` (`:443-445`). config에 디코더 키가 없고 실험 요약에 클래스 이름이 찍힌다
- ㉰ 이 사본에서의 차이
  - ㉠ 조상에 `2_LDPC_base/src`가 없어 런처가 `SystemExit`로 끝난다 (2026-09-30 실행 확인)
  - ㉡ `python -m src.run`은 `__main__`이 `main()`을 인자 없이 부르므로 `decoder_class`가 None이다. 자식 디코더를 넣을 자리가 없다 (`src/run.py:794-795`)
  - ㉢ config의 상대 경로(`../../Input/...`)는 config 파일 위치 기준이라 `-m` 경로에서도 그대로 맞는다 (`src/run.py:277`)
  - ㉣ `.gitignore`가 없다. `workspace/README.md:12`의 "git 무시"가 성립하지 않고, 탐침 결과물이 커밋에 들어 있으며, 실행하면 `src/__pycache__/`가 untracked로 남는다
  - ㉤ 형제 프로젝트(`3_LDPC_ideas/`, `4_H_matrix_tool`, C++ 원본)가 없다. 코드 import는 0건이라 실행에는 영향이 없고 문서 링크만 끊긴다 (`workspace/README.md:4-5`, `docs/profile/structure.md:97`)
  - ㉥ 이력 문서의 `workspace/vanilla/`는 이 사본의 `workspace/base_run/`이다. `workspace/minsum_dual_clip/`과 `workspace/실험로그.md`는 없다. 이력물의 원본 커밋 해시는 이 사본 git 이력에 없다
- ㉱ 온보딩(2026-09-30) 원칙: `src/`와 `workspace/` 무수정. Decision 등급은 판정요청 문서로만 남긴다. 실행 확인은 스크래치 출력만 쓰고 `Sim_Output`을 남기지 않는다

## 쓰는 법

- ㉮ 기준선 실행: 저장소 루트에서 `python -m src.run workspace/test/config.json`
- ㉯ 변형 디코더 실험은 원본 배치(`LDPC_dev/2_LDPC_base/`)에서 런처로 돌린다. 이 사본에서 돌리려면 판정요청 물음 1의 답이 필요하다. 권고는 런처 탐색 조건에 "이 저장소의 `src/run.py`가 있는 조상"도 허용하는 한 줄 추가
- ㉰ 런처를 고칠 때 탐색 조건이 폴더 이름에 묶여 있음을 기억한다. 이름이 바뀌면 런처 5개를 전부 고쳐야 한다
- ㉱ 실행 뒤 `src/__pycache__/`를 지운다 (`.gitignore`가 없으므로)

## 관련 문서

- ㉮ [판정요청: 이 사본의 변형 디코더 실행 경로](../decisions/20260930_variant-decoder-run-path.md)
- ㉯ [결정: 디코더 선택은 DECODER_CLASS 한 곳](../decisions/20260810_decoder-class-single-switch-registry-removed.md)
- ㉰ [run.py main 흐름](20260930_run-main-flow.md)
- ㉱ [교체 지점 6개](20260930_replacement-points-six.md)
- ㉲ [패턴: 논문 아이디어를 교체 지점 하나로 붙이는 절차](../assets/20260813_paper-idea-single-override-procedure.md)
- ㉳ 프로파일 [structure](../../docs/profile/structure.md), [replacement_points](../../docs/profile/replacement_points.md)
