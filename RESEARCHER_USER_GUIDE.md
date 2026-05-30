# Survey Lab Researcher User Guide

This guide explains how researchers can use Survey Lab to create, publish, and review social media study surveys.

Survey Lab is a research prototype. It is designed for study setup, participant testing, gaze-data collection, and results review. It is not a production authentication platform or a professional eye-tracking system.

This guide is written for the deployed Survey Lab service:

- Researcher site: <https://cs14-3-test.onrender.com>
- Participant link format: `https://cs14-3-test.onrender.com/participant?invite=INVITE_CODE`

Use the researcher site above to create and publish surveys. After publishing, share the generated participant link with participants.

## 1. Overview

The researcher interface allows you to:

- Create a social media survey.
- Add one or more news posts.
- Configure platform-style presentations for Instagram, Facebook, X, and TikTok.
- Create A/B versions of posts.
- Add optional question blocks.
- Generate an invite code and participant link.
- Publish the survey.
- Review participant sessions and export collected data.

The typical researcher workflow is:

1. Sign up or log in.
2. Create a new survey.
3. Add news content.
4. Configure platform style, A/B version, and question block settings.
5. Generate an invite code.
6. Publish the survey.
7. Share the participant link.
8. Review or export results after participants complete the study.

## 2. Before You Start

Make sure you have:

- Access to the deployed Survey Lab researcher site: <https://cs14-3-test.onrender.com>.
- A researcher account.
- One or more news article links.
- A modern browser such as Chrome, Edge, or Safari.
- Participant access to a webcam if gaze data will be collected.
- Participant permission to use the camera on `cs14-3-test.onrender.com`.
- A stable internet connection for researcher setup, participant completion, and result upload.

The service is deployed on Render. If the site has been idle, the first visit may take longer while the service wakes up. Wait for the page to load before retrying.

## 3. Sign Up and Log In

### Sign Up

1. Open <https://cs14-3-test.onrender.com>.
2. Go to the researcher registration page.
3. Enter your username or email.
4. Enter a password.
5. Submit the registration form.

Expected result: you are taken into the researcher interface after successful registration.

### Log In

1. Open <https://cs14-3-test.onrender.com>.
2. Go to the researcher login page.
3. Enter your registered username or email.
4. Enter your password.
5. Submit the login form.

Expected result: you are taken to the Survey Lab researcher dashboard.

### Sign Out

Use the account menu and select **Sign out** when you finish using the researcher interface.

## 4. Create a New Survey

Use **New Survey** to start a clean survey draft.

1. Open the researcher dashboard.
2. Select **New Survey** from the navigation.
3. Start editing the survey post content.

Expected result: the editor shows a blank or default survey draft that can be configured.

Notes:

- A draft survey is different from a published survey.
- Published surveys appear in the history/results workflow only after publishing.
- Starting a new survey avoids accidentally editing an old completed survey.

## 5. Add and Edit News Content

The news content defines what participants will see in the study feed.

### Add a News Link

1. Paste a news URL into the **News Link** field.
2. Click **Fetch Image**.
3. Wait for the system to fetch the title and image.

Expected result: the preview updates with the fetched article title and image.

Notes:

- Some websites block metadata scraping.
- If fetching fails, you can still manually edit the post content where the interface allows it.
- Fetching usually uses page metadata such as Open Graph or Twitter Card tags.

### Edit Post Elements

Depending on the selected platform style, you can edit visible post elements such as:

- Caption or title text.
- Image.
- Avatar.
- Username or handle.
- Social metrics such as likes, comments, and shares.
- Action button labels or icons.

Expected result: the live preview updates after you edit the post.

## 6. Configure Platform Styles

Survey Lab supports several platform-style layouts:

- Instagram
- Facebook
- X/Twitter
- TikTok

To configure a platform style:

1. Open the **Platform Style** dropdown.
2. Select the platform you want to simulate.
3. Review the live preview.

Expected result: the preview changes to match the selected platform style.

Use platform styles when your study needs to compare how the same or similar news content is perceived across different social media layouts.

Notes:

- Platform style affects the participant-facing layout.
- Different platform styles may display post images, captions, engagement controls, and social metrics differently.
- Keep platform selection consistent with your research question.

## 7. Configure A/B Versions

Each survey post can use **Version A** and **Version B**.

A/B versions are useful for comparing controlled differences, such as:

- Different captions.
- Different images.
- Different platform styles.
- Different social metrics.
- Different question wording.
- Different visible or hidden post elements.

To configure versions:

1. Select **Version A**.
2. Configure the post content and platform style.
3. Select **Version B**.
4. Configure the alternative version.
5. Review the preview for each version.

Expected result: each version keeps its own configured post state.

Notes:

- Use A/B versions deliberately. They should represent meaningful experimental conditions.
- Avoid changing too many variables at once unless your study design requires it.
- When publishing, confirm which version is selected and intended for participants.

## 8. Add Question Blocks

Question blocks allow you to collect direct participant responses after a post.

### Enable a Question Block

1. Find the **Question Block** section.
2. Turn on **Enable**.
3. Choose the question type.
4. Enter the question text.
5. Add or edit answer options.
6. Choose whether the answer is required.

Supported question types:

- **Single Choice**: participants choose one option.
- **Multiple Choice**: participants can choose more than one option.

Expected result: the question appears in the preview and later appears in the participant feed.

Notes:

- Question answers are saved as non-gaze survey data.
- Question options are exported in the survey CSV.
- Use clear option labels so exported results are easy to interpret.
- If an answer is required, participants should not be able to finish the question without selecting an option.

## 9. Generate Invite Code and Publish

The invite code connects a participant session to a published survey.

### Generate an Invite Code

1. Go to **Participant Access Control**.
2. Click **Generate Invite Code**.
3. Confirm that the invite code appears in the editor.

Expected result: the survey has a unique invite code.

### Publish the Survey

1. Confirm the survey content is ready.
2. Confirm the correct version and platform settings are selected.
3. Confirm the question block settings.
4. Click **Publish Survey Link**.
5. Copy the participant link shown after publishing.

Expected result: the survey is published, and the system gives you an invite code and participant URL.

The participant link should look like this:

```text
https://cs14-3-test.onrender.com/participant?invite=INVITE_CODE
```

Notes:

- You must generate an invite code before publishing.
- Share the participant link with participants.
- Participants can also enter the invite code manually if needed.
- A published survey is treated as a study record and should be reviewed before distribution.

## 10. Manage Published Surveys

Published surveys can be reviewed from the researcher interface.

Use the history or results areas to inspect:

- Published survey records.
- Published news posts.
- Platform styles.
- Published version information.
- Participant result availability.

Expected result: published surveys appear as records after successful publishing.

Notes:

- Draft surveys may not appear in published history.
- Published survey records are summaries of what was sent to participants.
- If a survey was already completed or published, start a new survey when setting up a new study.

## 11. View and Export Results

Survey Lab supports several result review methods.

### Participant Sessions

Participant sessions store study completion and payload data. A session may include:

- Participant invite code.
- Start and end timestamps.
- Calibration logs.
- Gaze logs.
- Interaction logs.
- Question answers.

### Non-Gaze CSV Export

Use the non-gaze CSV export to inspect structured survey and answer data.

The CSV can include:

- Survey ID and title.
- News item ID and source URL.
- Survey variant and platform.
- Question text and option labels.
- Invite code and publication timestamp.
- Participant session ID and status.
- Participant answer IDs and answer timestamps.

Use this export when analysing question responses and participant session metadata.

### JSON Study Data

JSON study data is useful for detailed inspection and debugging. It may include raw gaze logs, calibration logs, interaction logs, and full participant payloads. In the deployed service, download available JSON data through the researcher interface.

### Heatmap Viewer

The heatmap viewer can help analyse gaze data through:

- Per-post region analysis.
- Position heatmap.
- Gaze replay.
- Platform filtering.
- Session statistics.

Use the heatmap viewer when you need to inspect where participants looked, how long they looked at regions, and how gaze moved during the study.

Notes:

- Gaze data is approximate and depends on webcam quality, lighting, face position, and calibration quality.
- Invalid gaze samples should be filtered during analysis.
- Combine gaze data with interaction logs and question answers for stronger interpretation.

## 12. Translation

Survey Lab includes translation support for interface and survey/post content.

Translation can help when participants need to view content in another language. The system can translate text such as captions, action labels, question text, and question options when the deployed translation service is configured.

Notes:

- Translation requires the deployed translation service to be available.
- If the translation service fails, use the original English content.
- Review translated survey content before publishing when accuracy matters.
- Translation quality may affect participant interpretation of news content and questions.

## 13. Data and Privacy Notes

Survey Lab uses invite codes to connect participant sessions with published surveys. The invite code should not include real personal identity information.

Recommended practices:

- Do not put participant names, student IDs, emails, or private identifiers into invite codes.
- Store exported CSV and JSON files securely.
- Do not commit participant data or private researcher accounts to a public repository.
- Remove test data before sharing the project externally.
- Explain the data collection process to participants before running a study.

The collected data may include behavioural logs and webcam-derived gaze estimates. Handle these data carefully according to your project ethics and privacy requirements.
