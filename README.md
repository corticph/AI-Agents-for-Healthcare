
```
  ██████╗ ██████╗ ██████╗ ████████╗██╗
 ██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██║
 ██║     ██║   ██║██████╔╝   ██║   ██║
 ██║     ██║   ██║██╔══██╗   ██║   ██║
 ╚██████╗╚██████╔╝██║  ██║   ██║   ██║
  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝

  █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗
 ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝
 ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗
 ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
 ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║
 ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
```

![YAML](https://img.shields.io/badge/YAML-1.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)

> A community-driven library of production-ready AI agent system prompts for healthcare and life sciences, built on the [Corti Agentic Framework](https://www.corti.ai/agentic-framework).

## 📖 Table of Contents

- [About This Repository](#-about-this-repository)
- [Key Features](#-key-features)
- [Repository Structure](#-repository-structure)
- [Quick Start](#-quick-start)
- [Contributing](#-contributing-to-the-library)
- [Security and Privacy](#-security-and-privacy)

## 🏥 About This Repository

This repository serves as a **prompt library and validation toolkit** for AI agents in healthcare. It provides:

1. **Curated System Prompts**: Production-ready, field-tested agent configurations for clinical and administrative workflows
2. **Standardized Schema**: A structured YAML format ensuring consistency and maintainability
3. **Validation Tools**: Automated quality checks for prompt formatting, readability, and best practices
4. **Community Contributions**: An open platform for healthcare organizations and developers to share and improve agent prompts

### What is the Corti Agentic Framework?

The [Corti Agentic Framework](https://www.corti.ai/agentic-framework) is a specialized AI platform designed specifically for healthcare and life sciences, focused on creating **reliable, governed multi-agent systems**. It transforms "agent chaos into governed systems" by providing:

- **Governed Orchestration**: Manages agent roles, routes tasks, and enforces boundaries
- **Domain-Specific Expertise**: Pre-configured "Experts" with targeted clinical and administrative intelligence
- **Comprehensive Oversight**: Guardrails, audit trails, and complete visibility into agent actions
- **Standards Support**: Built on Agent-to-Agent (A2A) and Model Context Protocol (MCP) standards
- **High-Stakes Reliability**: Designed for healthcare environments requiring predictable and compliant AI behavior

This repository contains the **system prompts** that power these intelligent agents, enabling capabilities like medical coding, clinical documentation improvement (CDI), revenue cycle management, and automated clinical workflows.

## 🎯 Key Features

### For Prompt Library Users

- 🤖 **Production-Ready Agents**: Field-tested prompts for medical coding, clinical intelligence, and administrative tasks
- 📋 **Standardized Format**: Consistent YAML schema across all agent configurations
- 📚 **Comprehensive Documentation**: Detailed descriptions, use cases, and execution flows for each agent
- ✅ **Quality Assurance**: All prompts validated for syntax, structure, and readability

### For Contributors

- 🛠️ **Validation Toolkit**: Automated YAML validation with comprehensive checks
- 📖 **Clear Schema**: Well-documented structure for creating new agent prompts
- 🎨 **Best Practices**: Built-in checks for readability, formatting, and quotation standards
- 🔄 **Version Control**: Semantic versioning for prompt iterations
- 🤝 **Open Collaboration**: Community-driven improvement and expansion

## 📂 Repository Structure

```
corti-agents/
├── prompts/                     # Agent system prompt library
│   ├── schema.yaml              # YAML schema specification
│   └── [additional agents]      # Community-contributed prompts
├── tools/                       # Validation toolkit
│   └── validate_prompts.py      # Comprehensive YAML validator
└── README.md                    # This file
```

## 🚀 Quick Start

### For Prompt Users

1. **Browse Available Agents**: Explore the `prompts/` directory for production-ready agent configurations
2. **Select an Agent**: Choose an agent that matches your use case (e.g., medical coding, clinical documentation)
3. **Integrate with Framework**: Use these prompts with the Corti Agentic Framework by integrating directly with the Corti API (docs.corti.ai) or on the Console (console.corti.app)
4. **Customize as Needed**: Adapt prompts to your specific requirements while maintaining the schema structure

### For Contributors

#### Prerequisites

- Python 3.7 or higher
- PyYAML library

```bash
pip install pyyaml
```

#### Creating a New Agent Prompt

1. **Use the Schema**: Follow the structure defined in `prompts/schema.yaml`
2. **Reference Examples**: Use `medical-coding.yaml` as a template
3. **Required Fields**: Ensure all mandatory schema fields are included
4. **Best Practices**: Use literal block scalars (`|`) for long text, avoid unnecessary quotes
5. **Validate**: Run the validation tool before submitting

#### Validating Your Prompts

Validate all prompt files against the schema:

```bash
python tools/validate_prompts.py
```

The validator checks for:
- ✅ YAML syntax errors
- ✅ Schema compliance (required fields)
- ✅ Extra fields not defined in schema
- ✅ Proper string quoting and escaping
- ✅ Mismatched or unclosed quotations
- ✅ Indentation consistency
- ✅ Special character handling
- ✅ Field type validation
- ✅ Quotation best practices (warns about unnecessary quotes)
- ✅ Readability best practices (long strings, literal blocks, paragraph breaks)


## 🤝 Contributing to the Library

We welcome contributions from healthcare organizations, AI developers, and clinical informaticists! This library thrives on community input and real-world experience.

### Contribution Guidelines

- **Production-Ready**: Only submit agents tested in real workflows
- **Schema Compliance**: All agents must pass validation
- **Clear Documentation**: Provide detailed descriptions and use cases
- **Semantic Versioning**: Use `major.minor.patch` versioning (e.g., 1.0.0)
- **Expert Attribution**: Credit your organization in the `builder` field
- **Privacy First**: Never include PHI, credentials, or proprietary information

## 🔐 Security and Privacy

This repository contains **system prompts only** - no patient data, credentials, or proprietary information should ever be included. When contributing:

- ✅ Share agent instructions and workflow logic
- ✅ Describe use cases and expected inputs
- ✅ Document output formats and structures
- ❌ Never include PHI or PII
- ❌ Never include API keys or credentials
- ❌ Never include institution-specific data

## 📄 License

Apache 2.0

## 🌟 Acknowledgments

Built by the healthcare AI community for advancing reliable, governed agent systems in clinical and administrative workflows.

