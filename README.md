# VdCallFormat
A simple plugin to open VCF and BCF files in Visidata using cyvsf2 to parse the files.

## Installation

1) Install [Visidata](https://github.com/saulpw/visidata)
2) Install [cyvcf2](https://github.com/brentp/cyvcf2)
3) Create the directory: ```mkdir -p ~/.visidata/plugins```
4) Download the plugin to the directory creted: ```wget -P ~/.visidata/plugins https://raw.githubusercontent.com/rafaeltou/VdCallFormat/refs/heads/main/VdCallFormat.py```
5) Add the plugin to  ~/.visidatarc: ```echo "import plugins.VdCallFormat" >> ~/.visidatarc```

## Usage

The usage is very simple. Once installed, you just point the Visidata to the vcf(.gz)/bcf file, eg: ```vd file.vcf```

### Options:

```--threads=number```: for the number of threads used in the file parsing in cyvcf2. In my tests it doesn't make much difference. the standard value is 4.


```--region=chr:posBegin-posEnd```: for specifying the region you want to see. You can use ```--region=chr:posBegin``` to see a single position and ```--region=chr``` to see an entire chromossome. This option requires your variant file to be indexed, otherwise it will fail. I recommend always using this option if your file is too big, since the visidata will load all of it to the computer's RAM.


Example:
<img width="1167" height="727" alt="image" src="https://github.com/user-attachments/assets/c896321c-bb8c-4bd9-beb5-5fde1dd82f2e" />
