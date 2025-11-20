"""
Sample usage of:
    - ADCP_processing_L0_L1.py
    - ADCP_IOS_Header_file.py

Outputs:
    - L0 netCDF ADCP file with geographic_area variable
    - L1 netCDF ADCP file with geographic_area variable
    - L2 netCDF ADCP file 
    - IOS .adcp header file (produced from L1 netCDF ADCP file with geographic_area variable)
    - Full suite of plots for output L1 files
"""

from pycurrents_ADCP_processing import ADCP_processing_L0_L1, ADCP_IOS_Header_file
from pycurrents_ADCP_processing import plot_time_slice_with_naming
from pycurrents_ADCP_processing import ADCP_processing_L2
# from deprecated import add_var2nc

# Define raw ADCP file and associated metadata file
f = './project_data/updated_project_data/SMTETH005_GB_RDIWH_20150520_20150809_D1/SMTETH005_GB_RDIWH_20150520_20150809_D1.pd0' 
meta = './project_data/updated_project_data/SMTETH005_GB_RDIWH_20150520_20150809_D1/SMTETH005_GB_RDIWH_20150520_20150809_D1_metadata.csv'
dest_dir = './processed_data/SMTETH005_pycurrents_processed_GB_RDIWH_20150520_20150809_D1'

# Perform L0 processing on the raw data and export as a netCDF file
# ncname_L0 = ADCP_processing_L0.nc_create_L0(f_adcp=f, f_meta=meta, dest_dir=dest_dir)
ncnames_L0 = ADCP_processing_L0_L1.nc_create_L0_L1(in_file=f, file_meta=meta, dest_dir=dest_dir, level=0)


# Perform L1 processing on the raw data and export as a netCDF file
ncnames_L1 = ADCP_processing_L0_L1.nc_create_L0_L1(in_file=f, file_meta=meta, dest_dir=dest_dir, level=1)

# # Generate a header (.adcp) file from the L1 netCDF file that has the geographic area variable
# for n in ncnames_L1:
#     header_name = ADCP_IOS_Header_file.main_header(n, dest_dir)

#     plot_list = plot_westcoast_nc_LX.create_westcoast_plots(n, dest_dir, do_all_plots=True)

for n in ncnames_L1:
    # 1. Generate IOS .adcp header from L1 netCDF with geographic_area variable
    header_name = ADCP_IOS_Header_file.main_header(n, dest_dir)

    # 2. Create fully customizable plots
    plot_list = plot_time_slice_with_naming.create_westcoast_plots(
        ncfile=n,
        dest_dir=dest_dir,
        filter_type="Godin",             # Temporal filter: Godin, 30h, 35h. Removes variability <time 
        along_angle=137,               # Alongshore angle (degrees CCW from East) # None for automatic
        colourmap_lim=(-0.6, 0.6),     # Limits for all pcolormesh plots in m/s
        time_slice=("2015-06-01 00:00:00", "2015-07-01 00:00:00"), # set to None for full time range otherwise ("2015-06-01 00:00:00", "2015-07-01 00:00:00")
        override_resample=False,       # Set True to skip downsampling for large files
        do_all_plots=True,            # Set False to customise which plots are generated

        # --- Basic QC & diagnostics ---
        do_diagnostic=True,            # Plots for quality control
        do_pressure=True,              # Pressure (PRESPR01) vs time

        # --- Velocity pcolormesh plots ---
        do_ne=True,                    # North/East velocity pcolormesh
        do_ac=True,                    # Alongshore/Cross-shore velocity pcolormesh
        do_filter_ne=True,             # Filtered NE pcolormesh
        do_filter_ac=True,             # Filtered AC pcolormesh

        # --- Single-bin plots ---
        do_single_bin_ne=True,         # Single-bin NE velocity time series
        single_bin_depths=None, # Depths (m) for single-bin plots # can be None for automatic selection or ex: [10, 30, 50]
        # single_bin_inds can be used alternatively to select specific bin indices

        # --- Feather / quiver plots ---
        do_quiver=True,                # Vector plots (velocity arrows)

        # --- Spectral plots ---
        do_single_rotary_spectra=True, # Rotary spectra for single bins
        do_profile_rotary_spectra=True,# Depth-profile of rotary spectra
        do_tidal=True                  # Tidal ellipses / tidal analysis plots
    )

# Perform L2 processing on the L1 netCDF file(s)
for f_adcp in ncnames_L1:
    out_files = ADCP_processing_L2.create_nc_L2(f_adcp, dest_dir)
