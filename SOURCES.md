# 참고 자료와 배포 범위

이 저장소의 한국어 스킬, 역할 카드, 템플릿, CSV 도구와 테스트는 이 패키지를 위해 작성했다. 아래 공개 자료의 작업 원칙을 참고했다. upstream 소스 파일, 실행 키트, 전체 플러그인, 안내 PDF나 시험 자료는 복사해 포함하지 않았다. 원본 스킬을 축약해 재배포한 공식 배포판도 아니다.

이 저장소 자체 작성물에는 루트 [MIT License](LICENSE)가 적용된다. 링크된 외부 자료에는 각 저장소·파일의 별도 라이선스가 적용되며, 이 저장소의 MIT 표시는 외부 자료를 재라이선스하지 않는다. 아래 버전은 2026-10-31 확인한 참조다.

[응시 규정 프로필](docs/exam-contract.md)은 사용자가 제공한 시험별 안내·운영 공지에서 확인한 행동 제약을 자체 지침으로 정리했다. 원본 PDF·메일·화면·개인 접속 정보·과제 내용은 배포하지 않는다. 프로필은 공식 규정을 대신하지 않으며 최신 시험별 안내와 해결되지 않은 충돌을 별도로 확인한다.

v0.3.1은 개인별 접속 안내 메일의 모델 권장값·업데이트 금지·준비 및 감독 조건·공개 자료 기준·장애 신고 절차를 반영했다. 메일과 기존 가이드 3종이 충돌하는 항목만 메일을 우선하며 나머지 제한은 유지한다. 당일 09:40 추가 공지의 내용까지 확인했다는 뜻은 아니다. 개인 접속 링크나 메일 원문을 공개 출처 링크로 싣지 않는다.

| 참고 자료 | 참고한 원칙 | 확인한 참조 | 이 패키지에서의 범위 |
|---|---|---|---|
| [Matt Pocock skills](https://github.com/mattpocock/skills) | 사실 확인과 사람의 판단 구분, 동작 경계 테스트 | [커밋](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa), MIT | 짧은 질문과 작은 검증 흐름. 원문의 무제한 인터뷰·외부 이슈 발행 없음 |
| [Superpowers](https://github.com/obra/superpowers) | 재현을 통한 디버깅, 새 검증 결과로 완료 판단 | [커밋](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b), MIT | task-flow·task-verify의 검증 기준. Visual Companion·자동 브라우저·PR 기능 없음 |
| [Oh My Codex](https://github.com/Yeachan-Heo/oh-my-codex) | 역할·담당 범위·검증 책임 분리 | [커밋](https://github.com/Yeachan-Heo/oh-my-codex/tree/a60b9435a8e6d894ba69d1540ecf20afaac63a7a), MIT | 읽기용 역할 카드. OMX 런타임·hooks·tmux·모델 설정 없음 |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 일관된 시각 규칙과 접근성 검토 | [커밋](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/28b3b8dee8c976df4fa3e94aed4e092ad43fcb03), MIT | 자체 작성 ui-review. 원본 디자인 데이터·검색기·CLI 없음 |
| [Anatomy](https://github.com/wheresryan22/anatomy) | 구조와 관계를 설명하는 SVG/HTML 도해 | [커밋](https://github.com/wheresryan22/anatomy/tree/1482e8469b0a9e0d8cc18ea2740a01423d29ae80), MIT | 자체 작성 system-diagram. 원본 도해 키트·에셋·Chrome 도구 없음 |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 로컬 자료의 범위를 정하고 데이터 품질 확인 | [고정 EDA 참조](https://github.com/K-Dense-AI/scientific-agent-skills/tree/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/exploratory-data-analysis), 저장소 MIT | 자체 작성 CSV 구조·결측 점검기. 원본 EDA 스크립트·과학 라이브러리·클라우드 연동 없음 |
| [CodexClaw](https://github.com/lidge-jun/codexclaw) | 작업 크기에 맞는 계획 검토, 조건부 동작 증거, 중단 후 재개 | [0.2.45 커밋](https://github.com/lidge-jun/codexclaw/tree/a7ff3b6b1e8221dc9be4f665f26b50270854b951), MIT 및 별도 구성 요소 고지 | 기존 task-flow·task-verify·검토 역할·근거 양식의 자체 작성 지침. [파일별 반영 근거](docs/codexclaw-review.md). 플러그인·hooks·원본 코드·개인 대화 검색 없음 |

저장소 이름이나 스타 수는 성능·규정 적합성·공식 보증의 근거가 아니다. 실제 사용 환경과 해당 과제 안내를 먼저 확인한다. 공개 자료를 추가로 복사하는 변경에서는 파일별 라이선스와 필요한 저작권 고지를 별도로 검토해야 한다.
