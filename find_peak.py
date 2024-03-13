from scipy import signal as ss
from plotly import graph_objects as go
from scipy.special import voigt_profile
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

class signal_processing:

    def __init__(self):
        pass

    # Run the scipy routine to find peaks in a dataset, returns a dictionary with information about the founded peaks
    def find_peaks(self, x:list, y:list, y_threshold:float, prominence:float, width:float, plot_figure:bool=False)->dict:
        
        peaks_index, peaks_properties = ss.find_peaks(y, height= y_threshold, prominence=prominence, width=width)
        
        peaks_energy = x[peaks_index]
        
        peaks_intensity = y[peaks_index]

        if plot_figure:

            fig = go.Figure()

            # Plot the PL spectra
            fig.add_trace(go.Scatter(
                x=x,
                y=y
            ))

            # Plot the founded peaks
            fig.add_trace(go.Scatter(
                x=peaks_energy,
                y=peaks_intensity,
                mode='markers',
                marker=dict(symbol='x-dot', size=8, line=dict(width=2, color="DarkSlateGrey"))
            ))

            # Plot the intensity threshold
            fig.add_trace(go.Scatter(
                x=x,
                y=[y_threshold for _ in range(len(x))],
                line=dict(dash='dash', color='gray', width=1)
            ))

            fig.update_layout(
                width=300,
                height=200,
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20)
            )           
            
            fig.show()

        peaks_information = {
            'energy':peaks_energy,
            'intensity':peaks_intensity,
            'width':peaks_properties['widths']
        }

        return peaks_information

    def voigt(x:list, *pars):
        y = 0
        
        for i in range(0, len(pars), 4):
            A0 = pars[i]
            xc = pars[i + 1]
            sigma = pars[i + 2]
            gamma = pars[i + 3]
    
            y += A0 * voigt_profile(x-xc, sigma, gamma)
    
        return y
