# TSGenerator manual
<!-- #### October 24, 2021 -->
<!-- #### Tenyo Kawamura (Kavli IPMU, University of Tokyo) -->

## About TSGenerator
**TSGenerator** is a software to simulate a set of maximally stochastic time series.
The method is based on [Timmer \& Koenig, 1995](https://ui.adsabs.harvard.edu/abs/1995A%26A...300..707T/abstract), where the stochastic nature is assumed to be completely described by the power spectrum.

Users should edit `ts_property.py` to set properties of time series, such as the timing interval and power spectrum, and type `python do_simulate_data.py`.
User can check a sample of simulated time series with the command `python do_draw_data.py`.

## Prerequisite
To use **TSGenerator**, users are required to install following software:
- **Python** with standard packages + **Astropy**

