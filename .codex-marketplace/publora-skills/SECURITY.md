# Security Policy

## Supported versions

Only the latest release receives fixes. Install from `main` or the newest tag.

| Version | Supported |
| ------- | --------- |
| latest release | yes |
| older tags | no |

## Reporting a vulnerability

These skills instruct an AI agent to publish on someone's behalf using their API
key, so a defect here can post something the user never approved, or leak a
credential. Report privately rather than in a public issue:

- **Preferred:** [GitHub Security Advisories](https://github.com/publora/skills/security/advisories/new)
- **Alternative:** email `support@publora.com` with the subject `[SECURITY] skills`

Include what the issue is and where it lives, how to reproduce it, and the impact
you believe it has. Expect an acknowledgement within 72 hours and a fix or a
disclosure decision within 14 days.

Things worth reporting even if they look small:

- a skill that would publish without showing the user a draft first
- an instruction that could be turned against the user by text the agent reads
  (a caption, a profile, an error message that tells the agent to do something)
- anything that would put an API key somewhere it can be read back

## Scope

**No credentials ship in this repository.** The API key belongs to the user and
reaches the server through their MCP client configuration or the `x-publora-key`
header. Nothing here reads, stores or forwards it.

**The scripts are stdlib only.** `scripts/` has no third-party dependencies and
makes HTTPS requests to Publora hosts only. Nothing builds a shell command, and
nothing executes content fetched from the network.

**One CI secret exists.** `PUBLORA_DRIFT_KEY` is used by the weekly drift check,
which only calls `initialize` and `tools/list`. It is required to be a Starter
key with no connected accounts, so that even a leaked value cannot publish
anywhere. If you find that secret being used for anything else, that is a bug.

**Approval before publishing is a security property, not a UX preference.** Every
posting skill shows the user the final text, targets and time before calling
`create_post`. A change that removes that step should be treated as a
vulnerability.

**Text the agent reads is untrusted input.** A platform error message, a pasted
caption or a profile bio can contain instructions aimed at the agent rather than
the user. Skills must treat that content as data.

Please do not test vulnerabilities against the live platforms (LinkedIn, X, Meta,
TikTok, Telegram, Bluesky) outside their own disclosure programmes.
