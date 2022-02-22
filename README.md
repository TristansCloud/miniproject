# miniproject
## For COMP483  
## Introduction  
  
Lab strains of cells are used by researchers with the expectation that the same strain will produce replicable results. Evolution, however, continues in these cells and may complicate the replication of studies. Here we present a pipeline to compare the current samples of the *E. coli* strain K-12 to historical samples. We compare the number of coding sequences and tRNAs in our current K-12 sample to the assembled genome in RefSeq (NC_000913) using Prokka, then use TopHat and Cufflinks to quantify gene expression in the K-12 derivative BW38028.  
  
## Software Requirements  
### Conda  
Conda env running python 3.  

### Prokka, Spades, Tophat, Cufflinks
```sh 
conda install -c bioconda prokka spades tophat cufflinks
```

## Command line options
``` 
miniproject --help
   -h --help      display command line options
   -t --threads   number of CPUs to use in computation
```
