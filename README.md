# YAML-to-MD

A Sphinx directive for rendering YAML data as Markdown.

## Installation

```
$ pip install git+https://github.com/elastic/markitpy.extensions.yaml-to-md
```

## Configuration

Add yaml-to-md to the extensions list in conf.py

```
extensions = [
    ...
    markitpy.extensions.yaml_to_md
]
```

## Usage

The syntax of this directive is:

```
    ```{yaml_to_md}
    :yaml: <yaml_filepath>
    :template: <template_filepath>
    ```
```

The filepaths are relative to 'docs/source'. For example:

```
    ```{yaml_to_md}
    :yaml: _static/yaml/some-yaml.yaml
    :template: _static/templates/some-template.jinja
    ```
```

## Template Syntax

This directive uses Jinja as its templating engine.

> https://jinja.palletsprojects.com