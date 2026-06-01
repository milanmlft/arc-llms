# Makefile for the litellm stack.
# Run targets from this directory (litellm/).
# Run `make help` to list targets.

VM_IP    := $(shell terraform output -json vm_ips 2>/dev/null | tr -d '[]" ' | cut -d, -f1)
ENDPOINT := https://litellm.arc-llm.condenser.arc.ucl.ac.uk
SSH      := ssh -J condenser almalinux@$(VM_IP)

.PHONY: help init plan apply destroy deploy all ip ssh status logs verify

help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## terraform init
	terraform init

plan: ## terraform plan
	terraform plan

all: apply deploy ## terraform apply, then ansible deploy

apply: ## terraform apply (create/update VM)
	terraform apply

destroy: ## terraform destroy (delete VM)
	terraform destroy

deploy: ## Run the Ansible playbook against the VM
	ansible-playbook -i generate_inventory.py full.yaml

ip: ## Print the VM IP from terraform output
	@echo $(VM_IP)

ssh: ## SSH into the VM
	$(SSH)

status: ## Show running containers on the VM
	@$(SSH) "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

logs: ## Follow the litellm container logs
	$(SSH) "docker logs --tail 100 -f litellm"

verify: status ## Check containers and probe the endpoint
	@echo
	@echo "GET $(ENDPOINT)/health/liveliness"
	@curl -fsS $(ENDPOINT)/health/liveliness && echo
	@echo
	@echo "GET $(ENDPOINT)/v1/models (authenticated)"
	@curl -fsS -H "Authorization: Bearer sk-$$(cat .master)" $(ENDPOINT)/v1/models | head -1
	@echo
