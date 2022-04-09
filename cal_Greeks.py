"""
# File         :cal_Greeks.py
# Time         :2022/3/25 14:43
# Author       :Andy
# contact      :2019200836@ruc.edu.cn
# version      :python 3.9
# Description: The calculator of European option Greeks
"""


from numpy import *
from scipy.stats import norm


class greeks_calculator():

    def __init__(self, S, K, T, r, b, P, sigma, iscall: bool):
        """

        :param S:
        :param K:
        :param T:
        :param r:
        :param b:
        :param P:
        :param sigma:
        :param iscall:
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.b = b
        self.P = P
        self.sigma = sigma
        self.iscall = iscall

    def cal_BS_option_price(self):

        real_r = self.r - self.b
        d1 = (log(self.S/self.K) + (real_r + 0.5*self.sigma**2) * self.T)/(self.sigma*sqrt(self.T))
        d2 = d1 - self.sigma * sqrt(self.T)
        if self.iscall:
            return self.S * norm.cdf(d1) - self.K * exp(-real_r * self.T) * norm.cdf(d2)
        else:
            return -self.S * norm.cdf(-d1) + self.K * exp(-real_r * self.T) * norm.cdf(-d2)


    def cal_iv(self, method: str='binary'):

        if method == 'binary':
            sigma_up = 1
            sigma_down = 0.001
            sigma_mid = (sigma_up+sigma_down)/2
            while abs(self.cal_BS_option_price() - self.P) > 0.0001:
                if self.cal_BS_option_price() < self.P < self.cal_BS_option_price():
                    sigma_up = sigma_mid
                    sigma_mid = (sigma_up+sigma_down)/2
                else:
                    sigma_down = sigma_mid
                    sigma_mid = (sigma_up+sigma_down)/2
            return sigma_mid

        elif method == 'newton':
            pass

    def cal_delta(self):

        real_r = self.r - self.b
        d1 = (log(self.S/self.K) + (real_r + 0.5*self.sigma**2) * self.T)/(self.sigma*sqrt(self.T))
        if self.iscall:
            delta = norm.cdf(d1)
        else:
            delta = norm.cdf(d1) - 1
        return delta

    def cal_gamma(self):

        real_r = self.r - self.b
        d1 = (log(self.S/self.K) + (real_r + 0.5*self.sigma**2) * self.T)/(self.sigma*sqrt(self.T))
        return exp(-d1**2 / 2)/(self.S * self.sigma * sqrt(2*pi*self.T))

    def cal_theta(self):

        real_r = self.r - self.b
        d1 = (log(self.S/self.K) + (real_r + 0.5*self.sigma**2) * self.T)/(self.sigma*sqrt(self.T))
        d2 = d1 - self.sigma * sqrt(self.T)
        theta_call = -(self.S * self.sigma * exp(-d1**2 / 2)) / (2 * sqrt(2*pi*self.T)) - real_r * self.K * exp(-real_r * self.T) * norm.cdf(d2)
        if self.iscall:
            theta = theta_call
        else:
            theta = theta_call + real_r * self.K * exp(-self.r*self.T)
        return theta

    def cal_vega(self):

        real_r = self.r - self.b
        d1 = (log(self.S/self.K) + (real_r + 0.5*self.sigma**2) * self.T)/(self.sigma*sqrt(self.T))
        vega = self.S * norm.pdf(d1) * sqrt(real_r) / 100
        return vega