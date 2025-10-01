# GENIE_xsec_extract
Extract GENIE cross section information for plots, event rates, etc...

GENIE generator data releases can be found here: http://www.genie-mc.org/ (under _Data releases_)

**GENIE v3.0.6 G18_10a_02_11a** (MicroBooNE tuning) is the version used by ANNIE simulations, and can be downloaded here: https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v3_00_06/genie_xsec-3.00.06-noarch-G1810a0211a-k250-e1000.tar.bz2

Contained in the tar file are:
- cross-section splines (`gxspl-FNALbig.xml.gz`, `gxspl-FNALsmall.xml.gz`)
- Root file containing extracted cross section data for a variety of targets, neutrino flavors as a function of energy, ranging from ~0.1-100 GeV (`xsec_graphs.root`)

The script in this repo will read from `xsec_graphs.root`.

Please consult the root file for all targets, flavors, interaction type.
