"""
Sample usage of:
    - ADCP_processing_L0_L1.py
    - ADCP_IOS_Header_file.py

Outputs:
    - L0 netCDF ADCP file with geographic_area variable
    - L1 netCDF ADCP file with geographic_area variable
    - L2 netCDF ADCP file 
    - IOS .adcp header file (produced from L1/L2 netCDF ADCP file with geographic_area variable)
    - Full suite of plots for output L1 and L2 files
"""

from pycurrents_ADCP_processing import ADCP_processing_L0_L1, ADCP_IOS_Header_file
from pycurrents_ADCP_processing import plot_westcoast_nc_LX
from pycurrents_ADCP_processing import ADCP_processing_L2

# Define raw ADCP file and associated metadata file
f = './project_data/updated_project_data/SMTETH005_GB_RDIWH_20150520_20150809_D1/SMTETH005_GB_RDIWH_20150520_20150809_D1.pd0' 
meta = './project_data/updated_project_data/SMTETH005_GB_RDIWH_20150520_20150809_D1/SMTETH005_GB_RDIWH_20150520_20150809_D1_metadata.csv'
dest_dir = './processed_data/SMTETH005_pycurrents_processed_GB_RDIWH_20150520_20150809_D1'

# Perform L0 processing
ncnames_L0 = ADCP_processing_L0_L1.nc_create_L0_L1(
    in_file=f,
    file_meta=meta,
    dest_dir=dest_dir,
    level=0
)

# Perform L1 processing
ncnames_L1 = ADCP_processing_L0_L1.nc_create_L0_L1(
    in_file=f,
    file_meta=meta,
    dest_dir=dest_dir,
    level=1
)

# Collect all files (L1 + L2) for plotting
all_nc_files = []
all_nc_files.extend(ncnames_L1)

# Perform L2 processing on the L1 files and add resulting files
for f_adcp in ncnames_L1:
    l2_files = ADCP_processing_L2.create_nc_L2(f_adcp, dest_dir)
    all_nc_files.extend(l2_files)

# Loop over all files (L1 + L2) and generate headers + plots
for ncfile in all_nc_files:
    # 1. Generate IOS .adcp header from netCDF with geographic_area variable
    header_name = ADCP_IOS_Header_file.main_header(ncfile, dest_dir)

    # 2. Create fully customizable plots
    plot_list = plot_westcoast_nc_LX.create_westcoast_plots(
        ncfile=ncfile,
        dest_dir=dest_dir,
        filter_type="Godin",
        along_angle=137,
        colourmap_lim=(-0.5, 0.5),
        override_resample=False,
        do_all_plots=True,

        # --- Basic QC & diagnostics ---
        do_diagnostic=True,
        do_pressure=True,

        # --- Velocity pcolormesh plots ---
        do_ne=True,
        do_ac=True,
        do_filter_ne=True,
        do_filter_ac=True,

        # --- Single-bin plots ---
        do_single_bin_ne=True,
        single_bin_depths=None,

        # --- Feather / quiver plots ---
        do_quiver=True,

        # --- Spectral plots ---
        do_single_rotary_spectra=True,
        do_profile_rotary_spectra=True,
        do_tidal=True
    )
