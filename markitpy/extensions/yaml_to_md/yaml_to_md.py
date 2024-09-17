import yaml
import jinja2
from markitpy.extensions.yaml_to_md import __version__
from pathlib import Path
from docutils import nodes, frontend
from docutils.utils import new_document
from sphinx.application import Sphinx
from sphinx.util import logging as sphinx_logging
from sphinx.util.console import bold
from sphinx.util.docutils import SphinxDirective, directives
from sphinx.util.typing import ExtensionMetadata
from myst_parser.parsers.docutils_ import Parser

class YamlToMdDirective(SphinxDirective):
    """A directive to turn YAML to markdown!"""

    YAML_FILE_OPTION = 'yaml'
    TEMPLATE_FILE_OPTION = 'template'
    optional_arguments = 2
    option_spec = {
        'yaml': directives.unchanged,
        'template': directives.unchanged
    }

    def check_options(self) -> None:
        """Check if the directive has the required options."""
        if YamlToMdDirective.YAML_FILE_OPTION not in self.options:
            raise ValueError(f"yaml_markdown directive requires an option: {self.YAML_FILE_OPTION}")
        if YamlToMdDirective.TEMPLATE_FILE_OPTION not in self.options:  
            raise ValueError(f"yaml_markdown directive requires an option: {self.TEMPLATE_FILE_OPTION}")    

    def read_yaml(self, yaml_filepath: str) -> dict:
        """Parse a YAML file and return the data"""
        with open(yaml_filepath) as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ValueError(f"Error parsing YAML file: {yaml_filepath}") from exc

    def render_template(self, template_filepath: Path, yaml_data: dict) -> str:
        """Render a Jinja2 template with the YAML data."""
        template_dir = template_filepath.parent
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        template_filename = template_filepath.name
        template = env.get_template(template_filename)
        mdOutput =  template.render(**yaml_data)
        return mdOutput

    def create_document(self) -> nodes.document:
        """Create a new document for passing to the myst parser."""
        settings = frontend.get_default_settings(Parser)
        settings.env = self.env
        document = new_document('', settings)
        return document

    def parse_md(self, mdOutput: str) -> list[nodes.Node]:
        """Parse the markdown output with the myst parser."""       
        document = self.create_document()
        mystParser = Parser()
        mystParser.parse(mdOutput, document)
        return document.children

    def get_file_path(self, file_rel_path: str) -> str:
        """Get the full file path from the docs/source directory."""
        return Path('docs/source', file_rel_path).resolve()

    def run(self) -> list[nodes.Node]:
        """Run the directive."""        
        self.check_options()
        # Get the YAML and template file paths from the directive options
        yaml_rel_filepath = self.options[self.YAML_FILE_OPTION]
        template_rel_filepath = self.options[self.TEMPLATE_FILE_OPTION]
        # The YAML and template file paths are relative to the 
        # docs/source directory. Get the full file paths.
        yaml_filepath = self.get_file_path(yaml_rel_filepath)
        template_filepath = self.get_file_path(template_rel_filepath)
        # Parse the YAML file and render the template
        yaml_data = self.read_yaml(yaml_filepath)
        mdOutput = self.render_template(template_filepath, yaml_data)   
        # Since the markdown file is dynamically generated, it is not
        # parsed by Sphinx. We need to parse it ourseleves with the
        # myst parser.
        nodes = self.parse_md(mdOutput)
        return nodes

def print_version() -> None:
    """Print the version of the extension."""
    SPHINX_LOGGER = sphinx_logging.getLogger(__name__)
    SPHINX_LOGGER.info(bold("yaml-to-md v%s"), __version__)

def setup(app: Sphinx) -> ExtensionMetadata:
    """Setup the extension."""
    print_version()
    app.add_directive('yaml-to-md', YamlToMdDirective)
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }