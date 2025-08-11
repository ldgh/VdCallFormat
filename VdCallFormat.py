from visidata import VisiData, SequenceSheet, vd
from pathlib import Path
import pysam

vd.option('region', None, 'Region to fetch in chr:start-end format for pysam')
vd.option('threads', 4, 'Number of threads for pysam decompression')


@VisiData.api
def open_vcf(vd, p: Path):
    region_str = vd.options.get('region')
    num_threads = vd.options.get('threads')
    vcf_handle = pysam.VariantFile(str(p), threads=num_threads)
    return PysamVcfSheet(p.name, source=vcf_handle, region_to_fetch=region_str)

@VisiData.api
def open_bcf(vd, p: Path):
    region_str = vd.options.get('region')
    num_threads = vd.options.get('threads')
    vcf_handle = pysam.VariantFile(str(p), threads=num_threads)
    return PysamVcfSheet(p.name, source=vcf_handle, region_to_fetch=region_str)

class PysamVcfSheet(SequenceSheet):
    def __init__(self, name, source=None, region_to_fetch=None, **kwargs):
        super().__init__(name, source=source, **kwargs)
        self.region_to_fetch = region_to_fetch

    def iterload(self):
        vcf = self.source
        

        header_line = str(vcf.header).strip().split('\n')[-1]
        yield header_line.lstrip('#').split('\t')


        iterator = None
        if self.region_to_fetch:
            try:

                fetch_args = []
                if ':' in self.region_to_fetch:
                    chrom_part, pos_part = self.region_to_fetch.split(':', 1)
                    fetch_args.append(chrom_part)
                    if '-' in pos_part:
                        start_str, end_str = pos_part.split('-', 1)
                        if start_str: fetch_args.append(int(start_str))
                        if end_str:
                            if len(fetch_args) == 1: fetch_args.append(0)
                            fetch_args.append(int(end_str))
                    else:
                        if pos_part:
                            start_pos = int(pos_part) - 1
                            end_pos = int(pos_part)
                            fetch_args.append(start_pos)
                            fetch_args.append(end_pos)
                else:
                    fetch_args.append(self.region_to_fetch)
                iterator = vcf.fetch(*fetch_args)
            except (ValueError, IndexError):
                return
        else:
            iterator = vcf.fetch()

        for record in iterator:
            yield str(record).split('\t')
