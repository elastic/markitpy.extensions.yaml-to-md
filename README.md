# YAML-to-MD

A Sphinx directive for rendering YAML data as Markdown.

## Overview

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

This directive uses Jinja as its templating engine.

> https://jinja.palletsprojects.com