"""JSON-LD Structured Data Generator for MkDocs.

Generates SEO-optimized structured data for documentation pages
following schema.org standards with Docker-specific enhancements.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
import json
import re

from mkdocs.config import Config
from mkdocs.structure.pages import Page


@dataclass
class StructuredDataConfig:
    """Configuration for structured data generation."""

    # Site information
    site_name: str = "Docker Development Environment"
    site_description: str = "Comprehensive Docker development documentation"
    site_url: str = "https://docker-dev.local"
    site_logo: str = "/assets/images/docker-logo.png"

    # Organization details
    organization_name: str = "Docker Dev Team"
    organization_url: str = "https://github.com/docker-dev"
    organization_logo: str = "/assets/images/org-logo.png"

    # Author information
    default_author: str = "Docker Development Team"
    author_url: str = "https://github.com/docker-dev"

    # Content settings
    enable_breadcrumbs: bool = True
    enable_faq: bool = True
    enable_howto: bool = True
    enable_software_application: bool = True

    # Docker-specific schema
    docker_categories: List[str] = field(
        default_factory=lambda: [
            "containerization",
            "orchestration",
            "monitoring",
            "security",
            "networking",
            "storage",
        ]
    )


class JSONLDGenerator:
    """Generates JSON-LD structured data for documentation pages."""

    def __init__(self, config: StructuredDataConfig):
        self.config = config

    def generate_for_page(self, page: Page, config: Config) -> str:
        """Generate complete JSON-LD structured data for a page."""

        structured_data = {"context": "https://schema.org", "graph": []}

        # Base article/documentation schema
        article_schema = self._generate_article_schema(page, config)
        structured_data["graph"].append(article_schema)

        # Website schema
        website_schema = self._generate_website_schema(config)
        structured_data["graph"].append(website_schema)

        # Organization schema
        org_schema = self._generate_organization_schema()
        structured_data["graph"].append(org_schema)

        # Breadcrumb schema
        if self.config.enable_breadcrumbs:
            breadcrumb_schema = self._generate_breadcrumb_schema(page)
            if breadcrumb_schema:
                structured_data["graph"].append(breadcrumb_schema)

        # Content-specific schemas
        content_schemas = self._generate_content_specific_schemas(page)
        structured_data["graph"].extend(content_schemas)

        # Docker-specific software application schema
        if self.config.enable_software_application:
            software_schema = self._generate_software_schema(page)
            if software_schema:
                structured_data["graph"].append(software_schema)

        return json.dumps(structured_data, indent=2, ensure_ascii=False)

    def _generate_article_schema(self, page: Page, config: Config) -> Dict[str, Any]:
        """Generate article schema for documentation page."""

        # Extract metadata
        meta = page.meta
        title = page.title or "Documentation"
        description = meta.get("description", "")

        # Determine article type
        article_type = self._determine_article_type(page, meta)

        schema = {
            "@type": article_type,
            "@id": f"{self.config.site_url}{page.url}#article",
            "headline": title,
            "name": title,
            "url": f"{self.config.site_url}{page.url}",
            "datePublished": self._get_publish_date(meta),
            "dateModified": self._get_modified_date(meta, page),
            "author": self._generate_author_schema(meta),
            "publisher": {
                "@type": "Organization",
                "name": self.config.organization_name,
                "url": self.config.organization_url,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{self.config.site_url}{self.config.organization_logo}",
                },
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"{self.config.site_url}{page.url}"},
        }

        # Add description if available
        if description:
            schema["description"] = description
            schema["abstract"] = description

        # Add keywords/tags
        if "tags" in meta:
            schema["keywords"] = meta["tags"]

        # Add category
        if "category" in meta:
            schema["articleSection"] = meta["category"]

        # Add difficulty level for tutorials
        if "difficulty" in meta:
            schema["educationalLevel"] = meta["difficulty"]

        # Add estimated reading time
        if "reading_time" in meta:
            schema["timeRequired"] = f"PT{meta['reading_time']}M"

        return schema

    def _determine_article_type(self, page: Page, meta: Dict) -> str:
        """Determine the most appropriate schema.org article type."""

        category = meta.get("category", "").lower()
        title = page.title.lower()
        content = getattr(page, "content", "").lower()

        # Check for specific patterns
        if any(
            word in title or word in content
            for word in ["tutorial", "guide", "how to", "walkthrough"]
        ):
            return "HowTo"
        elif any(word in title or word in content for word in ["faq", "question", "answer"]):
            return "FAQPage"
        elif category in ["api", "reference"]:
            return "APIReference"
        elif category in ["troubleshooting", "debugging"]:
            return "TroubleshootingGuide"
        elif any(word in title for word in ["news", "update", "release"]):
            return "NewsArticle"
        else:
            return "TechnicalArticle"

    def _generate_website_schema(self, config: Config) -> Dict[str, Any]:
        """Generate website schema."""

        return {
            "@type": "WebSite",
            "@id": f"{self.config.site_url}#website",
            "name": self.config.site_name,
            "description": self.config.site_description,
            "url": self.config.site_url,
            "publisher": {"@type": "Organization", "name": self.config.organization_name},
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{self.config.site_url}/search/?q={{search_term_string}}",
                },
                "query-input": "required name=search_term_string",
            },
        }

    def _generate_organization_schema(self) -> Dict[str, Any]:
        """Generate organization schema."""

        return {
            "@type": "Organization",
            "@id": f"{self.config.organization_url}#organization",
            "name": self.config.organization_name,
            "url": self.config.organization_url,
            "logo": {
                "@type": "ImageObject",
                "url": f"{self.config.site_url}{self.config.organization_logo}",
            },
            "sameAs": [
                f"{self.config.organization_url}",
                f"https://github.com/{self.config.organization_name.lower().replace(' ', '-')}",
            ],
        }

    def _generate_breadcrumb_schema(self, page: Page) -> Optional[Dict[str, Any]]:
        """Generate breadcrumb navigation schema."""

        if not hasattr(page, "ancestors") or not page.ancestors:
            return None

        breadcrumb_items = []
        position = 1

        # Add home
        breadcrumb_items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": "Home",
                "item": self.config.site_url,
            }
        )
        position += 1

        # Add ancestors
        for ancestor in page.ancestors:
            breadcrumb_items.append(
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": ancestor.title,
                    "item": f"{self.config.site_url}{ancestor.url}",
                }
            )
            position += 1

        # Add current page
        breadcrumb_items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": page.title,
                "item": f"{self.config.site_url}{page.url}",
            }
        )

        return {
            "@type": "BreadcrumbList",
            "@id": f"{self.config.site_url}{page.url}#breadcrumb",
            "itemListElement": breadcrumb_items,
        }

    def _generate_content_specific_schemas(self, page: Page) -> List[Dict[str, Any]]:
        """Generate content-specific schemas based on page content."""

        schemas = []
        content = getattr(page, "content", "")
        meta = page.meta

        # FAQ schema
        if self.config.enable_faq:
            faq_schema = self._extract_faq_schema(content)
            if faq_schema:
                schemas.append(faq_schema)

        # HowTo schema
        if self.config.enable_howto:
            howto_schema = self._extract_howto_schema(content, meta)
            if howto_schema:
                schemas.append(howto_schema)

        # Code example schema
        code_schema = self._extract_code_schema(content, page)
        if code_schema:
            schemas.append(code_schema)

        return schemas

    def _extract_faq_schema(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract FAQ schema from content."""

        # Look for FAQ patterns in markdown
        faq_pattern = r"#{2,4}\s*(.+\?)\s*\n\n*(.+?)(?=\n#{2,4}|\n*$)"
        matches = re.findall(faq_pattern, content, re.MULTILINE | re.DOTALL)

        if not matches:
            return None

        faq_items = []
        for question, answer in matches:
            # Clean up the answer text
            answer = re.sub(r"\n+", " ", answer.strip())
            answer = re.sub(r"\s+", " ", answer)

            faq_items.append(
                {
                    "@type": "Question",
                    "name": question.strip(),
                    "acceptedAnswer": {"@type": "Answer", "text": answer},
                }
            )

        return {"@type": "FAQPage", "@id": "#faq", "mainEntity": faq_items}

    def _extract_howto_schema(self, content: str, meta: Dict) -> Optional[Dict[str, Any]]:
        """Extract HowTo schema from content."""

        # Look for numbered steps or step patterns
        step_patterns = [
            r"(?:^|\n)#{2,4}\s*(?:Step\s*)?(\d+)[\.\)]\s*(.+?)(?=\n#{2,4}|\n*$)",
            r"(?:^|\n)(\d+)\.\s*(.+?)(?=\n\d+\.|\n*$)",
        ]

        steps = []
        for pattern in step_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            if matches:
                for step_num, step_text in matches:
                    step_text = re.sub(r"\n+", " ", step_text.strip())
                    step_text = re.sub(r"\s+", " ", step_text)

                    steps.append(
                        {
                            "@type": "HowToStep",
                            "position": int(step_num),
                            "name": f"Step {step_num}",
                            "text": step_text,
                        }
                    )
                break

        if not steps:
            return None

        howto_schema = {
            "@type": "HowTo",
            "@id": "#howto",
            "name": meta.get("title", "How-to Guide"),
            "step": sorted(steps, key=lambda x: x["position"]),
        }

        # Add additional properties
        if "description" in meta:
            howto_schema["description"] = meta["description"]

        if "difficulty" in meta:
            howto_schema["difficulty"] = meta["difficulty"]

        if "time_required" in meta:
            howto_schema["totalTime"] = f"PT{meta['time_required']}M"

        return howto_schema

    def _extract_code_schema(self, content: str, page: Page) -> Optional[Dict[str, Any]]:
        """Extract code example schema."""

        # Find code blocks
        code_pattern = r"`(\w+)?\n(.*?)\n`"
        matches = re.findall(code_pattern, content, re.DOTALL)

        if not matches:
            return None

        code_examples = []
        for i, (language, code) in enumerate(matches):
            example = {
                "@type": "SoftwareSourceCode",
                "name": f"Code Example {i + 1}",
                "text": code.strip(),
                "programmingLanguage": language if language else "text",
                "codeRepository": self.config.organization_url,
            }
            code_examples.append(example)

        return {
            "@type": "CreativeWork",
            "@id": "#code-examples",
            "name": f"{page.title} - Code Examples",
            "hasPart": code_examples,
        }

    def _generate_software_schema(self, page: Page) -> Optional[Dict[str, Any]]:
        """Generate software application schema for Docker-related content."""

        meta = page.meta
        category = meta.get("category", "").lower()
        tags = [tag.lower() for tag in meta.get("tags", [])]

        # Check if this is Docker-related content
        docker_keywords = ["docker", "container", "dockerfile", "compose", "swarm", "kubernetes"]
        if not any(
            keyword in category or any(keyword in tag for tag in tags)
            for keyword in docker_keywords
        ):
            return None

        return {
            "@type": "SoftwareApplication",
            "@id": "#docker-software",
            "name": "Docker",
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": ["Linux", "Windows", "macOS"],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "downloadUrl": "https://docker.com/get-started",
            "softwareVersion": "latest",
            "description": "Platform for developing, shipping, and running applications in containers",
        }

    def _generate_author_schema(self, meta: Dict) -> Dict[str, Any]:
        """Generate author schema from metadata."""

        author_name = meta.get("author", self.config.default_author)

        return {
            "@type": "Person",
            "name": author_name,
            "url": meta.get("author_url", self.config.author_url),
        }

    def _get_publish_date(self, meta: Dict) -> str:
        """Extract publish date from metadata."""

        date_str = meta.get("date", meta.get("created", ""))
        if date_str:
            try:
                # Try to parse various date formats
                from dateutil.parser import parse

                parsed_date = parse(date_str)
                return parsed_date.isoformat()
            except (ImportError, ValueError):
                pass

        # Fallback to current date
        return datetime.now(timezone.utc).isoformat()

    def _get_modified_date(self, meta: Dict, page: Page) -> str:
        """Extract modified date from metadata or file stats."""

        modified_str = meta.get("modified", meta.get("updated", ""))
        if modified_str:
            try:
                from dateutil.parser import parse

                parsed_date = parse(modified_str)
                return parsed_date.isoformat()
            except (ImportError, ValueError):
                pass

        # Try to get file modification time
        if hasattr(page, "file") and page.file:
            try:
                file_path = Path(page.file.abs_src_path)
                if file_path.exists():
                    mtime = file_path.stat().st_mtime
                    return datetime.fromtimestamp(mtime, timezone.utc).isoformat()
            except (AttributeError, OSError):
                pass

        # Fallback to publish date
        return self._get_publish_date(meta)


def generate_jsonld_for_page(
    page: Page, config: Config, structured_config: Optional[StructuredDataConfig] = None
) -> str:
    """Main function to generate JSON-LD for a page."""

    if structured_config is None:
        structured_config = StructuredDataConfig()

    generator = JSONLDGenerator(structured_config)
    return generator.generate_for_page(page, config)


# Template for embedding in HTML
JSONLD_TEMPLATE = """<script type="application/ld+json">
{jsonld_data}
</script>"""


def embed_jsonld_in_html(html_content: str, jsonld_data: str) -> str:
    """Embed JSON-LD data into HTML content."""

    jsonld_script = JSONLD_TEMPLATE.format(jsonld_data=jsonld_data)

    # Insert before closing </head> tag
    if "</head>" in html_content:
        html_content = html_content.replace("</head>", f"    {jsonld_script}\n</head>")
    else:
        # Fallback: insert at the beginning of <body>
        html_content = html_content.replace("<body>", f"<body>\n    {jsonld_script}")

    return html_content
