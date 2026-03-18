import punpy
import numpy as np
import matplotlib.pyplot as plt


# combined environemntal correction factor
def correction_fp(press, temp, relhum, P0):  # P0 is the reference air pressure, do we have from file?
    fbar = correction_barometric(press, P0)
    fhum = correction_humidity(relhum, temp)
    return fbar*fhum

def propagate_uncertainty_correction_fp(P0, press, temp, relhum, 
                                        P0_ur, press_ur, temp_ur, relhum_ur,
                                        P0_us, press_us, temp_us, relhum_us):  
    
    prop = punpy.MCPropagation(100)
    fp = correction_fp(press, temp, relhum, P0)

    # your uncertainties
    # press_ur = press*0.05  # 5% random uncertainty
    # temp_ur = temp*0.02  # 2% random uncertainty
    # relhum_ur = relhum*0.03  # 3% random uncertainty

    # press_us = np.ones(5)*0.03  # systematic uncertainty of 0.03
    # temp_us = np.ones(2)*0.03
    # relhum_us = np.ones(3)*0.03

    # if known uncertainties add them here
    # press_ur = press_u
    # temp_ur = temp_u
    # relhum_ur = relhum_u

    # press_us = press_u
    # temp_us = temp_u
    # relhum_us = relhum_u

    print("RANDOM")
    fp_ur = prop.propagate_random(correction_fp, [press, temp, relhum, P0], [press_ur, temp_ur, relhum_ur, P0_ur])
    print("SYSTEMATIC")
    fp_us = prop.propagate_systematic(correction_fp, [press, temp, relhum, P0], [press_us, temp_us, relhum_us, P0_us])

    print("FPCOV")
    fp_ut = (fp_ur**2+fp_us**2)**0.5
    fp_cov = punpy.convert_corr_to_cov(np.eye(len(fp_ur)), fp_ur) +\
        punpy.convert_corr_to_cov(np.ones((len(fp_us), len(fp_us))), fp_us)

    print("Correlation from covar")
    fp_corr = punpy.correlation_from_covariance(fp_cov)
    # fp_cov = None
    # fp_corr = None
    return fp, fp_ur, fp_us, fp_ut, fp_cov, fp_corr


# function barometric pressure
def correction_barometric(press, P0):
    betta = 0.0077
    return np.exp(betta*(press-P0))

def propagate_uncertainty_correction_barometric(press, P0):  # , press, P0_u): if known uncertainties, add them as arguments
        # Monte Carlo propagation
    prop = punpy.MCPropagation(10000)
    fbar = correction_barometric(press, P0)
    
        # your uncertainties
    press_ur = press*0.05  # 5% random uncertainty
    P0_ur = P0*0.02  # 2% random uncertainty

    press_us = np.ones(5)*0.03  # systematic uncertainty of 0.03
    P0_us = np.ones(2)*0.03

        # if known uncertainties add them here
    # press_ur = press_u
    # P0_ur = P0_u

    # press_us = press_u
    # P0_us = P0_u

    fbar_ur = prop.propagate_random(correction_barometric, [press, P0], [press_ur, P0_ur])
    fbar_us = prop.propagate_systematic(correction_barometric, [press, P0], [press_us, P0_us])
    
    fbar_ut = (fbar_ur**2 + fbar_us**2)**0.5

    fbar_cov = punpy.convert_corr_to_cov(np.eye(len(fbar_ur)), fbar_ur) + \
               punpy.convert_corr_to_cov(np.ones((len(fbar_us), len(fbar_us))), fbar_us)
    fbar_corr = punpy.correlation_from_covariance(fbar_cov)
    
    return fbar, fbar_ur, fbar_us, fbar_ut, fbar_cov, fbar_corr


# function humidity correction
def correction_humidity(temp, relhum): # data from file ?
    k = 216.7  # convertion factor from saturation vapour pressure to water vapour density
    epw = 6.112  # pure water saturation vapour pressure
    a = 17.62  # calibration factor pure water
    b = 243.12  # calibration factor pure water
    water_vap = 0.0054  # atmopheric water vaour scaling factor
    return 1 + water_vap*relhum/100*((epw*np.exp(a*temp/(b+temp)))*k/temp+273.16)

def propagate_uncertainty_correction_humidity(temp, relhum, temp_u, relhum_u):
        # Monte Carlo propagation
    prop = punpy.MCPropagation(10000)
    H = correction_humidity(temp, relhum)
    
        # your uncertainties
    temp_ur = temp*0.05  # 5% random uncertainty
    relhum_ur = relhum*0.02  # 2% random uncertainty

    temp_us = np.ones(5)*0.03  # systematic uncertainty of 0.03
    relhum_us = np.ones(2)*0.03

        # if known uncertainties add them here
    # temp_ur = temp_u
    # relhum_ur = relhum_u

    # temp_us = temp_u
    # relhum_us = relhum_u

    H_ur = prop.propagate_random(correction_humidity, [temp, relhum], [temp_ur, relhum_ur])
    H_us = prop.propagate_systematic(correction_humidity, [temp, relhum], [temp_us, relhum_us])
    
    H_ut = (H_ur**2 + H_us**2)**0.5

    # this we do not need for one sensor, unless there is correlation between datetime measurements.
    # this we need for multiple sensors to see how the uncertainties of different sensors are correlated.
    H_cov = punpy.convert_corr_to_cov(np.eye(len(H_ur)), H_ur) + \
               punpy.convert_corr_to_cov(np.ones((len(H_us), len(H_us))), H_us)

    H_corr = punpy.correlation_from_covariance(H_cov) #error correlation of the total uncertainty
    
    return H, H_ur, H_us, H_ut, H_cov, H_corr    