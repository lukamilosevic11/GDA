# GDA - Gene Disease Annotation :microbe:

![GDA](gda_first_page.png)

# What is this? :book:
Web Application for creation of annotation file where data is used from different
sources. Annotation file contains gene disease connections and also additional information for genes and diseases from another sources.  
This is project for my master thesis and app will be used at the [Vinča Institute of Nuclear Sciences, National Institute of The Republic of Serbia](https://www.vin.bg.ac.rs/en/).
You can see example of this application on [YouTube](https://www.youtube.com/watch?v=n99pI8E5tTQ).

# Requirements :wrench: 
- `Docker`
- `Docker Compose`
- `Docker Volume`
<br>To be able to start this application on your computer, you should have installed `Windows`, `Linux` or `MacOS` operating system and listed Docker tools. 
Required Docker tools can be installed by following instructions on official [Docker website](https://www.docker.com/). 

# How to run application? :rocket:
Application will be delivered as compressed file [GDA.zip](./GDA.zip) which contains directory with all necessary files for starting application.
<br>Structure of compressed file:
```
GDA.zip
 └───── GDA
        ├── GDA.bat
        ├── GDA.sh
        ├── Storage
        │   ├── error_log.txt
        │   ├── annotation_file.txt
        │   ├── doid_accuracy.txt
        │   ├── disease_name_doid.jsonl
        │   └── data_filenames.json
        └── gda-compose.yml
```

There is a two script files for running application, depending on the operating system:
- `Windows` - short type
```shell
GDA.bat -u
```

- `Linux` and `MacOS` - long type
```shell
./GDA.sh -up
```
These scripts have two types of arguments, long and short, both types can be used as well as their combinations. 
Full usage is shown below:
```text
  Usage: ./GDA.sh <options> [output mode]
    -h|-help            Shows this help text.
    -s|-start           Starts existing containers for a service.
                        Starts the stopped containers, can't create new ones.
                        Can be run only in detach mode. There is no output.
    -e|-exit            Exits/Stops running containers without removing them.
                        They can be started again with start command.
    -u|-up              Builds, (re)creates, and starts containers.
                        Run in detached mode or in the background. There is no output.
    -u|-up -o|-output   Shows output of execution for Typesense and GDA.
    -d|-down            Stops containers and by default, the only things removed are:
                          - Containers for services defined in the gda-compose file
                          - Networks defined in the networks section of the gda-compose file
                          - The default network, if one is used
                        Networks and volumes defined as external are never removed.
    -d|-down -r|-reset  Stops containers and removes containers, networks, volumes, and images created by up command.
```

After starting the application it could be found on `localhost` addresses:
- http://127.0.0.1:8000/
- http://0.0.0.0:8000/
- http://localhost:8000/

# Updating data :dvd:
Databases used during the process of creating annotation file could be updated at a certain point in time, so it's important to provide new versions. To provide new versions there is a `data_filenames.json` file which should be added inside `Storage` folder and example of that file is shown below. Purpose of this file is to map database with data source file, so json file should contain only databases which are available inside `DATA_DIRECTORY`. Data for databases which were not found or are not listed inside `data_filenames.json` will be used from integrated databases stored inside source code. 
```json
{
      "DATA_DIRECTORY": "./Data",
      "CLINVAR": "clinvar.txt",
      "COSMIC": "cosmic.csv",
      "DISEASES": "diseases.tsv",
      "DISGENET": "disgenet.tsv",
      "HPO": "hpo.txt",
      "HUMSAVAR": "humsavar.txt",
      "ORPHANET": "orphanet.xml",
      "RGD_OBO": "rgd.txt",
      "OBO": "obo.txt",
      "UNIPROT": "uniprot.dat",
      "HUGO": "hugo.txt",
      "ORPHANET_XREF": "orphanet_xref.xml",
      "ENSEMBL_ENTREZ": "ensembl_entrez.tsv",
      "ENSEMBL_UNIPROT": "ensembl_uniprot.tsv"
}
```

Example of proper `structure` of directories and `data_filenames.json` file:

- `Structure`
```text
   GDA
    ├── GDA.bat
    ├── GDA.sh
    ├── Storage
    │   ├── Data
    │   │   ├── cos.csv
    │   │   ├── diseases.tsv
    │   │   └── obo.txt
    │   ├── error_log.txt
    │   ├── annotation_file.txt
    │   ├── disease_name_doid.jsonl
    │   ├── doid_accuracy.txt
    │   └── data_filenames.json    
    └── gda-compose.yml
```
- `data_filenames.json`

```json
{
      "DATA_DIRECTORY": "./Data",
      "COSMIC": "cos.csv",
      "DISEASES": "diseases.tsv",
      "OBO": "obo.txt"
}
```
# How is it implemented? :brain:

The application consists of two parts:

- `Backend` - created using `Python` programming language, dedicated for creation of annotation file and storing it as a text file.
- `Fronted` - created using `Django` framework, `Datatables` (`JavaScript` and `JQuery`). Dedicated for showing and providing interaction between user and annotation file. Text annotation file is represented as an interactive table.

# Improvements :rocket:
- Should be considered caching data during the process of creating annotation file
- Using Machine Learning methods
- Adding additional data from other resources which could be helpful in the process of information enrichment 

# More details about GDA :books:
There is no official documentation page, but there is my [master thesis](LukaMilosevic_Master_Thesis_Serbian.pdf) only available in Serbian which contains detailed explanation of each part of application, including full implementation explained. 

# License and used resources :earth_asia:
- `Typesense` - https://typesense.org/
- `Databases`
    - `DisGeNet` - https://www.disgenet.org/
    - `COSMIC` - https://cancer.sanger.ac.uk/cosmic
    - `HumsaVar` - https://www.uniprot.org/help/humsavar_change
    - `Orphanet` and `Orphanet Xref` - https://www.orphadata.com/
    - `ClinVar` - https://www.ncbi.nlm.nih.gov/clinvar/
    - `HPO` - https://hpo.jax.org/app/
    - `Diseases` - https://diseases.jensenlab.org/Search
    - `UniProt` - https://www.uniprot.org/
    - `HUGO` - https://www.genenames.org/
    - `OBO` - https://obofoundry.org/
    - `RGD` - https://rgd.mcw.edu/
    - `Ensembl` - https://www.ensembl.org/index.html
- `Images`
    - `freepik` - https://www.freepik.com/
    - `shutterstock` - https://www.shutterstock.com/

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*All links were last accessed in September 2022*

# System :computer:
- Model Name: MacBook Air
- Chip: Apple M1
- Total Number of Cores: 8 (4 performance and 4 efficiency)
- Memory: 16 GB
- Medium Type: SSD
- Capacity: 512 GB
- System Version: macOS 12.3.1 (21E258)
- Kernel Version: Darwin 21.4.0
