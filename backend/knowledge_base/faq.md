# CloudScale AI — Frequently Asked Questions

## General

### What is CloudScale AI?

CloudScale AI is an intelligent cloud infrastructure platform that combines predictive auto-scaling, AI-driven anomaly detection, cost optimization, and multi-cloud management in a single solution. It helps businesses run their cloud infrastructure more efficiently, reliably, and cost-effectively.

### How does CloudScale AI differ from basic monitoring tools?

Traditional monitoring tools alert you after something goes wrong. CloudScale AI uses machine learning to predict issues before they happen — typically twelve minutes before impact — and can automatically take corrective action. We also combine monitoring with active optimization, so you get both visibility and automated improvement.

### Do I need to replace my existing tools?

No. CloudScale AI integrates with your existing stack including PagerDuty, Datadog, Slack, Jira, and ServiceNow. It adds a layer of intelligence on top of your current tools rather than replacing them.

## Technical

### How does the agent work?

Our lightweight agent runs inside your environment and consumes less than one percent of host resources. It collects infrastructure metrics locally and transmits only aggregated, anonymized signals to our cloud control plane. No application data or customer data ever leaves your environment.

### Which cloud providers are supported?

We support Amazon Web Services, Microsoft Azure, and Google Cloud Platform. The Starter plan supports one provider, Professional supports two, and Enterprise supports all three with unlimited instances.

### Does it work with Kubernetes?

Yes. CloudScale AI has native Kubernetes support including pod-level scaling, cluster autoscaling, and namespace-level cost attribution. We support managed Kubernetes services like EKS, AKS, and GKE, as well as self-managed clusters.

### What is the setup time?

Most customers are up and running within two hours. Our guided onboarding walks you through agent deployment, integration setup, and initial configuration. Enterprise customers receive white-glove onboarding with a dedicated customer success manager.

## Security and Compliance

### Is CloudScale AI secure?

Yes. We are SOC two Type two certified, HIPAA-compliant, and GDPR-ready. All data in transit uses TLS one point three, and data at rest is encrypted with AES-256. We support SSO via SAML and OIDC with role-based access control.

### Does CloudScale AI access my application data?

No. Our agent only collects infrastructure-level metrics such as CPU usage, memory, network throughput, and disk I/O. We never access application logs, databases, or customer data.

### Can I deploy CloudScale AI in an air-gapped environment?

Enterprise customers can deploy a fully on-premises version of CloudScale AI that operates without any external connectivity. Contact our sales team for details.

## Pricing and Support

### Is there a free trial?

Yes. All plans include a fourteen-day free trial with full feature access. No credit card is required to start.

### What kind of support do you offer?

Starter plans include community support with a forty-eight-hour response time. Professional plans include priority support with a four-hour response time. Enterprise plans include twenty-four-seven premium support with a one-hour response SLA and a dedicated customer success manager.

### Can I switch plans?

Yes. You can upgrade or downgrade your plan at any time. Changes take effect at the start of your next billing cycle. If you upgrade mid-cycle, you will receive a prorated credit.

### Do you offer discounts for annual billing?

Yes. Annual billing is available at a fifteen percent discount on Starter and Professional plans. Enterprise customers can discuss multi-year commitments with our sales team for additional savings.
