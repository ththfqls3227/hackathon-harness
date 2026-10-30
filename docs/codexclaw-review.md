# CodexClaw 검토와 반영

2026-10-31에 확인한 대상은 [lidge-jun/codexclaw](https://github.com/lidge-jun/codexclaw)다. 같은 이름의 Telegram 원격 제어 프로젝트와 구분한다. 확인 버전은 0.2.45, 참조 커밋은 `a7ff3b6b1e8221dc9be4f665f26b50270854b951`이다.

원본의 작업 원칙을 검토하고 아래 내용을 한국어 지침으로 직접 작성했다. CodexClaw 설치·실행·호환성 검증이나 원본 기능 전체의 이식을 뜻하지 않는다.

| 확인한 원칙과 원문 | 이 하네스에 반영한 부분 |
|---|---|
| [PABCD와 작업 크기에 따른 절차](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/plugins/codexclaw/skills/pabcd/SKILL.md) | [task-flow](../.agents/skills/task-flow/SKILL.md)에 계획·사전 검토·구현·검증·정리 연결. 작은 수정은 직접 실행하고 단계별 승인·별도 문서를 강제하지 않음 |
| [실제 변경 경로와 검증 대상을 확인하는 계획](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/plugins/codexclaw/skills/pabcd/references/phase-plan.md), [구조 지도와 정확한 검색의 구분](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/plugins/codexclaw/skills/repo-map/SKILL.md) | 기존 검색 도구로 입력·처리·출력·테스트의 실제 경로를 확인. 지도에 없다는 이유로 코드가 없다고 단정하지 않음 |
| [지적의 처리 근거와 재검토 범위](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/plugins/codexclaw/skills/pabcd/references/phase-audit.md) | task-flow와 [검토 역할](../roles/reviewer.md)에 수정·근거 있는 반박·선택 사항 보류 및 관련 영향 재검토 |
| [조건부 경로의 실제 발동과 관찰](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/plugins/codexclaw/skills/pabcd/references/phase-check.md) | [task-verify](../.agents/skills/task-verify/SKILL.md)에 검사 대상 확인과 오류·대체 경로 실행 확인. 허용된 방법으로 확인할 수 없으면 미확인으로 표시 |
| [중단 후 이어갈 수 있는 근거와 반복 실패 대응](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/plugins/codexclaw/skills/pabcd/references/loop-engineering.md) | 기존 [근거 양식](../templates/work-evidence.md)에 필요할 때만 재개 항목 사용. 과제 안의 파일·로그를 다시 읽고 현재 버전과 대조 |

원본의 전역 대화·메모리 검색, 플러그인·hooks·상태 머신, 다중 공급자 모델 설정, 브라우저 자동화, 원격 카탈로그 검색은 반영하지 않았다. RepoMap의 tree-sitter/PageRank 코드와 의존성도 가져오지 않았다. 제공 환경의 설정·기능을 바꾸지 않고 명시적으로 문서를 읽는 사용 경로를 유지한다.

이 하네스는 **지침**이며 단계 전환이나 권한을 코드로 강제하지 않는다. 단독 재검토는 독립 검토가 아니며, 체크리스트 작성은 실행 증거가 아니다. 실제 과제의 필수 문서·시간·허용 범위가 우선한다.

[원본 LICENSE](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/LICENSE)는 MIT다. [NOTICE](https://github.com/lidge-jun/codexclaw/blob/a7ff3b6b1e8221dc9be4f665f26b50270854b951/NOTICE.md)는 일부 구성 요소의 별도 출처와 라이선스를 명시한다. 이번 변경은 원본 코드·문서·키트 파일을 복사하지 않았으며, 향후 복사한다면 해당 파일의 라이선스와 고지를 따로 보존해야 한다. [전체 출처 범위](../SOURCES.md).
