# miniproject  
For COMP483  
## Introduction  
  
Lab strains of cells are used by researchers with the expectation that the same strain will produce replicable results. Evolution, however, continues in these cells and may complicate the replication of studies. Here we present a pipeline to compare the current samples of the *E. coli* strain K-12 to historical samples. We compare the number of coding sequences and tRNAs in our current K-12 sample to the assembled genome in RefSeq (NC_000913) using Prokka. After this, we use TopHat and Cufflinks to quantify gene expression in the K-12 derivative BW38028 using NC_000913 as a reference genome.
  
## Main steps
0. Import libraries and parse command line options
1. Retrieve SRR8185310 Illumina reads for the resequencing of the K-12 project
2. Use SPAdes to assemble the SRR8185310 reads
3. Filter the assembled reads to only include contigs longer than 1000bp
4. Calculate the length of the assembly
5. Use Prokka to annotate the assembly
6. Write Prokka summary results to logfile
7. Find discrepencies in coding sequences and tRNAs between the Prokka assembly and RefSeq NC_000913
8. Use Bowtie2, Tophat, and Cufflinks to map reads of the K-12 derivative BW38028 and quantify their expression using the annotated genome NC_000913
9. Parse Cufflink output and create transcriptome_data.fpkm, which includes the seqname, start, end, and FPKM for each record in the Cufflinks output file
  
  
## Usage
```
python miniproject.py
```
  
## Software Requirements  
### Conda  
Conda environment running python 2.7. Tested on python 2.7.18  
```
conda create -n miniproj python=2.7.18
```
## Install pandas
```
conda install pandas
```

### Install Biopython, SRA-tools, Prokka, SPAdes, Bowtie2, Tophat, and Cufflinks
```sh 
conda install -c bioconda biopython sra-tools prokka spades bowtie2 tophat cufflinks
```

### Prokka issue

Prokka v1.13 is installed by bioconda by default, higher versions of prokka through `conda install` are not possible at this time to my knowledge, at least not without dependency conflicts. I gave up eventually. Conda's version has a few fixable errors. The first is a `Can't locate Bio/Root/Version.pm` error. I fixed this by running the following code. Change [env_name] to the name of your conda environment. (github.com/tseemann/prokka/issues/519)
```
conda env config vars set PERL5LIB=$CONDA_PREFIX/lib/perl5/site_perl/5.22.0/ -n [env_name]
conda activate [env_name]
```  
The second is an issue with prokka parsing the blastp version installed. It parses as a string, so prokka thinks its v2.2 requirement is greater than v2.12 which is installed. (github.com/tseemann/prokka/issues/449)
```
cd $CONDA_PREFIX/bin
nano prokka
# now within nano
^W # search for this text GETVER  => "blastp -version",
# Change MINVER  => "2.2" to MINVER  => "2.1"
# A few lines down is the option for makeblastdb, do the same change you did for blastp:
# Change MINVER  => "2.2" to MINVER  => "2.1"
```

### Bowtie2 issue

Bowtie2 installed from bioconda produces the error `error while loading shared libraries: libtbb.so.2: cannot open shared object file: No such file or directory`. To fix this on Ubuntu/Debian run:
```
sudo apt-get install libtbb2
```

## Command line options
``` 
python miniproject.py --help
   -h --help      show this help message and exit
   -t --threads   Number of CPUs to use in computation. Defaults to half the number of available CPUs (I ran this on my own server)
```
