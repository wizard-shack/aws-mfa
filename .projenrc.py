from projen.python import PythonProject

project = PythonProject(
    author_email="dev.rjhusein3@gmail.com",
    author_name="Rami Husein",
    github=True,
    module_name="aws_mfa",
    name="aws-mfa",
    projenrc_python=True,
    version="0.1.0"
)

project.add_dependency("attrs@>=23.1.0")
project.add_dependency("boto3@>=1.28.29")
project.add_dependency("boto3-stubs@>=1.28.29")
project.add_dependency("botocore@>=1.31.29")
project.add_dependency("botocore-stubs@>=1.31.29")
project.add_dependency("certifi@>=2023.5.7")
project.add_dependency("charset-normalizer@>=3.1.0")
project.add_dependency("click@>=8.1.3")
project.add_dependency("colorama@>=0.4.6")
project.add_dependency("distlib@>=0.3.6")
project.add_dependency("filelock@>=3.12.0")
project.add_dependency("ghp-import@>=2.1.0")
project.add_dependency("idna@>=3.4")
project.add_dependency("Jinja2@>=3.1.2")
project.add_dependency("jmespath@>=1.0.1")
project.add_dependency("jsonschema@>=4.19.0")
project.add_dependency("jsonschema-specifications@>=2023.7.1")
project.add_dependency("Markdown@>=3.3.7")
project.add_dependency("MarkupSafe@>=2.1.2")
project.add_dependency("mergedeep@>=1.3.4")
project.add_dependency("mkdocs@>=1.4.3")
project.add_dependency("mkdocs-material@>=9.1.14")
project.add_dependency("mkdocs-material-extensions@>=1.1.1")
project.add_dependency("mypy-boto3-cloudformation@>=1.28.19")
project.add_dependency("mypy-boto3-dynamodb@>=1.28.27")
project.add_dependency("mypy-boto3-ec2@>=1.28.29")
project.add_dependency("mypy-boto3-lambda@>=1.28.19")
project.add_dependency("mypy-boto3-rds@>=1.28.19")
project.add_dependency("mypy-boto3-s3@>=1.28.27")
project.add_dependency("mypy-boto3-sqs@>=1.28.19")
project.add_dependency("packaging@>=23.1")
project.add_dependency("platformdirs@>=3.5.1")
project.add_dependency("Pygments@>=2.15.1")
project.add_dependency("pymdown-extensions@>=10.0.1")
project.add_dependency("python-dateutil@>=2.8.2")
project.add_dependency("PyYAML@>=6.0.1")
project.add_dependency("pyyaml_env_tag@>=0.1")
project.add_dependency("referencing@>=0.30.2")
project.add_dependency("regex@>=2023.5.5")
project.add_dependency("requests@>=2.31.0")
project.add_dependency("rpds-py@>=0.10.0")
project.add_dependency("s3transfer@>=0.6.2")
project.add_dependency("six@>=1.16.0")
project.add_dependency("types-awscrt@>=0.19.0")
project.add_dependency("types-s3transfer@>=0.6.2")
project.add_dependency("urllib3@>=1.26.16")
project.add_dependency("virtualenv@>=20.23.0")
project.add_dependency("watchdog@>=3.0.0")

project.synth()
