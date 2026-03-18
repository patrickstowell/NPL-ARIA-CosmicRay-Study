import punpy
import numpy as np
import matplotlib.pyplot as plt
import fp_environmental_correction as fp_envicor
import fc_solar_correction as fc_solarcor

# your measurement function
def measurement_function(fp, fc, N, N0, robulk):
  a0 = 0.0808
  a1 = 0.372
  a2 = 0.115
  robulk = 1.0 #g/cm3

  return (a0/(fp*fc*(N/N0)-a1) - a2)*robulk


def propagate_uncertainty_measurement_function(fp, fc, N, N0, robulk, 
                                               fp_ur, fc_ur, N_ur, N0_ur, robulk_ur,
                                               fp_us, fc_us, N_us, N0_us, robulk_us):
        # Monte Carlo propagation
    prop = punpy.MCPropagation(100)
    vwc = measurement_function(fp, fc,) # need to add N, N0, robulk
    
        #progagated uncertainties

    vwc_ur = prop.propagate_random(measurement_function, [fp, fc, N, N0, robulk], 
                                  [fp_ur, fc_ur, N_ur, N0_ur, robulk_ur])
    
    vwc_us = prop.propagate_systematic(measurement_function, [fp, fc, N, N0, robulk], 
                                      [fp_us, fc_us, N_us, N0_us, robulk_us])
    
    vwc_ut = (vwc_ur**2 + vwc_us**2)**0.5

    vwc_cov = None
    vwc_corr = None
    
    # vwc_cov = punpy.convert_corr_to_cov(np.eye(len(vwc_ur)), vwc_ur) + \
    #            punpy.convert_corr_to_cov(np.ones((len(vwc_us), len(vwc_us))), vwc_us)
    # vwc_corr = punpy.correlation_from_covariance(vwc_cov)
    
    return vwc, vwc_ur, vwc_us, vwc_ut, vwc_cov, vwc_corr
