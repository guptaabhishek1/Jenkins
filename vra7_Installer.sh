
#!/bin/bash

export GOPATH=/home/dc-user/TerraformPluginProject
export GOROOT=/usr/local/go

### Initializing the terraform rc files

mkdir -p TerraformPluginProject/bin/
echo "providers { "> ~/.terraformrc
echo 'vra7 = "/home/dc-user/TerraformPluginProject/bin/terraform-provider-vra7" ' >>~/.terraformrc
echo "}" >>~/.terraformrc


### To get the terraform latest package
wget "https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip" >/dev/null
unzip terraform_0.11.10_linux_amd64.zip >/dev/null
sudo mv terraform /usr/local/bin/ >/dev/null

### check if terraform is installed 

if ! which terraform >/dev/null
then 
  echo "Terraform package is not installed"
  exit 1
fi

### Install GO

wget https://dl.google.com/go/go1.11.2.linux-amd64.tar.gz >/dev/null
tar -xvf go1.11.2.linux-amd64.tar.gz >/dev/null
sudo cp go/bin/go /usr/bin/
sudo mv go /usr/local/

### check if go is installed 

if ! which go >/dev/null
then 
  echo "Golang package is not installed"
  exit 1
fi

### Install dep package
curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh
sudo mv TerraformPluginProject/bin/dep /usr/bin/

if ! which dep >/dev/null
then 
  echo "Dep package is not installed"
  exit 1
fi

cd TerraformPluginProject
go get github.com/vmware/terraform-provider-vra7
cd src/github.com/vmware/terraform-provider-vra7/
dep ensure
go build
sudo cp terraform-provider-vra7 /home/dc-user/TerraformPluginProject/bin/
sudo cp terraform-provider-vra7 /usr/local/bin/

if ! which terraform-provider-vra7  >/dev/null
then 
  echo "terraform-provider-vra7 package is missing"
  exit 1
fi
