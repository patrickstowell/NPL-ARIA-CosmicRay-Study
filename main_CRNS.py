import punpy
import numpy as np
import matplotlib.pyplot as plt
import fp_environmental_correction as fp_envicor
import fc_solar_correction as fc_solarcor
import reading_data as rd
import measurement_function as meas_func


datetime, press, temp, relhum, volt, counts, nsecs, counts_bare, nsecs_bare, cph_filtered = rd.read_measured_data("X:\\Ariadna\\crns_stationary\\observations\\1_CRNS.txt")

fp, fp_ur, fp_us, fp_ut, fp_cov, fp_corr = fp_envicor.propagate_uncertainty_correction_fp(press, temp, relhum, press_u, temp_u, relhum_u)  # replace press_u, temp_u, relhum_u
fc, fc_ur, fc_us, fc_ut, fc_cov, fc_corr = fc_solarcor.propagate_uncertainty_correction_solar(cph_filtered, M0, cph_filtered_u, M0_u)  # replace M0

swc, swc_ur, swc_us, swc_ut, swc_cov, swc_corr = meas_func.propagate_uncertainty_measurement_function(fp, fc, fp_ur, fp_us, fc_ur, fc_us) # need to add N and N0

