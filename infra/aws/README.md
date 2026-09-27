# AWS target

`bootstrap.yaml` creates the account-level basics for this project:
- a monthly **budget** with email alerts (50/80/100% actual + 100% forecast)
- a **GitHub OIDC** trust (so CI deploys without stored AWS keys) and a deploy role limited to this repo's `production` environment
- an **ECR** repository (immutable tags) for the project's images

Compute (EC2, ECS/Fargate, etc.) is project-specific: add it in a second stack after kickoff, and keep it tagged `project=<name>`.

## First-time setup (human)
1. AWS account with root MFA; an admin IAM user (not root) with MFA and `SignInLocalDevelopmentAccess`.
2. AWS CLI ≥ 2.32: `aws login --profile <project>-admin --region <region>`.
3. Only one GitHub OIDC provider can exist per account. If another project already created it, deploy with `CreateOidcProvider=false`.

## Deploy the bootstrap
```
aws cloudformation deploy --profile <project>-admin --region <region> \
  --stack-name <project>-bootstrap --template-file infra/aws/bootstrap.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ProjectName=<project> GitHubRepo=<owner>/<repo> \
      AlertEmail=<email> MonthlyBudgetUsd=25 CreateOidcProvider=true
```
Confirm the SNS subscription email, or no alerts arrive.

## Secrets
`scripts/put_secret.sh <project>/<name>` stores a value in Secrets Manager (you run it).
