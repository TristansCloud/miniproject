# miniproject
## For COMP483  
## Introduction  
  
Lab strains of cells are used by researchers with the expectation that the same strain will produce replicable results. Evolution, however, continues in these cells and may complicate the replication of studies. Here we present a pipeline to compare the current samples of the *E. coli* strain K-12 to historical samples. We compare the number of coding sequences and tRNAs in our current K-12 sample to the assembled genome in RefSeq (NC_000913) using Prokka, then use TopHat and Cufflinks to quantify gene expression in the K-12 derivative BW38028.  
  
## Software Requirements  
### Conda  
Conda environment running python 2.7. Tested on python 2.7.18  

### Install Biopython, sra-tools, Prokka, SPAdes, Tophat, and Cufflinks
```sh 
conda install -c bioconda biopython sra-tools prokka spades tophat cufflinks
```

### Prokka issue

Prokka installed by bioconda can give a `Can't locate Bio/Root/Version.pm` error. I fixed this by running the following code. Change [env_name] to the name of your conda environment. (github.com/tseemann/prokka/issues/519)
```
conda env config vars set PERL5LIB=$CONDA_PREFIX/lib/perl5/site_perl/5.22.0/ -n [env_name]
```

## Command line options
``` 
python miniproject.py --help
   -h --help      show this help message and exit
   -t --threads   Number of CPUs to use in computation. Defaults to half the number of available CPUs (I ran this on my own server)
```
