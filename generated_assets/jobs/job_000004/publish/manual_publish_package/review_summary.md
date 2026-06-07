# P0-B 输出检查摘要

Job: `job_000004`
Candidate: `candidate_000004`

## 当前结论

- P0-B 链路已跑通：文字 seed -> planning -> prompt package -> manual slot -> candidate import -> QA -> manual publish package。
- 这是 manual package，不会自动发布。
- 主平台 payload 已准备：Bilibili、Douyin、Xiaohongshu、YouTube Shorts。
- TikTok、Kuaishou、Instagram Reels 只是 P0-B stub，状态应为 blocked/tool setup。

## 重要提醒

- `final_video.mp4` 是测试 fixture: `True`。
- 如果 `is_test_fixture` 为 true，它不能当真实生成视频发布，只证明链路能管理视频文件。
- `cover_finalized` 仍为 false，发布前需要人工选封面或后续生成封面。
- P0-B QA 通过只代表链路完整、记录完整、人工能继续，不代表成片质量达标。

## 你最该先看的文件

- `manifest.json`
- `platform_payloads/platform_payloads.json`
- `source_and_asset_provenance.md`
- `titles/selected_title.txt`
- `cover/cover_notes.md`
