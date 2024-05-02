# macOS/Homebrew

Ansible installed via Homebrew has its Python path hard coded, so if you want to use a Virtual Environment, you'll need to install Ansible via pip in that environment:

```
$ head -n 1 $(which ansible)
#!/opt/homebrew/Cellar/ansible/9.3.0/libexec/bin/python
```

# Setup instructions

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install black==22.3.0 autoflake jsonschema jinja2==3.0.3 ansible boto3 baron redbaron ruamel_yaml

$ mkdir -p ./collections/ansible_collections/
$ ansible-galaxy collection install git+https://github.com/ansible-community/ansible.content_builder.git

# These steps ensure ansible-playbook from the venv is on the path
$ deactivate
$ source .venv/bin/activate

$ mkdir -p ./collections/ansible_collections/amazon/cloud

$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install

$ aws configure
AWS Access Key ID [None]: xxx
AWS Secret Access Key [None]: xxx
Default region name [None]: us-east-1
Default output format [None]:
```
# To auto-generate modules.yaml:

```
$ aws cloudformation list-types --visibility PUBLIC --type RESOURCE --query "TypeSummaries[*].[TypeName,Description]" --output json > types.json
$ aws cloudformation list-types --visibility PUBLIC --type RESOURCE --query "TypeSummaries[?contains(TypeName, 'EC2')].[TypeName,Description]" --output json > types.json
$ ./create_modulesyaml.py
$ mkdir config api_specifications
$ cp modules.yaml config
```

# To generate the collection:
```
$ ansible-playbook -i hosts build.yaml -e manifest_file=MANIFEST.yaml
```
