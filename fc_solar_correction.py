import punpy
import numpy as np
import matplotlib.pyplot as plt

# function Solar correction factor
def correction_solar(M, M0):
    return M0/M

def propagate_uncertainty_correction_solar(cph_filtered, M0, cph_filtered_ur, M0_ur,cph_filtered_us, M0_us ):
    # Monte Carlo propagation
    prop = punpy.MCPropagation(100)
    fc = correction_solar(cph_filtered, M0)
    
        # if known uncertainties add them here
    # cph_filtered_ur = cph_filtered_u
    # M0_ur = M0_u
    # cph_filtered_us = cph_filtered_u
    # M0_us = M0_u

    fc_ur = prop.propagate_random(correction_solar, [cph_filtered, M0], [cph_filtered_ur, M0_ur])
    fc_us = prop.propagate_systematic(correction_solar, [cph_filtered, M0], [cph_filtered_us, M0_us])

    print(fc_ur)
    
    fc_ut = fc_ur # (fc_ur**2 + fc_us**2)**0.5

    fc_cov = punpy.convert_corr_to_cov(np.eye(len(fc_ur)), fc_ur) + \
               punpy.convert_corr_to_cov(np.ones((len(fc_us), len(fc_us))), fc_us)
    fc_corr = punpy.correlation_from_covariance(fc_cov)
    
    return fc, fc_ur, fc_us, fc_ut, fc_cov, fc_corr
