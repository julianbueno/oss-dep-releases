"""
Get the latest releases of the repositories used by GUIDE
"""

from github import Github
import os
import slack

slack_msg = ""

access_token = os.environ["GITHUB_TOKEN"]
g = Github(access_token)

critical = {
    "external-dns": "kubernetes-sigs/external-dns",
    "amazon-vpc-cni-k8s": "aws/amazon-vpc-cni-k8s",
}

medium = {
    "kubernetes": "kubernetes/kubernetes",
    "kubectl": "kubernetes/kubectl",
    "dashboard": "kubernetes/dashboard",
    "metrics-server": "kubernetes-sigs/metrics-server",
    "autoscaler": "kubernetes/autoscaler",
    "cw-agent": "aws-samples/amazon-cloudwatch-container-insights",
}

low = {
    "terraform (tf)": "hashicorp/terraform",
    "terragrunt": "gruntwork-io/terragrunt",
    "aws-cli": "aws/aws-cli",
    "tf-provider-aws": "terraform-providers/terraform-provider-aws",
    "tf-aws-vpc": "terraform-aws-modules/terraform-aws-vpc",
    "tf-aws-eks": "terraform-aws-modules/terraform-aws-eks",
    "tf-aws-rds": "terraform-aws-modules/terraform-aws-rds",
    "tf-aws-s3-bucket": "terraform-aws-modules/terraform-aws-s3-bucket",
    "tf-aws-iam": "terraform-aws-modules/terraform-aws-iam",
    "tflint": "terraform-linters/tflint",
    "tfsec": "tfsec/tfsec",
    "helm": "helm/helm",
    "terraform-aws-route53": "terraform-aws-modules/terraform-aws-route53",
    "tf-aws-vpn-gateway":  "terraform-aws-modules/terraform-aws-vpn-gateway",
    "kubent": "doitintl/kube-no-trouble"
}


def retrieveRepoAndPrint(title, array):
    """
    Retrieve release and add towards slack_msg
    """

    global slack_msg, g

    slack_msg += "\n -=[ `"+title+"` ]=- \n"

    for key, value in array.items():
        repository = g.get_repo(value)
        try:
            response = repository.get_latest_release()
            line = f"• {key} :: release :: {response.title}"
            slack_msg += line + "\n"

        except Exception:
            # fallback to tag if cannot find latest release
            tags = repository.get_tags()
            line = f"• {key} :: release :: {tags[0].name}"
            slack_msg += line + "\n"


def get_releases():
    """
    Get latest releases of the repositories
    """

    global slack_msg, critical, medium, low

    slack_msg += ":grey_exclamation: `Release Radar Report`"
    slack_msg += " :grey_exclamation: \n"

    retrieveRepoAndPrint("Critical", critical)
    retrieveRepoAndPrint("Medium", medium)
    retrieveRepoAndPrint("Low", low)

    print(slack_msg)
    slack.send_message_to_webhook(slack_msg)


if __name__ == "__main__":
    get_releases()
