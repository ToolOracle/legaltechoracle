# LegalTechOracle MCP Server v1.0.0

**Contract Lifecycle & Legal Compliance MCP Server — 12 tools for EU-compliant contracts, NDAs (GeschGehG), DSGVO AVV (Art.28), freelancer agreements (Scheinselbständigkeit), clause risk scanning, DORA Art.28-30 regulatory clause checks.**

Port 12701 | Part of [ToolOracle](https://tooloracle.io) & [FeedOracle](https://feedoracle.io) Infrastructure

## Quick Connect

```bash
# Claude Desktop / Claude Code
claude mcp add legaltechoracle https://tooloracle.io/legaltech/mcp

# Or use directly
curl -X POST https://tooloracle.io/legaltech/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## 12 Tools

| `contract_draft` | Tool 1 |
| `nda_generate` | Tool 2 |
| `freelancer_contract` | Tool 3 |
| `dpa_generate` | Tool 4 |
| `clause_risk_scan` | Tool 5 |
| `contract_summary` | Tool 6 |
| `termination_analysis` | Tool 7 |
| `obligation_matrix` | Tool 8 |
| `cross_jurisdiction` | Tool 9 |
| `regulatory_clause_check` | Tool 10 |
| `force_majeure_check` | Tool 11 |
| `liability_cap_check` | Tool 12 |

## Endpoints

| Endpoint | URL |
|----------|-----|
| MCP (StreamableHTTP) | `https://tooloracle.io/legaltech/mcp/` |
| MCP (FeedOracle) | `https://feedoracle.io/legaltech/mcp/` |
| Health | `https://tooloracle.io/legaltech/health` |

## Architecture

- **Transport**: StreamableHTTP + SSE (MCP Protocol 2025-03-26)
- **Auth**: x402 micropayments (USDC on Base) + Stripe subscriptions
- **Signing**: ECDSA ES256K — every response cryptographically signed
- **Platform**: Whitelabel MCP Platform v1.0

## Part of the ToolOracle Ecosystem

ToolOracle operates 81+ MCP servers with 824+ tools across:
- **Compliance & Regulation** — DORA, MiCA, NIS2, AMLR, GDPR, EU AI Act
- **Finance & Tax** — CFOCoPilot, TaxOracle, ISO20022Oracle
- **Legal** — LawOracle, LegalTechOracle, ContractOracle
- **Healthcare** — HealthGuard
- **Supply Chain** — SupplyChainOracle
- **Cybersecurity** — CyberShield, DORAOracle, TLPTOracle
- **HR** — HROracle
- **Blockchain** — 13 chains (ETH, BTC, Solana, Arbitrum, etc.)
- **Business Intelligence** — SEO, Leads, Reviews, E-Commerce

## License

Proprietary — © 2026 ToolOracle / FeedOracle. All rights reserved.
Contact: enterprise@feedoracle.io
