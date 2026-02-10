#!/usr/bin/env python3
"""
Validate YAML prompt files against schema and check formatting.

This script validates all YAML files in the prompts directory against the schema.yaml
and performs comprehensive formatting checks including:
- YAML syntax validation
- Schema compliance
- String quoting and escaping
- Special character handling
- Structural integrity
"""

import os
import sys
import time
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
import re


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def animate_loading(duration: float = 1.5):
    """Display animated ASCII art loading screen"""
    ascii_art = r"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║      ██████╗ ██████╗ ██████╗ ████████╗██╗                           ║
║     ██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██║                           ║
║     ██║     ██║   ██║██████╔╝   ██║   ██║                           ║
║     ██║     ██║   ██║██╔══██╗   ██║   ██║                           ║
║     ╚██████╗╚██████╔╝██║  ██║   ██║   ██║                           ║
║      ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝                           ║
║                                                                       ║
║   ██╗   ██╗ █████╗ ██╗     ██╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ ║
║   ██║   ██║██╔══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗║
║   ██║   ██║███████║██║     ██║██║  ██║███████║   ██║   ██║   ██║██████╔╝║
║   ╚██╗ ██╔╝██╔══██║██║     ██║██║  ██║██╔══██║   ██║   ██║   ██║██╔══██╗║
║    ╚████╔╝ ██║  ██║███████╗██║██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║║
║     ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

    clear_screen()
    print(Colors.CYAN + ascii_art + Colors.ENDC)

    # Animated loading bar
    print("\n")
    bar_length = 60
    loading_text = "Initializing Validator"
    print(f"{' ' * 10}{Colors.BOLD}{loading_text}{Colors.ENDC}")
    print(f"{' ' * 10}", end='')

    steps = 25
    for i in range(steps + 1):
        progress = i / steps
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r{' ' * 10}[{Colors.GREEN}{bar}{Colors.ENDC}] {int(progress * 100)}%", end='', flush=True)
        time.sleep(duration / steps)

    print("\n" * 2)
    time.sleep(0.2)


class PromptValidator:
    """Validates YAML prompt files against schema and formatting rules."""

    def __init__(self, schema_path: str):
        """Initialize validator with schema file."""
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.errors = []
        self.warnings = []

    def _load_schema(self) -> Dict:
        """Load and parse the schema YAML file."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error loading schema: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Schema file not found: {self.schema_path}")
            sys.exit(1)

    def validate_file(self, file_path: str) -> bool:
        """
        Validate a single YAML file.

        Returns:
            bool: True if validation passes, False otherwise
        """
        self.errors = []
        self.warnings = []
        file_path = Path(file_path)

        print(f"\n{'='*60}")
        print(f"Validating: {file_path.name}")
        print(f"{'='*60}")

        # Check file exists
        if not file_path.exists():
            self.errors.append(f"File not found: {file_path}")
            return False

        # Read raw content for formatting checks
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False

        # Check YAML syntax and parse
        parsed_data = self._validate_yaml_syntax(raw_content, file_path)
        if parsed_data is None:
            return False

        # Perform all validation checks
        self._validate_schema_structure(parsed_data, file_path)
        self._validate_formatting(raw_content, file_path)
        self._validate_string_quoting(raw_content, file_path)
        self._validate_special_characters(raw_content, file_path)
        self._validate_field_types(parsed_data, file_path)
        self._validate_field_values(parsed_data, file_path)
        self._validate_quotation_best_practices(raw_content, file_path)
        self._validate_readability(raw_content, parsed_data, file_path)

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _validate_yaml_syntax(self, content: str, file_path: Path) -> Any:
        """Validate YAML syntax and return parsed data."""
        try:
            data = yaml.safe_load(content)
            return data
        except yaml.scanner.ScannerError as e:
            self.errors.append(f"YAML Scanner Error: {e}")
            self.errors.append("  → Check for invalid characters, incorrect indentation, or unclosed quotes")
            return None
        except yaml.parser.ParserError as e:
            self.errors.append(f"YAML Parser Error: {e}")
            self.errors.append("  → Check for structural issues like unbalanced brackets or incorrect nesting")
            return None
        except yaml.constructor.ConstructorError as e:
            self.errors.append(f"YAML Constructor Error: {e}")
            self.errors.append("  → Check for duplicate keys or invalid value types")
            return None
        except Exception as e:
            self.errors.append(f"YAML Error: {e}")
            return None

    def _validate_schema_structure(self, data: Dict, file_path: Path):
        """Validate that all required schema fields are present."""
        if data is None:
            return

        # Define allowed fields per schema
        allowed_top_level_fields = {
            'version',
            'agent_name',
            'builder',
            'description',
            'system_prompt',
            'supported_experts',
            'expert_prompts'
        }

        allowed_description_fields = {
            'overview',
            'how_it_works',
            'use_cases',
            'category'
        }

        allowed_how_it_works_fields = {
            'configuration_requirements',
            'execution_flow'
        }

        required_fields = [
            'version',
            'agent_name',
            'builder',
            'description',
            'system_prompt',
            'supported_experts'
        ]

        # Check for extra fields not in schema
        for field in data.keys():
            if field not in allowed_top_level_fields:
                self.warnings.append(
                    f"Field '{field}' is not in schema - consider removing or updating schema.yaml"
                )

        # Check required fields
        for field in required_fields:
            if field not in data:
                self.errors.append(f"Missing required field: '{field}'")
            elif data[field] == "" and field != 'builder':
                self.errors.append(f"Required field '{field}' is empty")

        # Validate description subfields
        if 'description' in data and isinstance(data['description'], dict):
            # Check for extra description fields
            for field in data['description'].keys():
                if field not in allowed_description_fields:
                    self.warnings.append(
                        f"Field 'description.{field}' is not in schema - consider removing or updating schema.yaml"
                    )

            desc_required = ['overview', 'how_it_works', 'use_cases', 'category']
            for field in desc_required:
                if field not in data['description']:
                    self.errors.append(f"Missing required description field: '{field}'")

            # Validate how_it_works structure
            if 'how_it_works' in data['description']:
                how_it_works = data['description']['how_it_works']
                if isinstance(how_it_works, dict):
                    # Check for extra how_it_works fields
                    for field in how_it_works.keys():
                        if field not in allowed_how_it_works_fields:
                            self.warnings.append(
                                f"Field 'description.how_it_works.{field}' is not in schema - consider removing or updating schema.yaml"
                            )

                    if 'configuration_requirements' not in how_it_works:
                        self.errors.append("Missing 'configuration_requirements' in how_it_works")
                    if 'execution_flow' not in how_it_works:
                        self.errors.append("Missing 'execution_flow' in how_it_works")

        # Validate expert_prompts exists (can be empty dict)
        if 'expert_prompts' not in data:
            self.errors.append("Missing field: 'expert_prompts' (use {} if empty)")

    def _validate_formatting(self, content: str, file_path: Path):
        """Validate general YAML formatting issues."""
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for tabs (should use spaces)
            if '\t' in line and not line.strip().startswith('#'):
                self.warnings.append(f"Line {i}: Contains tab character (use spaces for indentation)")

            # Check for trailing whitespace
            if line.rstrip() != line and line.strip():
                self.warnings.append(f"Line {i}: Trailing whitespace detected")

            # Check for mixed indentation (spaces after content)
            if line.strip() and '  ' in line and not line.strip().startswith('#'):
                # Verify consistent indentation (multiples of 2)
                leading_spaces = len(line) - len(line.lstrip(' '))
                if leading_spaces % 2 != 0:
                    self.warnings.append(f"Line {i}: Inconsistent indentation (use multiples of 2 spaces)")

    def _validate_string_quoting(self, content: str, file_path: Path):
        """Validate string quoting and escape sequences."""
        lines = content.split('\n')
        in_literal_block = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip comments and empty lines
            if stripped.startswith('#') or not stripped:
                continue

            # Check if we're entering or in a literal block (|)
            if ':' in line and '|' in line.split(':', 1)[1].strip():
                in_literal_block = True
                continue

            # Check if we've exited the literal block (line at same or lower indentation level as the key with |)
            if in_literal_block:
                # If line starts with a non-whitespace character at column 0, we've exited
                if line and not line[0].isspace():
                    in_literal_block = False
                else:
                    # We're still in the literal block, skip all validation
                    continue

            # Check for list items with mismatched quotes
            if stripped.startswith('- '):
                list_value = stripped[2:].strip()

                # Check for mismatched quotes - ends with quote but doesn't start with one
                if list_value.endswith('"') and not list_value.startswith('"'):
                    self.errors.append(f"Line {i}: List item ends with quote but doesn't start with quote - mismatched quotation")
                elif list_value.endswith("'") and not list_value.startswith("'"):
                    self.errors.append(f"Line {i}: List item ends with quote but doesn't start with quote - mismatched quotation")

                # Check for starts with quote but doesn't end with matching quote
                if list_value.startswith('"') and not list_value.endswith('"'):
                    self.errors.append(f"Line {i}: List item starts with quote but doesn't end with quote - unclosed quotation")
                elif list_value.startswith("'") and not list_value.endswith("'"):
                    self.errors.append(f"Line {i}: List item starts with quote but doesn't end with quote - unclosed quotation")

            # Check for unescaped quotes in quoted strings
            # Pattern: key: "value with "unescaped" quotes"
            if ':' in stripped:
                key_value = stripped.split(':', 1)
                if len(key_value) == 2:
                    value = key_value[1].strip()

                    # Check for mismatched quotes in key-value pairs
                    if value.endswith('"') and not value.startswith('"'):
                        self.errors.append(f"Line {i}: Value ends with quote but doesn't start with quote - mismatched quotation")
                    elif value.endswith("'") and not value.startswith("'"):
                        self.errors.append(f"Line {i}: Value ends with quote but doesn't start with quote - mismatched quotation")

                    if value.startswith('"') and not value.endswith('"'):
                        self.errors.append(f"Line {i}: Value starts with quote but doesn't end with quote - unclosed quotation")
                    elif value.startswith("'") and not value.endswith("'"):
                        self.errors.append(f"Line {i}: Value starts with quote but doesn't end with quote - unclosed quotation")

                    # Check for improperly escaped quotes in double-quoted strings
                    if value.startswith('"') and value.endswith('"') and len(value) > 1:
                        inner = value[1:-1]
                        # Check for unescaped double quotes
                        if '"' in inner.replace('\\"', ''):
                            self.errors.append(f"Line {i}: Unescaped double quotes in string")

                    # Check for improperly escaped quotes in single-quoted strings
                    if value.startswith("'") and value.endswith("'") and len(value) > 1:
                        inner = value[1:-1]
                        # In YAML, single quotes escape by doubling: ''
                        if "'" in inner and "''" not in inner:
                            # Check if there are unpaired single quotes
                            single_quotes = [m.start() for m in re.finditer("'", inner)]
                            if len(single_quotes) % 2 != 0:
                                self.errors.append(f"Line {i}: Improperly escaped single quotes (use '' to escape)")

            # Check for common escape sequence issues
            if '\\n' in stripped and not ('"""' in stripped or "'''" in stripped):
                # Could be intentional, but worth checking if it's in quotes
                if '"' not in stripped and "'" not in stripped:
                    self.warnings.append(f"Line {i}: Found \\n outside of quoted string - may not be interpreted as intended")

    def _validate_special_characters(self, content: str, file_path: Path):
        """Validate handling of special YAML characters."""
        lines = content.split('\n')

        # Special characters that have meaning in YAML
        special_chars = {
            ':': 'colon (key-value separator)',
            '#': 'hash (comment indicator)',
            '|': 'pipe (literal block scalar)',
            '>': 'greater than (folded block scalar)',
            '-': 'dash (list item)',
            '&': 'ampersand (anchor)',
            '*': 'asterisk (alias)',
            '!': 'exclamation (tag)',
            '%': 'percent (directive)',
            '@': 'at sign',
            '`': 'backtick'
        }

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip comments
            if stripped.startswith('#') or not stripped:
                continue

            # Check for unquoted strings with special characters
            if ':' in stripped:
                key_value = stripped.split(':', 1)
                if len(key_value) == 2:
                    value = key_value[1].strip()

                    # Skip if already quoted or is a YAML structure indicator
                    if value and not value.startswith(('"', "'", '[', '{', '|', '>', '-')):
                        # Check for special chars in unquoted value
                        for char, desc in special_chars.items():
                            if char in value and char != '-':  # Allow hyphens in unquoted strings
                                self.warnings.append(
                                    f"Line {i}: Unquoted value contains special character '{char}' ({desc}) - consider quoting"
                                )
                                break

    def _validate_field_types(self, data: Dict, file_path: Path):
        """Validate that fields have the correct data types."""
        if data is None:
            return

        # Check field types
        type_checks = {
            'version': str,
            'agent_name': str,
            'builder': str,
            'system_prompt': str,
            'description': dict,
            'supported_experts': list,
            'expert_prompts': dict
        }

        for field, expected_type in type_checks.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    self.errors.append(
                        f"Field '{field}' has incorrect type: expected {expected_type.__name__}, "
                        f"got {type(data[field]).__name__}"
                    )

        # Check nested types in description
        if 'description' in data and isinstance(data['description'], dict):
            desc = data['description']

            if 'overview' in desc and not isinstance(desc['overview'], str):
                self.errors.append("Field 'description.overview' must be a string")

            if 'use_cases' in desc and not isinstance(desc['use_cases'], list):
                self.errors.append("Field 'description.use_cases' must be a list")

            if 'category' in desc and not isinstance(desc['category'], str):
                self.errors.append("Field 'description.category' must be a string")

            if 'how_it_works' in desc and isinstance(desc['how_it_works'], dict):
                how_it_works = desc['how_it_works']

                if 'configuration_requirements' in how_it_works:
                    if not isinstance(how_it_works['configuration_requirements'], list):
                        self.errors.append("Field 'how_it_works.configuration_requirements' must be a list")

                if 'execution_flow' in how_it_works:
                    if not isinstance(how_it_works['execution_flow'], list):
                        self.errors.append("Field 'how_it_works.execution_flow' must be a list")

    def _validate_field_values(self, data: Dict, file_path: Path):
        """Validate specific field value constraints."""
        if data is None:
            return

        # Validate version format (should be semantic versioning)
        if 'version' in data:
            version = data['version']
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                self.warnings.append(
                    f"Version '{version}' does not follow semantic versioning (e.g., '1.0.0')"
                )

        # Validate that lists are not empty where they shouldn't be
        if 'supported_experts' in data:
            if isinstance(data['supported_experts'], list) and len(data['supported_experts']) == 0:
                self.warnings.append("Field 'supported_experts' is empty - is this intentional?")

        if 'description' in data and isinstance(data['description'], dict):
            desc = data['description']

            if 'use_cases' in desc:
                if isinstance(desc['use_cases'], list) and len(desc['use_cases']) == 0:
                    self.warnings.append("Field 'use_cases' is empty - is this intentional?")

            if 'how_it_works' in desc and isinstance(desc['how_it_works'], dict):
                how = desc['how_it_works']

                if 'configuration_requirements' in how:
                    if isinstance(how['configuration_requirements'], list) and len(how['configuration_requirements']) == 0:
                        self.warnings.append("Field 'configuration_requirements' is empty")

                if 'execution_flow' in how:
                    if isinstance(how['execution_flow'], list) and len(how['execution_flow']) == 0:
                        self.warnings.append("Field 'execution_flow' is empty")

        # Validate system_prompt is not empty
        if 'system_prompt' in data:
            if isinstance(data['system_prompt'], str) and len(data['system_prompt'].strip()) == 0:
                self.errors.append("Field 'system_prompt' cannot be empty")

    def _validate_quotation_best_practices(self, content: str, file_path: Path):
        """Validate quotation usage follows YAML best practices."""
        lines = content.split('\n')
        in_literal_block = False
        literal_block_indent = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip comments and empty lines
            if stripped.startswith('#') or not stripped:
                continue

            # Track literal blocks
            if ':' in line and '|' in line.split(':', 1)[1].strip():
                in_literal_block = True
                # Store the indentation level of the key that started the literal block
                literal_block_indent = len(line) - len(line.lstrip())
                continue

            if in_literal_block:
                # Exit if we hit a non-whitespace character at column 0
                if line and not line[0].isspace():
                    in_literal_block = False
                # Exit if we find a key at the same or less indentation than the literal block key
                elif ':' in line and not stripped.startswith('-'):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= literal_block_indent:
                        in_literal_block = False
                else:
                    # Still in literal block, skip validation
                    continue

            # Check for unnecessary quotes in simple values
            if ':' in stripped and not stripped.startswith('-'):
                parts = stripped.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    # Check if value is unnecessarily quoted
                    if value.startswith('"') and value.endswith('"') and len(value) > 2:
                        inner_value = value[1:-1]

                        # Check if quotes are unnecessary (no spaces, no special chars, not a number-like string)
                        needs_quotes = False

                        # Check for spaces
                        if ' ' in inner_value:
                            needs_quotes = True

                        # Check for special YAML characters
                        special_chars = [':', '#', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', '[', ']', '{', '}', ',']
                        for char in special_chars:
                            if char in inner_value:
                                needs_quotes = True
                                break

                        # Check if it starts with special chars
                        if inner_value and inner_value[0] in ['-', '?', ':', '|', '>', '&', '*', '!']:
                            needs_quotes = True

                        # If quotes not needed, warn
                        if not needs_quotes and inner_value:
                            self.warnings.append(
                                f"Line {i}: Unnecessary quotes around '{inner_value}' - remove for cleaner YAML"
                            )

            # Check for unnecessarily quoted list items
            if stripped.startswith('- '):
                list_value = stripped[2:].strip()

                if list_value.startswith('"') and list_value.endswith('"') and len(list_value) > 2:
                    inner_value = list_value[1:-1]

                    needs_quotes = False

                    # Check for spaces
                    if ' ' in inner_value:
                        needs_quotes = True

                    # Check for special YAML characters (hyphens in middle are OK)
                    special_chars = [':', '#', '&', '*', '?', '|', '<', '>', '=', '!', '%', '@', '`', '[', ']', '{', '}', ',']
                    for char in special_chars:
                        if char in inner_value:
                            needs_quotes = True
                            break

                    # Check if it starts with special chars (including hyphen at start)
                    if inner_value and inner_value[0] in ['-', '?', ':', '|', '>', '&', '*', '!']:
                        needs_quotes = True

                    if not needs_quotes and inner_value:
                        self.warnings.append(
                            f"Line {i}: Unnecessary quotes around list item '{inner_value}' - remove for cleaner YAML"
                        )

    def _validate_readability(self, content: str, data: Dict, file_path: Path):
        """Validate readability best practices based on medical-coding.yaml standards."""
        lines = content.split('\n')

        # Check for long single-line strings that should use literal block scalars
        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip comments and empty lines
            if stripped.startswith('#') or not stripped:
                continue

            # Check for very long quoted strings (> 120 characters)
            if ':' in stripped and not stripped.startswith('-'):
                parts = stripped.split(':', 1)
                if len(parts) == 2:
                    value = parts[1].strip()

                    # Check if it's a quoted string
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        if len(value) > 120:
                            key = parts[0].strip()
                            self.warnings.append(
                                f"Line {i}: Long string in '{key}' ({len(value)} chars) - consider using literal block scalar (|) for better readability"
                            )

        # Check for long overview or system_prompt without literal block scalar
        if data and isinstance(data, dict):
            if 'description' in data and isinstance(data['description'], dict):
                overview = data['description'].get('overview', '')
                if isinstance(overview, str) and len(overview) > 200:
                    # Check if it's using literal block scalar
                    found_literal = False
                    for i, line in enumerate(lines, 1):
                        if 'overview:' in line and '|' in line:
                            found_literal = True
                            break

                    if not found_literal:
                        self.warnings.append(
                            "Field 'description.overview' is long - consider using literal block scalar (|) for better readability"
                        )

            if 'system_prompt' in data:
                system_prompt = data['system_prompt']
                if isinstance(system_prompt, str) and len(system_prompt) > 200:
                    # Check if it's using literal block scalar
                    found_literal = False
                    for i, line in enumerate(lines, 1):
                        if 'system_prompt:' in line and '|' in line:
                            found_literal = True
                            break

                    if not found_literal:
                        self.warnings.append(
                            "Field 'system_prompt' is long - consider using literal block scalar (|) for better readability"
                        )

        # Check for list items that are very long (should potentially be split)
        # Skip items inside literal blocks as they may be naturally long
        in_literal_block = False
        literal_block_indent = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Track literal blocks
            if ':' in line and '|' in line.split(':', 1)[1].strip():
                in_literal_block = True
                literal_block_indent = len(line) - len(line.lstrip())
                continue

            if in_literal_block:
                if line and not line[0].isspace():
                    in_literal_block = False
                elif ':' in line and not stripped.startswith('-'):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= literal_block_indent:
                        in_literal_block = False

            # Only check list items outside literal blocks
            if not in_literal_block and stripped.startswith('- '):
                list_value = stripped[2:].strip()
                # Remove quotes if present
                if (list_value.startswith('"') and list_value.endswith('"')) or \
                   (list_value.startswith("'") and list_value.endswith("'")):
                    list_value = list_value[1:-1]

                if len(list_value) > 100:
                    self.warnings.append(
                        f"Line {i}: Long list item ({len(list_value)} chars) - consider breaking into multiple items or using different structure"
                    )

        # Check for proper use of multiline strings in description fields
        if data and isinstance(data, dict):
            if 'description' in data and isinstance(data['description'], dict):
                desc = data['description']

                # Check overview structure
                if 'overview' in desc:
                    overview = desc['overview']
                    if isinstance(overview, str) and len(overview) > 300:
                        # Check if it has paragraph breaks (good practice)
                        if '\n\n' not in overview:
                            self.warnings.append(
                                "Field 'description.overview' is long without paragraph breaks - consider adding blank lines for readability"
                            )

    def _print_results(self):
        """Print validation results."""
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All checks passed!")
        elif not self.errors:
            print("\n✅ No errors (warnings can be reviewed)")


def main():
    """Main validation function."""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    prompts_dir = project_root / 'prompts'
    schema_path = prompts_dir / 'schema.yaml'

    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'YAML Prompt Validation Tool'.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")

    # Check if schema exists
    if not schema_path.exists():
        print(f"{Colors.RED}Error: Schema file not found at {schema_path}{Colors.ENDC}")
        sys.exit(1)

    # Initialize validator
    validator = PromptValidator(schema_path)

    # Find all YAML files except schema.yaml
    yaml_files = [
        f for f in prompts_dir.glob('*.yaml')
        if f.name != 'schema.yaml'
    ]

    if not yaml_files:
        print(f"\n{Colors.YELLOW}No YAML files found in {prompts_dir}{Colors.ENDC}")
        return

    print(f"\n{Colors.BOLD}Found {len(yaml_files)} prompt file(s) to validate{Colors.ENDC}\n")

    # Validate each file
    results = {}
    for yaml_file in yaml_files:
        passed = validator.validate_file(str(yaml_file))
        results[yaml_file.name] = passed

    # Print summary
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'VALIDATION SUMMARY'.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

    passed_count = sum(1 for v in results.values() if v)
    failed_count = len(results) - passed_count

    for filename, passed in results.items():
        if passed:
            status = f"{Colors.GREEN}✅ PASSED{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌ FAILED{Colors.ENDC}"
        print(f"{status}: {Colors.BOLD}{filename}{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Total: {len(results)} files | "
          f"{Colors.GREEN}Passed: {passed_count}{Colors.ENDC} | "
          f"{Colors.RED}Failed: {failed_count}{Colors.ENDC}")

    # Exit with appropriate code
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == '__main__':
    main()
