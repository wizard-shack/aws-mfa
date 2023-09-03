from projen.python import PythonProject

project = PythonProject(
    author_email="dev.rjhusein3@gmail.com",
    author_name="Rami Husein",
    github=True,
    module_name="aws_mfa",
    name="aws-mfa",
    projenrc_python=True,
    version="0.1.0",
)

project.synth()