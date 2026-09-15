import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const root = "/home/ubuntu/Allamni-Apex-Enterprise";
const domains = [
  ["learners", "Learner", "learner profiles, consent, and owner-scoped access"],
  ["assessments", "Assessment", "diagnostic sessions, attempts, and mastery evidence"],
  ["curriculum", "Curriculum", "standards, learning objectives, and progression maps"],
  ["content", "Content", "content review, licensing, and publication boundaries"],
  ["tutoring", "Tutoring", "guided sessions, citations, and tutor safeguards"],
  ["goals", "Goal", "learning plans, milestones, and next-best actions"],
  ["institutions", "Institution", "educator operations, cohorts, and reporting scope"],
];
const features = ["learner-profile", "diagnostic-assessment", "learning-roadmap", "tutor-session", "content-library", "educator-console", "progress-insights"];

async function emit(relativePath, content) {
  const target = path.join(root, relativePath);
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, content.trimStart(), "utf8");
}

for (const [domain, entity, purpose] of domains) {
  const folder = `backend/domain/${domain}`;
  await emit(`${folder}/__init__.py`, `"""${entity} bounded context: ${purpose}."""\nfrom .contracts import ${entity}Snapshot\nfrom .policies import requires_human_review\n\n__all__ = ["${entity}Snapshot", "requires_human_review"]\n`);
  await emit(`${folder}/contracts.py`, `from datetime import datetime\nfrom pydantic import BaseModel, Field\n\nclass ${entity}Snapshot(BaseModel):\n    identifier: str = Field(min_length=1, max_length=150)\n    status: str = Field(min_length=1, max_length=40)\n    owner_id: str | None = None\n    correlation_id: str | None = None\n    updated_at: datetime | None = None\n\nclass ${entity}Page(BaseModel):\n    items: list[${entity}Snapshot] = Field(default_factory=list)\n    next_cursor: str | None = None\n`);
  await emit(`${folder}/commands.py`, `from dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Create${entity}:\n    actor_id: str\n    correlation_id: str\n    reason: str | None = None\n\n@dataclass(frozen=True)\nclass Review${entity}:\n    identifier: str\n    actor_id: str\n    decision: str\n    reason: str\n`);
  await emit(`${folder}/events.py`, `from dataclasses import dataclass\nfrom datetime import datetime, timezone\n\n@dataclass(frozen=True)\nclass ${entity}Event:\n    event_type: str\n    identifier: str\n    correlation_id: str\n    occurred_at: datetime\n\n    @classmethod\n    def now(cls, event_type: str, identifier: str, correlation_id: str):\n        return cls(event_type, identifier, correlation_id, datetime.now(timezone.utc))\n`);
  await emit(`${folder}/policies.py`, `REVIEW_ACTIONS = {"PUBLISH_CONTENT", "INSTITUTION_EXPORT", "HIGH_RISK_INTERVENTION", "EXTERNAL_MEDIA"}\n\ndef requires_human_review(action: str, learner_age_band: str = "adult") -> bool:\n    return action.upper() in REVIEW_ACTIONS or learner_age_band.lower() in {"child", "minor"}\n\ndef may_expose_personalisation(owner_match: bool, consent: bool) -> bool:\n    return owner_match and consent\n`);
  await emit(`${folder}/repository.py`, `from typing import Protocol\nfrom .contracts import ${entity}Page, ${entity}Snapshot\n\nclass ${entity}Repository(Protocol):\n    def get(self, identifier: str, actor_id: str) -> ${entity}Snapshot | None: ...\n    def list_for_owner(self, actor_id: str, cursor: str | None = None, limit: int = 50) -> ${entity}Page: ...\n`);
  await emit(`${folder}/service.py`, `from .contracts import ${entity}Snapshot\n\ndef display_label(snapshot: ${entity}Snapshot) -> str:\n    return f"{snapshot.identifier} · {snapshot.status}"\n\ndef is_terminal(status: str) -> bool:\n    return status.upper() in {"ARCHIVED", "COMPLETED", "REJECTED", "WITHDRAWN"}\n`);
  await emit(`${folder}/telemetry.py`, `METRIC_PREFIX = "allamni.${domain}"\n\ndef metric(name: str) -> str:\n    return f"{METRIC_PREFIX}.{name}"\n\ndef tags(status: str, correlation_id: str | None) -> dict[str, str]:\n    return {"status": status, "correlation_id": correlation_id or "unassigned"}\n`);
  await emit(`backend/tests/domain/test_${domain}_domain.py`, `from domain.${domain}.contracts import ${entity}Snapshot\nfrom domain.${domain}.policies import requires_human_review\nfrom domain.${domain}.service import display_label, is_terminal\n\ndef test_${domain}_contract_and_safeguards():\n    snapshot = ${entity}Snapshot(identifier="${domain}-001", status="ACTIVE", correlation_id="req-${domain}")\n    assert display_label(snapshot) == "${domain}-001 · ACTIVE"\n    assert is_terminal("COMPLETED")\n    assert requires_human_review("PUBLISH_CONTENT")\n    assert not requires_human_review("READ")\n`);
  for (const document of ["operating-model", "safeguards", "acceptance-criteria"]) {
    await emit(`docs/domains/${domain}/${document}.md`, `# ${entity}: ${document.replaceAll("-", " ")}\n\n## Responsibility\n\nThe ${entity} bounded context owns ${purpose}. Every command identifies an accountable actor and correlation identifier; every sensitive side effect follows an explicit review policy.\n\n## Learner safeguard\n\nAdaptive recommendations are support tools, not diagnoses. Content, interventions, institution exports, and minor learner data require scoped ownership and applicable human review.\n\n## Acceptance signal\n\nA feature is accepted only when its test, policy contract, and operational evidence agree.\n`);
  }
}

for (const feature of features) {
  const className = feature.split("-").map(word => word[0].toUpperCase() + word.slice(1)).join("");
  const folder = `frontend/lib/features/${feature}/enterprise`;
  await emit(`${folder}/${feature}_model.dart`, `class ${className}Model {\n  const ${className}Model({required this.id, required this.status, this.correlationId});\n  final String id;\n  final String status;\n  final String? correlationId;\n}\n`);
  await emit(`${folder}/${feature}_state.dart`, `class ${className}State {\n  const ${className}State({this.loading = false, this.error, this.items = const []});\n  final bool loading;\n  final String? error;\n  final List<Object> items;\n}\n`);
  await emit(`${folder}/${feature}_repository.dart`, `abstract interface class ${className}Repository {\n  Future<List<Object>> load({String? cursor});\n}\n`);
  await emit(`${folder}/${feature}_controller.dart`, `import '${feature}_state.dart';\n\nclass ${className}Controller {\n  ${className}State state = const ${className}State();\n  void beginLoad() => state = const ${className}State(loading: true);\n  void fail(String message) => state = ${className}State(error: message);\n}\n`);
  await emit(`${folder}/${feature}_policy.dart`, `bool canProceed${className}(String action, {required bool reviewed, required bool ownerMatch}) {\n  const protected = {'publish_content', 'institution_export', 'high_risk_intervention'};\n  return ownerMatch && (!protected.contains(action) || reviewed);\n}\n`);
  await emit(`${folder}/${feature}_accessibility.dart`, `const ${feature.replaceAll("-", "_")}Labels = {\n  'loading': 'جارٍ تحميل ${feature}',\n  'empty': 'لا توجد بيانات ${feature}',\n  'retry': 'إعادة المحاولة',\n};\n`);
  await emit(`${folder}/README.md`, `# ${feature}\n\nThis module separates learner-facing state, repository boundaries, policy checks, accessibility text, and model contracts so personalised learning features can grow without crossing safeguarding boundaries.\n`);
}

for (const file of [
  "infrastructure/kubernetes/base/namespace.yaml", "infrastructure/kubernetes/base/gateway-deployment.yaml", "infrastructure/kubernetes/base/frontend-deployment.yaml", "infrastructure/kubernetes/base/gateway-service.yaml", "infrastructure/kubernetes/base/network-policy.yaml", "infrastructure/kubernetes/overlays/staging/kustomization.yaml", "infrastructure/kubernetes/overlays/production/kustomization.yaml", "infrastructure/observability/slo.md", "infrastructure/observability/alerts.md", "infrastructure/security/secret-rotation.md", "docs/learner-privacy-impact.md", "docs/content-governance.md", "docs/agent-safety-runbook.md", "docs/institution-rollout.md"
]) {
  const title = path.basename(file).replaceAll("-", " ");
  await emit(file, file.endsWith(".yaml") ? `apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: allamni-${title.replace(".yaml", "").replaceAll(" ", "-")}\n  labels:\n    app.kubernetes.io/name: allamni\ndata:\n  managed-by: enterprise-expansion\n` : `# ${title}\n\nThis artifact records a controlled Allamni operating boundary. It is a safe template, not a production authorisation; learner data, external content, institutional exports, and AI-provider changes require scoped review.\n`);
}

console.log(`Generated ${domains.length} learning domains and ${features.length} Flutter feature modules.`);
