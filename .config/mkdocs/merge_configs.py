import yaml
from pathlib import Path


# Use UnsafeLoader to handle custom tags
def load_yaml(path):
    text = path.read_text()
    # Replace custom tags
    text = text.replace("!ENV", "")
    text = text.replace("!!python/name:", "")
    return yaml.safe_load(text)


# Read all config files
config_dir = Path("C:/global/docker/.config/mkdocs")
base = load_yaml(config_dir / "base.yml")
theme = load_yaml(config_dir / "theme.yml")
plugins = load_yaml(config_dir / "plugins.yml")
markdown = load_yaml(config_dir / "markdown.yml")
hooks = load_yaml(config_dir / "hooks.yml")

# Create consolidated config
merged = {
    "site_name": "Docker Modern Data Platform",
    "site_description": "Production-grade Docker orchestration platform",
    "site_author": "Dean Luus",
    "site_url": "http://localhost:8000",
    "repo_name": "DeanLuus22021994/docker_dotfiles",
    "repo_url": "https://github.com/DeanLuus22021994/docker_dotfiles",
    "edit_uri": "edit/feat/remaining-todos/docs/",
    "copyright": "Copyright © 2025 Dean Luus",
    "strict": True,
    "use_directory_urls": True,
    "docs_dir": "../../docs",
    "site_dir": "site",
    "dev_addr": "0.0.0.0:8000",
    "watch": [".", "../../docs"],
}

# Merge all sections
merged.update(theme)
merged["extra"] = base.get("extra", {})
merged["validation"] = base.get("validation", {})
merged.update(plugins)
merged.update(markdown)
merged.update(hooks)

# Write
(config_dir / "mkdocs.yml").write_text(
    yaml.dump(merged, default_flow_style=False, sort_keys=False, width=120)
)
print("✅ Consolidated mkdocs.yml created")
